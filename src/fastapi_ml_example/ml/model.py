import logging

import pandas as pd
from catboost import CatBoostClassifier

from fastapi_ml_example.ml.config import config
from fastapi_ml_example.schemas.dto import FeaturesPayload

log = logging.getLogger(__name__)


class Model:
    "Model inference class."

    def __init__(self) -> None:
        "Load model from file."
        self.model = CatBoostClassifier()
        if config.model_path.exists():
            self.model.load_model(config.model_path)
            log.info("Loaded trained model from %s", config.model_path)
        else:
            log.error("Trained model not found at %s", config.model_path)

    def predict(self, features: FeaturesPayload) -> float:
        "Model prediction."
        data = pd.DataFrame([features])
        proba = self.model.predict_proba(data)[0][1]
        return float(proba)


def load_model() -> Model:
    return Model()
