"""
Model evaluation utilities for the churn prediction project.

This module provides functions to evaluate trained models and
generate performance metrics and reports.
"""

from sklearn.metrics import classification_report, confusion_matrix
from typing import Any


def evaluate_model(model: Any, X_test: Any, y_test: Any) -> None:
    """
    Evaluate a trained model on test data and print performance metrics.

    Args:
        model: Trained machine learning model with predict method.
        X_test: Test feature matrix.
        y_test: True labels for test data.
    """
    preds = model.predict(X_test)
    print("Classification Report:\n", classification_report(y_test, preds))
    print("Confusion Matrix:\n", confusion_matrix(y_test, preds))