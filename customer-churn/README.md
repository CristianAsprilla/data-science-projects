# Customer Churn Prediction

## 📌 Project Overview
This project predicts customer churn for a telecommunications company using machine learning. The goal is to identify customers likely to churn so the company can take proactive retention actions. The application is built with FastAPI for the backend API and Gradio for an interactive web UI.

**Business Context**: Customer churn is a critical metric for telecom companies, where retaining existing customers is often more cost-effective than acquiring new ones. This model helps identify at-risk customers based on their usage patterns, demographics, and service subscriptions.

## 📊 Dataset
- **Source**: [Telco Customer Churn Dataset on Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- **Size**: 7,043 rows, 21 columns
- **Features**: Includes demographics (gender, age, dependents), account info (tenure, contract type), and service usage (internet, phone, streaming services)
- **Target**: Churn (Yes/No)
- **Notes**: Dataset contains a mix of categorical and numerical features. Some preprocessing is required for data types and missing values.

## ⚙️ Methods
### Data Preprocessing
- Handled missing values and data type conversions (e.g., TotalCharges to numeric)
- Cleaned column names and standardized formats

### Feature Engineering
- Binary encoding for categorical features (gender, Partner, etc.)
- One-hot encoding for multi-category features (InternetService, Contract, etc.)
- Generated 7,072 features total after encoding

### Model
- **Algorithm**: XGBoost Classifier
- **Hyperparameters**: Optimized for imbalance (scale_pos_weight), n_estimators=301, max_depth=7, learning_rate=0.034
- **Training**: Stratified split (80/20), class imbalance handling

### Evaluation
- **Metrics**: Precision, Recall, F1-Score, ROC AUC
- **Performance**: F1 0.616, ROC AUC 0.837, Precision 0.49, Recall 0.83

## 📈 Results
- **Model Accuracy**: 72.5% on test set
- **Key Insights**:
  - High recall indicates good identification of churners
  - Features like tenure, contract type, and monthly charges are strong predictors
  - Customers with month-to-month contracts are more likely to churn
- **Business Impact**: Enables targeted retention campaigns, potentially reducing churn by identifying at-risk customers early

## 🚀 Installation and Usage

### Prerequisites
- Python 3.11+
- Docker (for containerized deployment)

### Local Development
1. **Clone the repository**:
   ```bash
   git clone https://github.com/CristianAsprilla/data-science-projects.git
   cd data-science-projects/customer-churn
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the training pipeline** (generates model artifacts):
   ```bash
   python pipelines/run_pipelines.py --input data/WA_Fn-UseC_-Telco-Customer-Churn.csv --target Churn
   ```

4. **Run the app locally**:
   ```bash
   python -m uvicorn src.app.main:app --host 0.0.0.0 --port 8000
   ```
   - API: http://localhost:8000/predict (POST with JSON data)
   - UI: http://localhost:8000/ui (Gradio interface)

### Docker Deployment
1. **Build the image**:
   ```bash
   docker build -t customer-churn-app .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 customer-churn-app
   ```

3. **Access**:
   - API: http://localhost:8000
   - UI: http://localhost:8000/ui

### CI/CD with GitHub Actions
This project uses GitHub Actions for automated building and pushing of Docker images to Docker Hub.

1. **Trigger the Workflow**:
   - Make changes to files in the `customer-churn/` directory.
   - Commit and push to the `main` branch.
   - The workflow will automatically build and push the image to Docker Hub.

2. **Required Secrets** (set in GitHub repository settings):
   - `DOCKERHUB_USERNAME`: Your Docker Hub username.
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token.

### Azure Deployment
The application is deployed to Azure App Service using the Docker image from Docker Hub.

1. **Access the Deployed App**:
   - URL: <https://customer-churn-app.azurewebsites.net>
   - API Endpoint: <https://customer-churn-app.azurewebsites.net/predict>
   - Gradio UI: <https://customer-churn-app.azurewebsites.net/ui>

2. **Update the Deployment**:
   - After pushing a new image via GitHub Actions, restart the Azure Web App:

     ```bash
     az webapp restart --name customer-churn-app --resource-group data-science-projects
     ```

3. **Azure Resources**:
   - Resource Group: `data-science-projects`
   - App Service Plan: `customer-churn-plan`
   - Web App: `customer-churn-app`

### API Usage
Send a POST request to `/predict` with customer data:

```json
{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "tenure": 1,
  "PhoneService": "No",
  "MultipleLines": "No phone service",
  "InternetService": "DSL",
  "OnlineSecurity": "No",
  "OnlineBackup": "Yes",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "No",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 29.85,
  "TotalCharges": 29.85
}
```

Response: `{"prediction": "Likely to churn"}`

## 🏗️ Project Structure

```text
customer-churn/
├── data/                    # Raw and processed datasets
├── pipelines/               # Training pipeline scripts
├── src/
│   ├── app/                 # FastAPI application
│   ├── data/                # Data loading and preprocessing
│   ├── models/              # Model training and evaluation
│   └── serving/             # Inference code
├── artifacts/               # Generated model artifacts (not in repo)
├── mlruns/                  # MLflow experiment logs (not in repo)
├── Dockerfile               # Container configuration
├── requirements.txt         # Python dependencies
└── README.md
```

## 🚀 Next Steps

- **Improvements**: Hyperparameter tuning with Optuna, feature selection, ensemble models
- **Extensions**: Real-time prediction API, A/B testing for retention strategies, integration with CRM systems
- **Deployment**: Kubernetes, cloud services (AWS SageMaker, GCP AI Platform)

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📞 Contact

- **Author**: Cristian Asprilla
- **GitHub**: [CristianAsprilla](https://github.com/CristianAsprilla)
- **Repository**: [data-science-projects](https://github.com/CristianAsprilla/data-science-projects)

<!-- Trigger workflow -->
Trigger change
