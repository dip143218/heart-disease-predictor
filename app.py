import streamlit as st
import joblib
import numpy as np

st.set_page_config(page_title="Heart Disease Predictor", page_icon="❤️", layout="centered")

@st.cache_resource
def load_model():
    model = joblib.load('heart_disease_model.pkl')
    scaler = joblib.load('scaler.pkl')
    return model, scaler

model, scaler = load_model()

st.title("❤️ Heart Disease Predictor")
st.markdown("### Patient এর তথ্য দিন, AI predict করবে!")
st.divider()

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 20, 80, 50)
    sex = st.selectbox("Sex", options=[0,1], format_func=lambda x: "Female" if x==0 else "Male")
    cp = st.selectbox("Chest Pain Type", options=[0,1,2,3],
                      format_func=lambda x: {0:"0-Typical Angina",1:"1-Atypical Angina",2:"2-Non-anginal",3:"3-Asymptomatic"}[x])
    trestbps = st.slider("Resting Blood Pressure", 90, 200, 130)
    chol = st.slider("Cholesterol", 100, 600, 246)
    fbs = st.selectbox("Fasting Blood Sugar > 120?", options=[0,1], format_func=lambda x: "No" if x==0 else "Yes")
    restecg = st.selectbox("Resting ECG", options=[0,1,2])

with col2:
    thalach = st.slider("Max Heart Rate", 70, 210, 150)
    exang = st.selectbox("Exercise Induced Angina", options=[0,1], format_func=lambda x: "No" if x==0 else "Yes")
    oldpeak = st.slider("ST Depression", 0.0, 6.5, 1.0, 0.1)
    slope = st.selectbox("Slope of ST Segment", options=[0,1,2])
    ca = st.selectbox("Major Vessels (0-4)", options=[0,1,2,3,4])
    thal = st.selectbox("Thalassemia", options=[0,1,2,3],
                        format_func=lambda x: {0:"0-Normal",1:"1-Fixed Defect",2:"2-Reversible Defect",3:"3-Unknown"}[x])

st.divider()

if st.button("🔍 Predict Now", use_container_width=True, type="primary"):
    input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0]

    st.divider()
    if prediction == 1:
        st.error("## ⚠️ Heart Disease এর সম্ভাবনা আছে!")
    else:
        st.success("## ✅ Heart Disease এর সম্ভাবনা নেই!")

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("✅ Healthy", f"{probability[0]*100:.1f}%")
    with col_b:
        st.metric("⚠️ Heart Disease", f"{probability[1]*100:.1f}%")

    st.progress(float(probability[1]))
    st.warning("⚠️ এটি AI prediction, চূড়ান্ত সিদ্ধান্তের জন্য অবশ্যই ডাক্তারের পরামর্শ নিন।")
