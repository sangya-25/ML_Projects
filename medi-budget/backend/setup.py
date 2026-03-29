#!/usr/bin/env python3
"""
Setup script for Medical Expense Prediction API
This script helps you prepare your trained model for the API
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def create_sample_model():
    """Create a sample model if you don't have one yet"""
    print("Creating sample model...")
    
    # Generate sample data similar to medical.csv
    np.random.seed(42)
    n_samples = 1000
    
    # Generate sample data
    data = {
        'age': np.random.randint(18, 65, n_samples),
        'sex': np.random.choice(['male', 'female'], n_samples),
        'bmi': np.random.normal(28, 6, n_samples),
        'children': np.random.randint(0, 6, n_samples),
        'smoker': np.random.choice(['yes', 'no'], n_samples, p=[0.2, 0.8]),
        'region': np.random.choice(['northeast', 'northwest', 'southeast', 'southwest'], n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Create target variable (charges) with realistic relationships
    base_charge = 10000
    age_factor = df['age'] * 200
    bmi_factor = (df['bmi'] - 18.5) * 300
    smoker_factor = df['smoker'].map({'yes': 15000, 'no': 0})
    children_factor = df['children'] * 1000
    region_factor = df['region'].map({
        'northeast': 2000,
        'northwest': 1000,
        'southeast': 3000,
        'southwest': 1500
    })
    
    # Add some noise
    noise = np.random.normal(0, 2000, n_samples)
    
    df['charges'] = (base_charge + age_factor + bmi_factor + 
                    smoker_factor + children_factor + region_factor + noise)
    
    # Ensure charges are positive
    df['charges'] = np.maximum(df['charges'], 1000)
    
    return df

def prepare_model_data(df):
    """Prepare data for model training"""
    # Create a copy for processing
    model_df = df.copy()
    
    # Convert categorical variables
    model_df['smoker'] = model_df['smoker'].map({'yes': 1, 'no': 0})
    model_df['sex'] = model_df['sex'].map({'male': 1, 'female': 0})
    
    # Create dummy variables for region
    region_dummies = pd.get_dummies(model_df['region'], prefix='region')
    model_df = pd.concat([model_df, region_dummies], axis=1)
    model_df = model_df.drop('region', axis=1)
    
    return model_df

def train_model(df):
    """Train a linear regression model"""
    print("Training model...")
    
    # Prepare features and target
    feature_columns = ['age', 'children', 'bmi', 'smoker', 'sex', 
                      'region_northeast', 'region_northwest', 'region_southeast', 'region_southwest']
    X = df[feature_columns]
    y = df['charges']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluate model
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"Training R² score: {train_score:.4f}")
    print(f"Test R² score: {test_score:.4f}")
    
    return model

def save_model(model, filename='model.pkl'):
    """Save the trained model"""
    joblib.dump(model, filename)
    print(f"Model saved as {filename}")

def main():
    """Main setup function"""
    print("Medical Expense Prediction API Setup")
    print("=" * 40)
    
    # Check if model already exists
    if os.path.exists('model.pkl'):
        print("Model file already exists!")
        response = input("Do you want to recreate it? (y/n): ")
        if response.lower() != 'y':
            print("Setup complete. Using existing model.")
            return
    
    # Create sample data and model
    df = create_sample_model()
    model_df = prepare_model_data(df)
    model = train_model(model_df)
    save_model(model)
    
    print("\nSetup complete!")
    print("You can now run the API with: python app.py")
    print("\nTo use your own model:")
    print("1. Train your model using your medical.csv data")
    print("2. Save it as 'model.pkl' using joblib.dump()")
    print("3. Replace the current model.pkl file")

if __name__ == "__main__":
    main()
