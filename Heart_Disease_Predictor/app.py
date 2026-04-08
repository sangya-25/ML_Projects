import streamlit as st
import pandas as pd
import joblib
model=joblib.load('LR_heart_disease_model.pkl')
scaler=joblib.load('scaler.pkl')
columns=joblib.load('columns.pkl')

st.title("Heart Disease Predictor")
st.markdown("This is a simple heart disease predictor app built using Streamlit. It uses a logistic regression model to predict whether a person has heart disease or not based on the input features.")
age=st.slider("Age",21, 90, 40)
sex=st.selectbox("Sex", ["M", "F"])
chest_pain=st.selectbox("Chest Pain Type", ["ATA","NAP","TA","ASY"])
resting_bp=st.number_input("Resting Blood Pressure", 80, 200, 120)
cholesterol=st.number_input("Cholesterol", 100, 400, 200)
fasting_bs=st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0,1])
resting_ecg=st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
max_heart_rate=st.number_input("Max Heart Rate", 60, 220, 150)
exercise_angina=st.selectbox("Exercise Induced Angina", [0,1])
oldpeak=st.number_input("Oldpeak", 0.0, 10.0, 1.0)
st_slope=st.selectbox("ST Slope", ["Up", "Flat", "Down"])

if st.button("Predict"):
    input_data=pd.DataFrame([{
        'Age': age,
        'RestingBP': resting_bp,
        'Cholesterol': cholesterol,
        'FastingBS': fasting_bs,
        'MaxHR': max_heart_rate,
        'Oldpeak': oldpeak,
        'Sex_M': 1 if sex == "M" else 0,
        'ChestPainType_ATA': 1 if chest_pain == "ATA" else 0,
        'ChestPainType_NAP': 1 if chest_pain == "NAP" else 0,
        'ChestPainType_TA': 1 if chest_pain == "TA" else 0,
        'RestingECG_Normal': 1 if resting_ecg == "Normal" else 0,
        'RestingECG_ST': 1 if resting_ecg == "ST" else 0,
        'ExerciseAngina_Y': exercise_angina,
        'ST_Slope_Flat': 1 if st_slope == "Flat" else 0,
        'ST_Slope_Up': 1 if st_slope == "Up" else 0
    }])
    input_data = input_data.reindex(columns=columns, fill_value=0)
    numeric_cols = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']
    input_data[numeric_cols] = scaler.transform(input_data[numeric_cols])
    prediction = model.predict(input_data)
    if prediction[0] == 1:
        st.error("The model predicts that the person has heart disease.")
    else:
        st.success("The model predicts that the person does not have heart disease.")                