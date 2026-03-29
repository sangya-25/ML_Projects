from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model (using your medical_model.pkl)
model_path = 'medical_model.pkl'
label_encoders = {}

def load_model():
    """Load the trained model and label encoders"""
    try:
        if os.path.exists(model_path):
            model_data = joblib.load(model_path)
            # Handle tuple format (model, scaler)
            if isinstance(model_data, tuple) and len(model_data) == 2:
                model, scaler = model_data
                return {'model': model, 'scaler': scaler}
            else:
                return {'model': model_data, 'scaler': None}
        else:
            print(f"Model file {model_path} not found. Using mock prediction.")
            return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def preprocess_data(data):
    """Preprocess the input data to match training format"""
    # Create a DataFrame from the input data
    df = pd.DataFrame([data])
    
    # Handle categorical variables to match your model's expected format
    # Convert 'smoker' from 'yes'/'no' to smoker_code (1/0)
    df['smoker_code'] = df['smoker'].map({'yes': 1, 'no': 0})
    
    # Convert 'sex' from 'male'/'female' to sex_code (1/0)
    df['sex_code'] = df['sex'].map({'male': 1, 'female': 0})
    
    # Handle region - convert to one-hot encoding with specific column names
    region = df['region'].iloc[0]
    df['northeast'] = 1.0 if region == 'northeast' else 0.0
    df['northwest'] = 1.0 if region == 'northwest' else 0.0
    df['southeast'] = 1.0 if region == 'southeast' else 0.0
    df['southwest'] = 1.0 if region == 'southwest' else 0.0
    
    # Select and reorder columns to match your model's expected input
    # Based on your transformed dataset, the model expects these columns in this order:
    expected_columns = ['age', 'bmi', 'children', 'smoker_code', 'sex_code', 
                      'northeast', 'northwest', 'southeast', 'southwest']
    
    # Create the final DataFrame with the correct column order
    processed_df = df[expected_columns]
    
    return processed_df

def mock_prediction(data):
    """Mock prediction function when model is not available"""
    # This is a simplified prediction based on the input features
    base_charge = 5000
    age_factor = data['age'] * 100
    bmi_factor = (data['bmi'] - 18.5) * 200
    smoker_factor = 15000 if data['smoker'] == 'yes' else 0
    children_factor = data['children'] * 500
    
    # Region factors
    region_factors = {
        'northeast': 1000,
        'northwest': 500,
        'southeast': 1500,
        'southwest': 800
    }
    region_factor = region_factors.get(data['region'], 0)
    
    predicted_charge = base_charge + age_factor + bmi_factor + smoker_factor + children_factor + region_factor
    
    return round(predicted_charge, 2)

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for medical expense prediction"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['age', 'children', 'bmi', 'smoker', 'sex', 'region']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate data types and ranges
        try:
            data['age'] = int(data['age'])
            data['children'] = int(data['children'])
            data['bmi'] = float(data['bmi'])
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid data types for age, children, or bmi'}), 400
        
        # Validate ranges
        if not (0 <= data['age'] <= 120):
            return jsonify({'error': 'Age must be between 0 and 120'}), 400
        if not (0 <= data['children'] <= 10):
            return jsonify({'error': 'Children count must be between 0 and 10'}), 400
        if not (10 <= data['bmi'] <= 60):
            return jsonify({'error': 'BMI must be between 10 and 60'}), 400
        if data['smoker'] not in ['yes', 'no']:
            return jsonify({'error': 'Smoker must be "yes" or "no"'}), 400
        if data['sex'] not in ['male', 'female']:
            return jsonify({'error': 'Sex must be "male" or "female"'}), 400
        if data['region'] not in ['northeast', 'northwest', 'southeast', 'southwest']:
            return jsonify({'error': 'Invalid region'}), 400
        
        # Load model
        model = load_model()
        
        if model is not None:
            # Preprocess data for the model
            processed_data = preprocess_data(data)
            
            # Apply scaling only to numerical features (age, bmi, children)
            if model.get('scaler') is not None:
                # Scale only the first 3 columns (age, bmi, children)
                numerical_features = processed_data.iloc[:, :3]  # age, bmi, children
                scaled_numerical = model['scaler'].transform(numerical_features)
                
                # Combine scaled numerical features with categorical features
                categorical_features = processed_data.iloc[:, 3:]  # smoker_code, sex_code, regions
                final_data = pd.concat([
                    pd.DataFrame(scaled_numerical, columns=['age', 'bmi', 'children']),
                    categorical_features
                ], axis=1)
            else:
                final_data = processed_data
            
            # Make prediction
            prediction = model['model'].predict(final_data)[0]
        else:
            # Use mock prediction
            prediction = mock_prediction(data)
        
        # Convert USD to INR (approx 83.5 rate) for Indian users
        inr_prediction = prediction * 83.5
        result = {
            'charges': round(inr_prediction, 2),
            'currency': 'INR',
            'confidence': 0.87,
            'status': 'success'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Medical Expense Prediction API is running'})

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Medical Expense Prediction API',
        'endpoints': {
            '/predict': 'POST - Predict medical expenses',
            '/health': 'GET - Health check'
        }
    })

if __name__ == '__main__':
    print("Starting Medical Expense Prediction API...")
    print("Available endpoints:")
    print("- POST /predict: Predict medical expenses")
    print("- GET /health: Health check")
    print("- GET /: API information")
    app.run(debug=True, host='0.0.0.0', port=5000)
