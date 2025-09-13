import streamlit as st

"""
Streamlit App: Fraud Detection Demo
-----------------------------------
This simple web app lets you play with a trained fraud detection model. Enter a few transaction details and see if the model thinks it's legit or suspicious.

Author: Cristian Asprilla
"""

import streamlit as st
import pickle
import pandas as pd

# --- Load the trained model ---
# Make sure the model path is correct!
model = pickle.load(open('../models/fraud_model.pkl', 'rb'))

st.title("Fraud Detection Demo")
st.write("""
Curious if a transaction might be flagged as fraud? Tweak the values below and see what the model predicts.
This is a first version, so don't use it for real banking decisions!
""")

# --- User Inputs ---
transaction_amount = st.number_input("Transaction Amount", min_value=0.0, value=100.0)
device = st.selectbox("Device Used", ["Mobile", "Desktop", "Tablet"])
account_age = st.number_input("Account Age (days)", min_value=0, value=60)

def preprocess_input(amount, device, age):
    """
    Prepare a single transaction for prediction.
    (In a real app, you'd want to match this to your model's training pipeline.)
    """
    input_data = {
        'User_ID': 0,  # Placeholder
        'Transaction_Amount': amount,
        'Time_of_Transaction': 12,  # Noon as a default
        'Previous_Fraudulent_Transactions': 0,
        'Account_Age': age,
        'Number_of_Transactions_Last_24H': 1,
        'Is_Mobile': 1 if device == 'Mobile' else 0,
        'Is_Tablet': 1 if device == 'Tablet' else 0,
        'Is_Desktop': 1 if device == 'Desktop' else 0,
        'Is_New_Account': 1 if age < 30 else 0,
        'New_Account_And_Tablet': 1 if (age < 30 and device == 'Tablet') else 0,
        'Transaction_Hour': 12,
        'Avg_Transaction_Amount_Past_24H': amount,
        'User_Avg_Amount': amount,
        'Amount_Ratio_To_Avg': 1.0,
        # For demo: assume online purchase, credit card, LA
        'Transaction_Type_ATM Withdrawal': 0,
        'Transaction_Type_Bank Transfer': 0,
        'Transaction_Type_Bill Payment': 0,
        'Transaction_Type_Online Purchase': 1,
        'Transaction_Type_POS Payment': 0,
        'Device_Used_Desktop': 1 if device == 'Desktop' else 0,
        'Device_Used_Mobile': 1 if device == 'Mobile' else 0,
        'Device_Used_Tablet': 1 if device == 'Tablet' else 0,
        'Device_Used_Unknown Device': 0,
        'Location_Boston': 0,
        'Location_Chicago': 0,
        'Location_Houston': 0,
        'Location_Los Angeles': 1,
        'Location_Miami': 0,
        'Location_New York': 0,
        'Location_San Francisco': 0,
        'Location_Seattle': 0,
        'Payment_Method_Credit Card': 1,
        'Payment_Method_Debit Card': 0,
        'Payment_Method_Invalid Method': 0,
        'Payment_Method_Net Banking': 0,
        'Payment_Method_UPI': 0
    }
    return pd.DataFrame([input_data])


# --- Prediction ---
if st.button("Predict Fraud"):
    input_data = preprocess_input(transaction_amount, device, account_age)
    prediction = model.predict(input_data)
    if prediction[0] == 1:
        st.error("⚠️ This transaction looks suspicious! (Fraudulent)")
    else:
        st.success("✅ This transaction looks legitimate.")
