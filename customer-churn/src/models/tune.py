"""
Model hyperparameter tuning utilities for the churn prediction project.

This module provides functions to optimize model hyperparameters
using Optuna for better performance.
"""

import optuna
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score
from typing import Any, Dict


def tune_model(X: Any, y: Any) -> Dict[str, Any]:
    """
    Tune XGBoost hyperparameters using Optuna optimization.

    Args:
        X: Feature matrix.
        y: Target vector.

    Returns:
        Dict containing the best hyperparameters found.
    """
    def objective(trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 300, 800),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2),
            "max_depth": trial.suggest_int("max_depth", 3, 10),
            "subsample": trial.suggest_float("subsample", 0.5, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
            "random_state": 42,
            "n_jobs": -1,
            "eval_metric": "logloss"
        }
        model = XGBClassifier(**params)
        scores = cross_val_score(model, X, y, cv=3, scoring="recall")
        return scores.mean()

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=20)

    print("Best Params:", study.best_params)
    return study.best_params