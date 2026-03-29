from pydantic import BaseModel

class AnalyzeResponse(BaseModel):
    keywords: list
    sentiment: float
    similarity: float
    truth: float
    credibility: float
    final_score: float
    verdict: str