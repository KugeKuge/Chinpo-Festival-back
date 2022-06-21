import tweepy
from datetime import datetime,timezone, timedelta
from Utils import database

# API情報を記入
BEARER_TOKEN        = "AAAAAAAAAAAAAAAAAAAAAL9mdwEAAAAAkzydybhWZO%2BFya4NxnEEX2UUcxM%3DruoCBiG7cfqWgPw9yLDs1WjE00pSyjHBm4vVMs2raJAE5FKzaL"
API_KEY             = "Mbd4HEdPl8lpUJmW8ftz3YAS6"
API_SECRET          = "ARkuqFp2ilJszgT4ksv5TT25atveuZSD3eP1Lv3mHxXXmYMhF2"
ACCESS_TOKEN        = "627025270-FJJtG9HLCOXLTeHvobLywL7qRQpDlK9INY0y98FK"
ACCESS_TOKEN_SECRET = "sAFaWKi3lo9vJZDpL2tM0SW6EYVMfnrlhvzOZlshAObkL"

now = datetime.now()
now = now.replace(minute=0, second=0, microsecond=0)
end_time_tweepy = str(now.isoformat())+'+09:00'
start_time = now - timedelta(days=1) 
start_time_tweepy = str(start_time.isoformat())+'+09:00'

# ★必要情報入力
SEARCH_CHARACTER    = "ちんぽ OR チンポ"  # 検索対象
TWEET_MAX = 100           # 取得したいツイート数(10〜100で設定可能)
LAST_GET_MINUTES = -5     # 5分以上処理されてなかったら再取得する

# クライアント関数を作成
def ClientInfo():
	# 取得対象のツイートの時間幅を指定する この例では実行前の２４時間としています。
	# iso形式のUTC時間で指定しないと正しく時間指定ができない模様。
	# 指定した時間幅に、limitで指定した件数以上のツイートがあってもlimit以上は取得しません。

    client = tweepy.Client(bearer_token    = BEARER_TOKEN,
                           consumer_key    = API_KEY,
                           consumer_secret = API_SECRET,
                           access_token    = ACCESS_TOKEN,
                           access_token_secret = ACCESS_TOKEN_SECRET,
                          )
    return client

def change_time_JST(u_time):
    #イギリスのtimezoneを設定するために再定義する
    utc_time = datetime(u_time.year, u_time.month,u_time.day, \
    u_time.hour,u_time.minute,u_time.second, tzinfo=timezone.utc)
    #タイムゾーンを日本時刻に変換
    jst_time = utc_time.astimezone(timezone(timedelta(hours=+9), 'JST'))
    # 文字列で返す
    str_time = jst_time.strftime("%Y-%m-%d_%H:%M:%S")
    return str_time

# Tweet検索処理
def get_chinpo_tweet_from_twitter():
    # 直近のツイート取得
    tweets = ClientInfo().search_recent_tweets(query = SEARCH_CHARACTER, max_results = TWEET_MAX,
            tweet_fields = ['author_id', 'created_at'],
            expansions = ['author_id'])

    # 取得したデータ加工
    results     = []
    tweets_data = tweets.data

    # tweet検索結果取得
    if tweets_data != None:
        for tweet in tweets_data:
            obj = {}
            obj["tweet_id"] = tweet.id      # Tweet_ID
            obj["text"] = tweet.text  # Tweet Content
            obj["created_at"] = change_time_JST(tweet.created_at) # Tweet date

            for i in range(len(tweets.includes['users'])):
                if tweet.author_id == tweets.includes['users'][i]['id']:
                    obj['user_id'] = tweets.includes['users'][i]['username']
                    obj['user_name'] = tweets.includes['users'][i]['name']

            results.append(obj)
    else:
        results.append('')
    
    return results

def search_tweet(): #search,tweet_max):    
    # 最新ちんぽ取得時刻を取得
    latest_chinpo_time = database.get_latest_chinpo_time()

    # もし前回取得から1分経っていない場合はDBから結果を返す
    if latest_chinpo_time == None:
        latest_chinpo_datetime = datetime.now() + timedelta(minutes=-100)
    else:
        latest_chinpo_datetime = datetime.strptime(latest_chinpo_time['latest_time'], '%Y-%m-%d_%H:%M:%S')
    
    if datetime.now() + timedelta(minutes=LAST_GET_MINUTES) > latest_chinpo_datetime:
        # 1分以上たっている場合はDB全消ししてTwitterから取得し入れなおす。
        chinpo_tweets_from_twitter = get_chinpo_tweet_from_twitter()

        database.remove_all_chinpoTweets()
        
        for document in chinpo_tweets_from_twitter:
            database.insert_chinpo_one(document)
            del document['_id']
        
        # 最終更新時刻を更新
        database.delete_and_insert_latest_chinpo_time({"latest_time": datetime.now().strftime('%Y-%m-%d_%H:%M:%S')})
        
        return list(chinpo_tweets_from_twitter)
    else:
        # DBから取得して返す
        return list(database.get_all_chinpo_tweet())
