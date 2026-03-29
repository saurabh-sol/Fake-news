from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    tweet: str
    likes: int
    retweets: int
    comments: int
    verified: bool
    time_range: str = "1w"