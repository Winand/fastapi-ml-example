from collections.abc import Generator
from typing import override

import pytest
from fastapi.testclient import TestClient

from fastapi_ml_example.api.deps import get_model
from fastapi_ml_example.main import app
from fastapi_ml_example.ml.model import Model


class StubModel(Model):
    "ML model stub for FastAPI TestClient tests."
    @override
    def predict(self, feature_a: float, feature_b: str) -> float:
        return 42.0


@pytest.fixture
def client() -> Generator[TestClient]:
    "FastAPI TestClient with ML model stub."
    app.dependency_overrides[get_model] = StubModel
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
