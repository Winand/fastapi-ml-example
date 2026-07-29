from fastapi import APIRouter

from fastapi_ml_example.api.custom_routes import CatchExceptionsWithBodyRoute
from fastapi_ml_example.api.deps import PredictionServiceDep
from fastapi_ml_example.schemas.predict import PredictRequest, PredictResponse

router = APIRouter(tags=["predict"], route_class=CatchExceptionsWithBodyRoute)


@router.post("/predict")
async def predict(
    payload: PredictRequest, service: PredictionServiceDep,
) -> PredictResponse:
    "Run inference."
    return service.predict(payload)
