from typing import override

from fastapi_ml_example.ml.model import Model
from fastapi_ml_example.schemas.predict import PredictRequest
from fastapi_ml_example.services.prediction_service import PredictionService


class StubModel(Model):
    "ML model stub for prediction service."
    @override
    def predict(self, feature_a: float, feature_b: str) -> float:
        return feature_a * 2


def test_prediction_service_returns_model_prediction() -> None:
    "Prediction service calls an ML model and returns its result."
    service = PredictionService(StubModel())
    payload = PredictRequest(feature_a=3.0, feature_b="value")
    expected_prediction = 6.0

    result = service.predict(payload)
    assert result.prediction == expected_prediction
