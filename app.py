import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go

# Load model files
@st.cache_resource
def load_model():
    model = joblib.load('heart_model.pkl')
    scaler = joblib.load('scaler.pkl')
    feature_medians = joblib.load('feature_medians.pkl')
    feature_names = joblib.load('feature_names.pkl')
    return model, scaler, feature_medians, feature_names

model, scaler, feature_medians, feature_names = load_model()

# Page config
st.set_page_config(page_title="Heart Disease Predictor", page_icon="❤️", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stApp { background-color: #0e1117; }
    .title-text { 
        font-size: 2.5rem; 
        font-weight: bold; 
        text-align: center;
        background: linear-gradient(90deg, #ff4b4b, #ff8c8c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .subtitle-text {
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
    }
    .required-badge {
        background-color: #ff4b4b;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75rem;
        margin-left: 5px;
    }
    .optional-badge {
        background-color: #1f77b4;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75rem;
        margin-left: 5px;
    }
    .result-card {
        background: linear-gradient(135deg, #1e1e2e, #2d2d44);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #444;
    }
    .metric-card {
        background: #1e1e2e;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid #333;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title-text">❤️ Heart Disease Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">AI-powered heart disease risk assessment using clinical parameters</div>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar info
with st.sidebar:
    st.markdown("## ℹ️ About")
    st.markdown("""
    This tool uses a **Random Forest** model trained on clinical heart disease data.
    
    **Model Performance:**
    - AUC-ROC: 0.866
    - Dataset: Heart Failure Prediction
    - Algorithm: Random Forest
    
    **Required fields** must be filled for prediction.
    **Optional fields** improve accuracy if available.
    """)
    st.markdown("---")
    st.warning("⚠️ This tool is for informational purposes only. Always consult a medical professional.")

# Input Section
st.markdown("## 📋 Patient Information")

# Required fields
st.markdown("### 🔴 Required Fields")
col1, col2, col3, col4 = st.columns(4)

with col1:
    age = st.number_input("🎂 Age (years)", min_value=1, max_value=120, value=50)

with col2:
    sex = st.selectbox("⚧ Sex", options=[1, 0], format_func=lambda x: "Male" if x == 1 else "Female")

with col3:
    chest_pain = st.selectbox("💔 Chest Pain Type", options=[0, 1, 2, 3],
                               format_func=lambda x: {
                                   0: "Typical Angina",
                                   1: "Atypical Angina", 
                                   2: "Non-Anginal Pain",
                                   3: "Asymptomatic"
                               }[x])

with col4:
    fasting_bs = st.selectbox("🩸 Fasting Blood Sugar > 120", options=[0, 1],
                               format_func=lambda x: "Yes" if x == 1 else "No")

col5, col6, col7 = st.columns(3)

with col5:
    blood_pressure = st.number_input("💊 Resting BP (mmHg)", min_value=50, max_value=250, value=130)

with col6:
    cholesterol = st.number_input("🧪 Cholesterol (mg/dL)", min_value=0, max_value=700, value=223)

with col7:
    max_hr = st.number_input("💓 Max Heart Rate", min_value=50, max_value=250, value=138)

st.markdown("---")

# Optional fields
st.markdown("### 🔵 Optional Fields (improves accuracy)")
with st.expander("➕ Add Optional Information"):
    opt_col1, opt_col2, opt_col3 = st.columns(3)
    
    with opt_col1:
        exercise_angina = st.selectbox("🏃 Exercise Angina", 
                                        options=[None, 0, 1],
                                        format_func=lambda x: "Not provided" if x is None else ("Yes" if x == 1 else "No"))
        oldpeak = st.number_input("📉 ST Depression (Oldpeak)", min_value=-5.0, max_value=10.0, value=0.0, step=0.1)
        use_oldpeak = st.checkbox("Include ST Depression")

    with opt_col2:
        st_slope = st.selectbox("📈 ST Slope",
                                  options=[None, 0, 1, 2],
                                  format_func=lambda x: "Not provided" if x is None else {0:"Down", 1:"Flat", 2:"Up"}[x])
        
    with opt_col3:
        resting_ecg = st.selectbox("📊 Resting ECG",
                                    options=[None, 0, 1, 2],
                                    format_func=lambda x: "Not provided" if x is None else {0:"Normal", 1:"ST Abnormality", 2:"LV Hypertrophy"}[x])

st.markdown("---")

# Predict Button
predict_btn = st.button("🔍 Predict Heart Disease Risk", use_container_width=True, type="primary")

if predict_btn:
    # Build input with required fields
    input_data = {
        'age': age,
        'sex': sex,
        'cholesterol': cholesterol,
        'blood_pressure': blood_pressure,
        'max_hr': max_hr,
        'chest_pain': chest_pain,
        'fasting_bs': fasting_bs
    }

    # Fill missing with median
    missing_fields = []
    input_values = []
    for feature in feature_names:
        if feature in input_data:
            input_values.append(input_data[feature])
        else:
            input_values.append(feature_medians[feature])
            missing_fields.append(feature)

    if missing_fields:
        st.warning(f"⚠️ Some fields filled with average values: {', '.join(missing_fields)}. Results may be less accurate.")

    # Predict
    input_array = np.array(input_values).reshape(1, -1)
    input_scaled = scaler.transform(input_array)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]
    risk_percent = probability * 100

    # Risk level
    if risk_percent >= 70:
        risk_level = "High"
        risk_color = "#ff4b4b"
        risk_emoji = "🔴"
    elif risk_percent >= 40:
        risk_level = "Medium"
        risk_color = "#ffa500"
        risk_emoji = "🟡"
    else:
        risk_level = "Low"
        risk_color = "#00cc44"
        risk_emoji = "🟢"

    st.markdown("---")
    st.markdown("## 📊 Prediction Results")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Diagnosis", "Heart Disease" if prediction == 1 else "No Heart Disease",
                  delta="Positive" if prediction == 1 else "Negative")
    with col2:
        st.metric("Risk Probability", f"{risk_percent:.1f}%")
    with col3:
        st.metric("Risk Level", f"{risk_emoji} {risk_level}")
    with col4:
        st.metric("Confidence", f"{max(probability, 1-probability)*100:.1f}%")

    # Gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_percent,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Heart Disease Risk (%)", 'font': {'size': 20, 'color': 'white'}},
        delta={'reference': 50, 'font': {'size': 14}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white", 'tickfont': {'color': 'white'}},
            'bar': {'color': risk_color},
            'bgcolor': "#1e1e2e",
            'borderwidth': 2,
            'bordercolor': "#444",
            'steps': [
                {'range': [0, 40], 'color': '#1a3a1a'},
                {'range': [40, 70], 'color': '#3a2e00'},
                {'range': [70, 100], 'color': '#3a0000'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': risk_percent
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

    # Feature importance display
    st.markdown("### 📌 Input Summary")
    summary_col1, summary_col2 = st.columns(2)
    with summary_col1:
        st.markdown(f"- **Age:** {age} years")
        st.markdown(f"- **Sex:** {'Male' if sex == 1 else 'Female'}")
        st.markdown(f"- **Chest Pain:** {['Typical Angina','Atypical Angina','Non-Anginal','Asymptomatic'][chest_pain]}")
        st.markdown(f"- **Blood Pressure:** {blood_pressure} mmHg")
    with summary_col2:
        st.markdown(f"- **Cholesterol:** {cholesterol} mg/dL")
        st.markdown(f"- **Max Heart Rate:** {max_hr} bpm")
        st.markdown(f"- **Fasting Blood Sugar > 120:** {'Yes' if fasting_bs == 1 else 'No'}")

    st.markdown("---")

    # Advice
    if prediction == 1:
        st.error("""
        ### ⚠️ High Risk Detected
        Based on the provided information, there are indicators of potential heart disease.
        
        **Recommended Actions:**
        - Consult a cardiologist immediately
        - Get a comprehensive cardiac evaluation
        - Monitor blood pressure and cholesterol regularly
        - Adopt heart-healthy lifestyle changes
        """)
    else:
        st.success("""
        ### ✅ Low Risk Detected
        Based on the provided information, the risk of heart disease appears to be low.
        
        **Maintain Your Health:**
        - Continue regular exercise
        - Maintain a balanced diet
        - Regular health check-ups
        - Avoid smoking and excessive alcohol
        """)

    st.caption("⚠️ This prediction is based on AI analysis and should not replace professional medical advice.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#555; padding: 1rem;'>
    Built with ❤️ using Streamlit & Random Forest Classifier<br>
    Dataset: Heart Failure Prediction | AUC-ROC: 0.866
</div>
""", unsafe_allow_html=True)
