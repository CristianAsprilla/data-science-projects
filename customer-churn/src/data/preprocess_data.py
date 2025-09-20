"""
Data preprocessing utilities for the churn prediction project.

This module provides functions to clean and prepare raw data for
feature engineering and modeling.
"""

import pandas as pd


def preprocess_data(df: pd.DataFrame, target_col: str = "Churn") -> pd.DataFrame:
    """
    Perform basic data cleaning and preprocessing for Telco churn dataset.

    This function handles common data quality issues in the Telco dataset:
    - Trims column names
    - Converts target variable to binary (0/1)
    - Fixes TotalCharges to numeric type
    - Handles missing values appropriately

    Args:
        df (pd.DataFrame): Raw input DataFrame.
        target_col (str): Name of the target column. Defaults to "Churn".

    Returns:
        pd.DataFrame: Preprocessed DataFrame ready for feature engineering.
    """
    # Clean column names by removing leading/trailing whitespace
    df.columns = df.columns.str.strip()

    # Convert target column to binary if it's categorical
    if target_col in df.columns and df[target_col].dtype == "object":
        df[target_col] = df[target_col].str.strip().map({"No": 0, "Yes": 1})

    # Convert TotalCharges to numeric (handles blank strings in dataset)
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # Ensure SeniorCitizen is integer type
    if "SeniorCitizen" in df.columns:
        df["SeniorCitizen"] = df["SeniorCitizen"].fillna(0).astype(int)

    # Handle missing values:
    # - Numeric columns: fill with 0
    # - Categorical columns: leave as NaN (encoders handle them safely)
    num_cols = df.select_dtypes(include=["number"]).columns
    df[num_cols] = df[num_cols].fillna(0)

    return df