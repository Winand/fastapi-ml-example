from collections.abc import Generator
from typing import override

import pytest
from fastapi.testclient import TestClient

from fastapi_ml_example.api.deps import get_income_model
from fastapi_ml_example.main import app
from fastapi_ml_example.ml.model import IncomeModel
from fastapi_ml_example.schemas.dto import IncomeFeatures


class StubModel(IncomeModel):
    "ML model stub for FastAPI TestClient tests."
    @override
    def predict(self, features: IncomeFeatures) -> float:
        return 42.0


@pytest.fixture
def client() -> Generator[TestClient]:
    "FastAPI TestClient with ML model stub."
    app.dependency_overrides[get_income_model] = StubModel
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
