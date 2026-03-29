# Medical Expense Prediction API

A Flask backend API for predicting medical expenses using machine learning.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Place your trained model file as `model.pkl` in the backend directory

3. Run the API:
```bash
python app.py
```

## API Endpoints

### POST /predict
Predict medical expenses based on input data.

**Request Body:**
```json
{
  "age": 23,
  "children": 0,
  "bmi": 19.9,
  "smoker": "no",
  "sex": "female",
  "region": "northeast"
}
```

**Response:**
```json
{
  "charges": 12345.67,
  "currency": "USD",
  "confidence": 0.87,
  "status": "success"
}
```

### GET /health
Health check endpoint.

### GET /
API information and available endpoints.

## Model Integration

To use your trained model:
1. Save your trained scikit-learn model as `model.pkl` using `joblib.dump()`
2. Place the file in the backend directory
3. The API will automatically load and use your model

If no model file is found, the API will use a mock prediction function.
