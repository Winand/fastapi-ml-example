"Prediction data flow orchestration."
from fastapi_ml_example.core.metrics import INFERENCE_TIME
from fastapi_ml_example.ml.model import Model
from fastapi_ml_example.schemas.predict import PredictRequest, PredictResponse


class PredictionService:
    "Prediction data flow orchestration class."

    def __init__(self, model: Model) -> None:
        "Set current model."
        self.model = model

    def predict(self, payload: PredictRequest) -> PredictResponse:
        "Call model prediction."
        with INFERENCE_TIME.time():
            prediction = self.model.predict(payload.model_dump())
        return PredictResponse(income_ge_50k=prediction)
