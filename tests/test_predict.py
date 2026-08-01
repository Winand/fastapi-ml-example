from typing import override

from fastapi import status
from fastapi.testclient import TestClient

from fastapi_ml_example.api.deps import get_model
from fastapi_ml_example.main import app
from fastapi_ml_example.ml.model import Model
from fastapi_ml_example.schemas.dto import FeaturesPayload
from fastapi_ml_example.schemas.predict import EMPTY_RESPONSE

VALID_PAYLOAD = {
    "age": 0,
    "workclass": "",
    "fnlwgt": 0,
    "education": "",
    "education_num": 0,
    "marital_status": "",
    "occupation": "",
    "relationship": "",
    "race": "",
    "sex": "",
    "capital_gain": 0,
    "capital_loss": 0,
    "hours_per_week": 0,
    "native_country": "",
}


def test_predict_success(client: TestClient) -> None:
    "Test /predict endpoint response."
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"income_ge_50k": 42.0}


def test_predict_invalid_payload_returns_422(client: TestClient) -> None:
    "Generate HTTP 422 error on invalid input data and return default response."
    invalid_payload = {"feature_a": "not-a-float", "feature_b": "test"}
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == EMPTY_RESPONSE.model_dump()


def test_predict_unhandled_exception_returns_500(client: TestClient) -> None:
    "Generate HTTP 500 error on unknown errors and return default response."
    class FailingModel(Model):
        @override
        def predict(self, features: FeaturesPayload) -> float:
            msg = "unknown error"
            raise ValueError(msg)
    app.dependency_overrides[get_model] = FailingModel
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == EMPTY_RESPONSE.model_dump()
