import requests
import json

# Test the API with your specific input
test_data = {
    "age": 23,
    "sex": "female", 
    "bmi": 21,
    "children": 0,
    "smoker": "no",
    "region": "northwest"
}

try:
    response = requests.post('http://localhost:5000/predict', json=test_data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", e)
