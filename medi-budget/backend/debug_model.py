import joblib
import os

# Debug the model file
model_path = 'medical_model.pkl'

if os.path.exists(model_path):
    print(f"Model file exists: {model_path}")
    print(f"File size: {os.path.getsize(model_path)} bytes")
    
    try:
        model = joblib.load(model_path)
        print(f"Model type: {type(model)}")
        print(f"Model attributes: {dir(model)}")
        
        # Check if it's a tuple (common when saving multiple objects)
        if isinstance(model, tuple):
            print(f"Model is a tuple with {len(model)} elements")
            for i, item in enumerate(model):
                print(f"Element {i}: {type(item)} - {dir(item)}")
        else:
            print(f"Model object: {model}")
            
    except Exception as e:
        print(f"Error loading model: {e}")
else:
    print(f"Model file not found: {model_path}")
