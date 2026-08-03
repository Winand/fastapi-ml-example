"Prediction data flow orchestration."
from typing import cast

from fastapi_ml_example.core.metrics import INFERENCE_TIME
from fastapi_ml_example.ml.model import CountryModel, IncomeModel
from fastapi_ml_example.schemas.dto import CountryFeatures, IncomeFeatures
from fastapi_ml_example.schemas.predict import (
    CountryPredictRequest,
    CountryPredictResponse,
    IncomePredictRequest,
    IncomePredictResponse,
)


class IncomePredictionService:
    "Income prediction data flow orchestration class."

    def __init__(self, model: IncomeModel) -> None:
        "Set current model."
        self.model = model

    def predict(self, payload: IncomePredictRequest) -> IncomePredictResponse:
        "Call model prediction."
        with INFERENCE_TIME.labels("income").time():
            prediction = self.model.predict(cast(IncomeFeatures, payload.model_dump()))
        return IncomePredictResponse(income_ge_50k=prediction)


class CountryPredictionService:
    "Country prediction data flow orchestration class."

    def __init__(self, model: CountryModel) -> None:
        "Set current model."
        self.model = model

    def predict(self, payload: CountryPredictRequest) -> CountryPredictResponse:
        "Call model prediction."
        with INFERENCE_TIME.labels("country").time():
            prediction = self.model.predict(cast(CountryFeatures, payload.model_dump()))
        return CountryPredictResponse(native_country=prediction)
