import logging
from pathlib import Path

import click
import pandas as pd
from catboost import CatBoostClassifier
from catboost.datasets import adult

from fastapi_ml_example.core.logging import configure_logging
from fastapi_ml_example.ml.config import config

configure_logging(logging.INFO, log_file=Path("train.log"))
log = logging.getLogger(__name__)


@click.group()
def cli() -> None:
    "Train CatBoost models."


def prepare_income_data(df: pd.DataFrame,
                        ) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    "Split input DataFrame into X and y and determine categorical features."
    df.columns = df.columns.str.replace("-", "_")  # simplifies schema description

    target_col = "income"
    x = df.drop(columns=[target_col])
    y = df[target_col].str.contains(">50K").astype(int)

    cat_features: list[str] = x.select_dtypes(include=["str", "category"]) \
        .columns.to_list()
    x[cat_features] = x[cat_features].fillna('NaN').astype(str)
    return x, y, cat_features


@cli.command("income")
def train_income_model() -> None:
    "Train and save income CatBoost model."
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
    x_train, y_train, cat_features = prepare_income_data(train_df)
    x_test, y_test, _ = prepare_income_data(test_df)

    print("X:", x_train.columns.to_list())
    print(x_train)
    print("y:", y_train.name)
    print("Categorical features:", cat_features)

    # Training stage
    model = CatBoostClassifier(
        task_type=config.task_type,
        iterations=config.income.iterations,
        learning_rate=config.income.learning_rate,
        depth=config.income.depth,
        random_seed=config.random_seed,
        early_stopping_rounds=config.income.early_stopping_rounds,
    ).fit(
        x_train, y_train, cat_features, eval_set=(x_test, y_test),
        verbose=config.income.verbosity,
    )
    log.info("Training finished")

    # Test model accuracy
    final_acc = model.score(x_test, y_test)
    log.info("Accuracy %.4f", final_acc)

    # Save model
    config.income.model_path.parent.mkdir(parents=True, exist_ok=True)
    model.save_model(config.income.model_path)
    log.info("Model saved to %s", config.income.model_path)


def prepare_country_data(df: pd.DataFrame,
                         ) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    "Split input DataFrame into X and y and determine categorical features."
    df.columns = df.columns.str.replace("-", "_")  # simplifies schema description

    target_col = "native_country"
    x = df.drop(columns=[target_col])
    y = df[target_col]

    cat_features: list[str] = x.select_dtypes(include=["str", "category"]) \
        .columns.to_list()
    x[cat_features] = x[cat_features].fillna('NaN').astype(str)
    return x, y, cat_features


@cli.command("country")
def train_country_model() -> None:
    "Train and save native country CatBoost model."
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
    x_train, y_train, cat_features = prepare_country_data(train_df)
    x_test, y_test, _ = prepare_country_data(test_df)

    print("X:", x_train.columns.to_list())
    print(x_train)
    print("y:", y_train.name)
    print("Categorical features:", cat_features)

    # Training stage
    model = CatBoostClassifier(
        task_type=config.task_type,
        iterations=config.country.iterations,
        learning_rate=config.country.learning_rate,
        depth=config.country.depth,
        random_seed=config.random_seed,
        early_stopping_rounds=config.country.early_stopping_rounds,
    ).fit(
        x_train, y_train, cat_features, eval_set=(x_test, y_test),
        verbose=config.country.verbosity,
    )
    log.info("Training finished")

    # Test model accuracy
    final_acc = model.score(x_test, y_test)
    log.info("Accuracy %.4f", final_acc)

    # Save model
    config.country.model_path.parent.mkdir(parents=True, exist_ok=True)
    model.save_model(config.country.model_path)
    log.info("Model saved to %s", config.country.model_path)


if __name__ == "__main__":
    cli()
