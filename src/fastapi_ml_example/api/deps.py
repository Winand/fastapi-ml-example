from typing import Annotated

from fastapi import Depends, Request

from fastapi_ml_example.ml.model import Model
from fastapi_ml_example.services.prediction_service import PredictionService


def get_model(request: Request) -> Model:
    "Get ML model instance from app state."
    return request.app.state.model


def get_prediction_service(
    model: Annotated[Model, Depends(get_model)],
) -> PredictionService:
    "Prediction service dependency."
    return PredictionService(model)

PredictionServiceDep = Annotated[PredictionService, Depends(get_prediction_service)]
