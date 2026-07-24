from pydantic import BaseModel
from typing import List
from typing import Optional

class PredictRequest(BaseModel):
    rank: int
    category: str

class PredictionResult(BaseModel):
    college_name: str
    branch_name: str
    category: str
    opening_rank: Optional[int] = None
    closing_rank: int
    chance: str

class PredictResponse(BaseModel):
    results: List[PredictionResult]
    total_matches: int