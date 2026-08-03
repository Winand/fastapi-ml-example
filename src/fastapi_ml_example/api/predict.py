from fastapi import APIRouter

from fastapi_ml_example.api.custom_routes import CatchExceptionsWithBodyRoute
from fastapi_ml_example.api.deps import (
    CountryPredictionServiceDep,
    IncomePredictionServiceDep,
)
from fastapi_ml_example.schemas.predict import (
    CountryPredictRequest,
    CountryPredictResponse,
    IncomePredictRequest,
    IncomePredictResponse,
)

router = APIRouter(tags=["predict"], route_class=CatchExceptionsWithBodyRoute)


@router.post("/predict")
@router.post("/predict/income")
async def predict_income(
    payload: IncomePredictRequest, service: IncomePredictionServiceDep,
) -> IncomePredictResponse:
    "Run income>=50k inference."
    return service.predict(payload)


@router.post("/predict/country")
async def predict_country(
    payload: CountryPredictRequest, service: CountryPredictionServiceDep,
) -> CountryPredictResponse:
    "Run native country inference."
    return service.predict(payload)
