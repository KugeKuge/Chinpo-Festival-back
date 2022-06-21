from pydantic import BaseModel

class ChinpoTweet(BaseModel):
    tweet_id: str
    user_id: str
    user_name: str
    text: str
    created_at: str