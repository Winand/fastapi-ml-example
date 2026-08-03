from pydantic import BaseModel


class IncomePredictRequest(BaseModel):
    "Income prediction input data."
    age: float
    workclass: str
    fnlwgt: float
    education: str
    education_num: float
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: float
    capital_loss: float
    hours_per_week: float
    native_country: str


class IncomePredictResponse(BaseModel):
    "Income prediction result."
    income_ge_50k: float


class CountryPredictRequest(BaseModel):
    "Native country prediction input data."
    age: float
    workclass: str
    fnlwgt: float
    education: str
    education_num: float
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: float
    capital_loss: float
    hours_per_week: float
    income: str


class CountryPredictResponse(BaseModel):
    "Native country prediction result."
    native_country: str


# keys are api.predict route names (method names by default)
EMPTY_RESPONSES: dict[str, BaseModel] = {
    "predict_income": IncomePredictResponse(income_ge_50k=.0),
    "predict_country": CountryPredictResponse(native_country="United-States"),
}
