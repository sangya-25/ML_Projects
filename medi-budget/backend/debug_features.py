import joblib
import pandas as pd

# Load the model and check what features it expects
model_path = 'medical_model.pkl'

try:
    model_data = joblib.load(model_path)
    if isinstance(model_data, tuple) and len(model_data) == 2:
        model, scaler = model_data
        print("Model loaded successfully!")
        print(f"Model type: {type(model)}")
        print(f"Scaler type: {type(scaler)}")
        
        # Check if the model has feature names
        if hasattr(model, 'feature_names_in_'):
            print(f"Model expects features: {model.feature_names_in_}")
        else:
            print("Model doesn't have feature_names_in_ attribute")
            
        # Check if the scaler has feature names
        if hasattr(scaler, 'feature_names_in_'):
            print(f"Scaler expects features: {scaler.feature_names_in_}")
        else:
            print("Scaler doesn't have feature_names_in_ attribute")
            
        # Check the number of features expected
        if hasattr(model, 'n_features_in_'):
            print(f"Model expects {model.n_features_in_} features")
        else:
            print("Model doesn't have n_features_in_ attribute")
            
        # Check scaler feature count
        if hasattr(scaler, 'n_features_in_'):
            print(f"Scaler expects {scaler.n_features_in_} features")
        else:
            print("Scaler doesn't have n_features_in_ attribute")
            
except Exception as e:
    print(f"Error: {e}")
