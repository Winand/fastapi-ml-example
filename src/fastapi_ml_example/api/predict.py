from fastapi import APIRouter

from fastapi_ml_example.api.deps import PredictionServiceDep
from fastapi_ml_example.schemas.predict import PredictRequest, PredictResponse

router = APIRouter(tags=["predict"])


@router.post("/predict")
async def predict(
    payload: PredictRequest, service: PredictionServiceDep,
) -> PredictResponse:
    return service.predict(payload)
