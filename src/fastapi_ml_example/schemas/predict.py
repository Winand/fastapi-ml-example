from pydantic import BaseModel


class PredictRequest(BaseModel):
    "Prediction input data."
    feature_a: float
    feature_b: str


class PredictResponse(BaseModel):
    "Prediction result."
    prediction: float
