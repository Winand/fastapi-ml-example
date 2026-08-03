from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

ARTIFACT_DIR: Path = Path(__file__).parent / "artifacts"


class ModelSettings(BaseSettings):
    "Default hyperparameters for a model."
    model_path: Path
    iterations: int = 250
    learning_rate: float = 0.08
    depth: int = 6
    early_stopping_rounds: int = 30

    verbosity: int = 50


class IncomeModelConfig(ModelSettings):
    "Income model settings."
    model_config = SettingsConfigDict(env_prefix="INCOME_")  # pydantic-settings
    model_path: Path = ARTIFACT_DIR / "income_model.cbm"


class CountryModelConfig(ModelSettings):
    "Native country model settings."
    model_config = SettingsConfigDict(env_prefix="COUNTRY_")  # pydantic-settings
    model_path: Path = ARTIFACT_DIR / "country_model.cbm"


class Config(BaseSettings):
    "ML configuration class."
    income: IncomeModelConfig = IncomeModelConfig()
    country: CountryModelConfig = CountryModelConfig()
    # common hyperparamenters
    task_type: Literal["CPU", "GPU"] = "GPU"
    random_seed: int = 42


config = Config()
