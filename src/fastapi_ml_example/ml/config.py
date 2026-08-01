from pathlib import Path

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    "ML configuration class."
    artifact_dir: Path = Path(__file__).parent / "artifacts"
    model_path: Path = artifact_dir / "catboost_model.cbm"

    # Гиперпараметры по умолчанию
    iterations: int = 250
    learning_rate: float = 0.08
    depth: int = 6
    early_stopping_rounds: int = 30


config = Config()
