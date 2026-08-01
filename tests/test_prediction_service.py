from typing import override

from fastapi_ml_example.ml.model import Model
from fastapi_ml_example.schemas.dto import FeaturesPayload
from fastapi_ml_example.schemas.predict import PredictRequest
from fastapi_ml_example.services.prediction_service import PredictionService


class StubModel(Model):
    "ML model stub for prediction service."
    @override
    def predict(self, features: FeaturesPayload) -> float:
        return 0.5


def test_prediction_service_returns_model_prediction() -> None:
    "Prediction service calls an ML model and returns its result."
    service = PredictionService(StubModel())
    payload = PredictRequest(
        age = 0,
        workclass = "",
        fnlwgt = 0,
        education = "",
        education_num = 0,
        marital_status = "",
        occupation = "",
        relationship = "",
        race = "",
        sex = "",
        capital_gain = 0,
        capital_loss = 0,
        hours_per_week = 0,
        native_country = "",
    )
    expected_prediction = 0.5

    result = service.predict(payload)
    assert result.income_ge_50k == expected_prediction
