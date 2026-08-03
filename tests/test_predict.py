from typing import override

from fastapi import status
from fastapi.testclient import TestClient

from fastapi_ml_example.api.deps import get_income_model
from fastapi_ml_example.main import app
from fastapi_ml_example.ml.model import IncomeModel
from fastapi_ml_example.schemas.dto import IncomeFeatures
from fastapi_ml_example.schemas.predict import EMPTY_RESPONSES

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
    invalid_payload = {"feature_a": 1.0, "feature_b": "test"}
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == EMPTY_RESPONSES["predict_income"].model_dump()


def test_predict_unhandled_exception_returns_500(client: TestClient) -> None:
    "Generate HTTP 500 error on unknown errors and return default response."
    class FailingModel(IncomeModel):
        @override
        def predict(self, features: IncomeFeatures) -> float:
            msg = "unknown error"
            raise ValueError(msg)
    app.dependency_overrides[get_income_model] = FailingModel
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == EMPTY_RESPONSES["predict_income"].model_dump()
