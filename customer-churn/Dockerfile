#FROM ubuntu:latest
#LABEL authors="cristian"
#
#ENTRYPOINT ["top", "-b"]
# 1. Use the official lightweight Python base image
FROM python:3.11-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy only dependency file first (for Docker caching)
COPY requirements.txt .

# 4. Install Python dependencies (add curl if you use MLflow local tracking URI)
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 5. Copy the entire project into the image (excluding artifacts)
COPY . .

# 6. Generate model artifacts by running the training pipeline
# Set environment variable to disable MLflow in CI/CD
# Force re-run by using a unique command each time
RUN echo "Starting model training..." && \
    CI=true python pipelines/run_pipelines.py \
    --input data/WA_Fn-UseC_-Telco-Customer-Churn.csv \
    --target Churn \
    --experiment "Docker Build" && \
    echo "Model training completed"

# 7. Verify artifacts were created
RUN ls -la artifacts/ && echo "Artifacts created successfully"

# make "serving" and "app" importable without the "src." prefix
# ensures logs are shown in real-time (no buffering).
# lets you import modules using from app... instead of from src.app....
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# 8. Expose FastAPI port
EXPOSE 8000

# 9. Run the FastAPI app using uvicorn (change path if needed)
CMD ["python", "-m", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]