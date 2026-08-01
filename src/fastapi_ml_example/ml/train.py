import logging
from pathlib import Path

import pandas as pd
from catboost import CatBoostClassifier
from catboost.datasets import adult

from fastapi_ml_example.core.logging import configure_logging
from fastapi_ml_example.ml.config import config

configure_logging(logging.INFO, log_file=Path("train.log"))
log = logging.getLogger(__name__)


def prepare_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    "Split input DataFrame into X and y and determine categorical features."
    df.columns = df.columns.str.replace("-", "_")  # simplifies schema description

    target_col = "income"
    x = df.drop(columns=[target_col])
    y = df[target_col].str.contains(">50K").astype(int)

    cat_features: list[str] = x.select_dtypes(include=["str", "category"]) \
        .columns.to_list()
    x[cat_features] = x[cat_features].fillna('NaN').astype(str)
    return x, y, cat_features


def train() -> None:
    "Train and save CatBoost model."
    log.info("Start model training...")

    # Load data
    dataset = adult
    p = Path(".dataset-cache") / dataset.__name__
    if p.is_dir():  # dataset was cached
        train_df = pd.read_parquet(p / "train_df.parquet")
        test_df = pd.read_parquet(p / "test_df.parquet")
    else:
        train_df, test_df = dataset()
        p.mkdir(parents=True, exist_ok=True)
        train_df.to_parquet(p / "train_df.parquet")
        test_df.to_parquet(p / "test_df.parquet")

    # Prepare features and target
    x_train, y_train, cat_features = prepare_data(train_df)
    x_test, y_test, _ = prepare_data(test_df)

    print("X:", x_train.columns.to_list())
    print(x_train)
    print("y:", y_train.name)
    print("Categorical features:", cat_features)

    # Training stage
    model = CatBoostClassifier(
        iterations=config.iterations,
        learning_rate=config.learning_rate,
        depth=config.depth,
        random_seed=42,
        early_stopping_rounds=config.early_stopping_rounds,
    ).fit(
        x_train, y_train, cat_features, eval_set=(x_test, y_test), verbose=50,
    )
    log.info("Training finished")

    # Test model accuracy
    final_acc = model.score(x_test, y_test)
    log.info("Accuracy %.4f", final_acc)

    # Save model
    config.model_path.parent.mkdir(parents=True, exist_ok=True)
    model.save_model(config.model_path)
    log.info("Model saved to %s", config.model_path)


if __name__ == "__main__":
    train()
