"""
FastAPI application for Telco Customer Churn Prediction.

This module provides both a REST API and a Gradio web UI for predicting
customer churn based on customer data. The prediction logic is handled
by the inference module.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import gradio as gr
import os
import sys

# Ensure we can import from src/serving when running "uvicorn src.app.app:app"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from serving.inference import predict  # our single source of truth for inference

app = FastAPI(title="Telco Churn Predictor", description="API for predicting customer churn")

@app.get("/")
def root():
    """
    Health check endpoint.

    Returns:
        dict: Status message indicating the API is running.
    """
    return {"status": "ok"}

# Request schema (same fields you collect in the UI)
class CustomerData(BaseModel):
    """
    Pydantic model for customer data input.

    Attributes:
        gender (str): Customer's gender.
        Partner (str): Whether the customer has a partner.
        Dependents (str): Whether the customer has dependents.
        PhoneService (str): Whether the customer has phone service.
        MultipleLines (str): Multiple lines status.
        InternetService (str): Type of internet service.
        OnlineSecurity (str): Online security status.
        OnlineBackup (str): Online backup status.
        DeviceProtection (str): Device protection status.
        TechSupport (str): Tech support status.
        StreamingTV (str): Streaming TV status.
        StreamingMovies (str): Streaming movies status.
        Contract (str): Contract type.
        PaperlessBilling (str): Paperless billing preference.
        PaymentMethod (str): Payment method.
        tenure (int): Number of months as customer.
        MonthlyCharges (float): Monthly charges.
        TotalCharges (float): Total charges.
    """
    gender: str
    Partner: str
    Dependents: str
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    tenure: int
    MonthlyCharges: float
    TotalCharges: float

@app.post("/predict")
def api_predict(data: CustomerData):
    """
    Predict churn for a single customer via REST API.

    Args:
        data (CustomerData): Customer data for prediction.

    Returns:
        dict: Prediction result or error message.
    """
    try:
        out = predict(data.dict())
        return {"prediction": out}
    except Exception as e:
        return {"error": str(e)}

# --- Gradio UI wrappers the same predict() ---
def gradio_interface(
    gender, Partner, Dependents, PhoneService, MultipleLines,
    InternetService, OnlineSecurity, OnlineBackup, DeviceProtection,
    TechSupport, StreamingTV, StreamingMovies, Contract,
    PaperlessBilling, PaymentMethod, tenure, MonthlyCharges, TotalCharges
):
    """
    Gradio interface function for churn prediction.

    Args:
        gender (str): Customer's gender.
        Partner (str): Whether the customer has a partner.
        Dependents (str): Whether the customer has dependents.
        PhoneService (str): Whether the customer has phone service.
        MultipleLines (str): Multiple lines status.
        InternetService (str): Type of internet service.
        OnlineSecurity (str): Online security status.
        OnlineBackup (str): Online backup status.
        DeviceProtection (str): Device protection status.
        TechSupport (str): Tech support status.
        StreamingTV (str): Streaming TV status.
        StreamingMovies (str): Streaming movies status.
        Contract (str): Contract type.
        PaperlessBilling (str): Paperless billing preference.
        PaymentMethod (str): Payment method.
        tenure (int): Number of months as customer.
        MonthlyCharges (float): Monthly charges.
        TotalCharges (float): Total charges.

    Returns:
        str: Prediction result.
    """
    payload = {
        "gender": gender,
        "Partner": Partner,
        "Dependents": Dependents,
        "PhoneService": PhoneService,
        "MultipleLines": MultipleLines,
        "InternetService": InternetService,
        "OnlineSecurity": OnlineSecurity,
        "OnlineBackup": OnlineBackup,
        "DeviceProtection": DeviceProtection,
        "TechSupport": TechSupport,
        "StreamingTV": StreamingTV,
        "StreamingMovies": StreamingMovies,
        "Contract": Contract,
        "PaperlessBilling": PaperlessBilling,
        "PaymentMethod": PaymentMethod,
        "tenure": int(tenure),
        "MonthlyCharges": float(MonthlyCharges),
        "TotalCharges": float(TotalCharges),
    }
    out = predict(payload)
    return str(out)

# Create Gradio interface
demo = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Dropdown(["Male", "Female"], label="Gender"),
        gr.Dropdown(["Yes", "No"], label="Partner"),
        gr.Dropdown(["Yes", "No"], label="Dependents"),
        gr.Dropdown(["Yes", "No"], label="Phone Service"),
        gr.Dropdown(["Yes", "No", "No phone service"], label="Multiple Lines"),
        gr.Dropdown(["DSL", "Fiber optic", "No"], label="Internet Service"),
        gr.Dropdown(["Yes", "No", "No internet service"], label="Online Security"),
        gr.Dropdown(["Yes", "No", "No internet service"], label="Online Backup"),
        gr.Dropdown(["Yes", "No", "No internet service"], label="Device Protection"),
        gr.Dropdown(["Yes", "No", "No internet service"], label="Tech Support"),
        gr.Dropdown(["Yes", "No", "No internet service"], label="Streaming TV"),
        gr.Dropdown(["Yes", "No", "No internet service"], label="Streaming Movies"),
        gr.Dropdown(["Month-to-month", "One year", "Two year"], label="Contract"),
        gr.Dropdown(["Yes", "No"], label="Paperless Billing"),
        gr.Dropdown(
            ["Electronic check", "Mailed check",
             "Bank transfer (automatic)", "Credit card (automatic)"],
            label="Payment Method"
        ),
        gr.Number(label="Tenure (months)"),
        gr.Number(label="Monthly Charges"),
        gr.Number(label="Total Charges"),
    ],
    outputs="text",
    title="Telco Churn Predictor",
    description="Fill in the customer details to get a churn prediction.",
)

# Mount Gradio app on FastAPI
app = gr.mount_gradio_app(app, demo, path="/ui")