from typing import Annotated

from fastapi import Depends, Request

from fastapi_ml_example.ml.model import CountryModel, IncomeModel
from fastapi_ml_example.services.prediction_service import (
    CountryPredictionService,
    IncomePredictionService,
)


def get_income_model(request: Request) -> IncomeModel:
    "Get income ML model instance from app state."
    return request.app.state.income_model


def get_income_prediction_service(
    model: Annotated[IncomeModel, Depends(get_income_model)],
) -> IncomePredictionService:
    "Prediction service dependency."
    return IncomePredictionService(model)

IncomePredictionServiceDep = Annotated[
    IncomePredictionService, Depends(get_income_prediction_service),
]


def get_country_model(request: Request) -> CountryModel:
    "Get country ML model instance from app state."
    return request.app.state.country_model


def get_country_prediction_service(
    model: Annotated[CountryModel, Depends(get_country_model)],
) -> CountryPredictionService:
    "Prediction service dependency."
    return CountryPredictionService(model)

CountryPredictionServiceDep = Annotated[
    CountryPredictionService, Depends(get_country_prediction_service),
]
