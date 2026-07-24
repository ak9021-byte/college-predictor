from fastapi import APIRouter
from schemas.predict import PredictRequest, PredictResponse
from services.prediction import predict_colleges

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    results = predict_colleges(student_rank=request.rank, category=request.category)
    return PredictResponse(results=results, total_matches=len(results))