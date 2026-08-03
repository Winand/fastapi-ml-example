import logging

import pandas as pd
from catboost import CatBoostClassifier

from fastapi_ml_example.ml.config import config
from fastapi_ml_example.schemas.dto import CountryFeatures, IncomeFeatures

log = logging.getLogger(__name__)


class IncomeModel:
    "Income model inference class."

    def __init__(self) -> None:
        "Load model from file."
        self.model = CatBoostClassifier()
        if config.income.model_path.exists():
            self.model.load_model(config.income.model_path)
            log.info("Loaded trained model from %s", config.income.model_path)
        else:
            log.error("Trained model not found at %s", config.income.model_path)

    def predict(self, features: IncomeFeatures) -> float:
        "Model prediction."
        data = pd.DataFrame([features])
        proba = self.model.predict_proba(data)[0][1]
        return float(proba)


class CountryModel:
    "Native country model inference class."

    def __init__(self) -> None:
        "Load model from file."
        self.model = CatBoostClassifier()
        if config.country.model_path.exists():
            self.model.load_model(config.country.model_path)
            log.info("Loaded trained model from %s", config.country.model_path)
        else:
            log.error("Trained model not found at %s", config.country.model_path)

    def predict(self, features: CountryFeatures) -> str:
        "Model prediction."
        data = pd.DataFrame([features])
        return self.model.predict(data)[0][0]


def load_income_model() -> IncomeModel:
    return IncomeModel()


def load_country_model() -> CountryModel:
    return CountryModel()
