from pymongo import MongoClient

## MongoClient
client = MongoClient('mongodb+srv://admin:admin@cluster0.spluvvn.mongodb.net/?retryWrites=true&w=majority')
chinpo_tweet_db = client.ChinpoTweet
chinpo_tweet_collection = chinpo_tweet_db.ChinpoTweet
latest_chinpo_tweet_time = chinpo_tweet_db.LastGet

def insert_chinpo_one(document):
    chinpo_tweet_collection.insert_one(document)

def remove_all_chinpoTweets():
    chinpo_tweet_collection.delete_many({})

def get_all_chinpo_tweet():
    return chinpo_tweet_collection.find({},{'_id':0}).sort([{"created_at", -1}])

def get_latest_chinpo_time():
    latest_chinpo_time = latest_chinpo_tweet_time.find_one()
    return latest_chinpo_time

def delete_and_insert_latest_chinpo_time(latest_time):
    latest_chinpo_tweet_time.delete_many({})
    latest_chinpo_tweet_time.insert_one(latest_time)