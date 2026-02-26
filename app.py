import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile
import os
from datetime import datetime

st.set_page_config(page_title="Heart Disease Predictor", page_icon="❤️", layout="wide")

st.markdown("""
<style>
    .title-card {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(231,76,60,0.3);
    }
    .result-danger {
        background: linear-gradient(135deg, rgba(231,76,60,0.2), rgba(192,57,43,0.2));
        border: 2px solid #e74c3c;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
    }
    .result-safe {
        background: linear-gradient(135deg, rgba(46,204,113,0.2), rgba(39,174,96,0.2));
        border: 2px solid #2ecc71;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
    }
    .section-header {
        color: #e74c3c;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 1rem 0 0.5rem 0;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid rgba(231,76,60,0.3);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model = joblib.load('heart_disease_model.pkl')
    scaler = joblib.load('scaler.pkl')
    return model, scaler

model, scaler = load_model()

st.markdown("""
<div class="title-card">
    <h1 style="color:white; margin:0; font-size:2.5rem;">Heart Disease Predictor</h1>
    <p style="color:rgba(255,255,255,0.8); margin:0.5rem 0 0 0; font-size:1.1rem;">AI-powered heart health assessment using Random Forest</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Prediction", "BMI Calculator"])

with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Basic Info**")
        age = st.slider("Age", 20, 80, 50)
        sex = st.selectbox("Sex", options=[0,1], format_func=lambda x: "Female" if x==0 else "Male")
        cp = st.selectbox("Chest Pain Type", options=[0,1,2,3],
                          format_func=lambda x: {0:"Typical Angina",1:"Atypical Angina",2:"Non-anginal",3:"Asymptomatic"}[x])
        trestbps = st.slider("Resting Blood Pressure (mmHg)", 90, 200, 130)
        chol = st.slider("Cholesterol (mg/dl)", 100, 600, 246)

    with col2:
        st.markdown("**Blood & ECG**")
        fbs = st.selectbox("Fasting Blood Sugar > 120?", options=[0,1], format_func=lambda x: "No" if x==0 else "Yes")
        restecg = st.selectbox("Resting ECG", options=[0,1,2],
                               format_func=lambda x: {0:"Normal",1:"ST-T Abnormality",2:"LV Hypertrophy"}[x])
        thalach = st.slider("Max Heart Rate Achieved", 70, 210, 150)
        exang = st.selectbox("Exercise Induced Angina", options=[0,1], format_func=lambda x: "No" if x==0 else "Yes")

    with col3:
        st.markdown("**Advanced**")
        oldpeak = st.slider("ST Depression", 0.0, 6.5, 1.0, 0.1)
        slope = st.selectbox("Slope of ST Segment", options=[0,1,2],
                             format_func=lambda x: {0:"Upsloping",1:"Flat",2:"Downsloping"}[x])
        ca = st.selectbox("Major Vessels (0-4)", options=[0,1,2,3,4])
        thal = st.selectbox("Thalassemia", options=[0,1,2,3],
                            format_func=lambda x: {0:"Normal",1:"Fixed Defect",2:"Reversible Defect",3:"Unknown"}[x])

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Predict Heart Disease Risk", use_container_width=True, type="primary"):
        input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0]

        st.markdown("---")

        if prediction == 1:
            st.markdown(f"""
            <div class="result-danger">
                <h2 style="color:#e74c3c; margin:0;">High Risk Detected</h2>
                <p style="color:white; font-size:1.1rem;">Heart Disease er sombhabona ache</p>
                <h1 style="color:#e74c3c; margin:0;">{probability[1]*100:.1f}%</h1>
                <p style="color:rgba(255,255,255,0.7);">Risk Probability</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-safe">
                <h2 style="color:#2ecc71; margin:0;">Low Risk</h2>
                <p style="color:white; font-size:1.1rem;">Heart Disease er sombhabona nei</p>
                <h1 style="color:#2ecc71; margin:0;">{probability[0]*100:.1f}%</h1>
                <p style="color:rgba(255,255,255,0.7);">Healthy Probability</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_chart, col_explain = st.columns(2)

        with col_chart:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=probability[1]*100,
                title={'text': "Heart Disease Risk %", 'font': {'color': 'white'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': 'white'},
                    'bar': {'color': "#e74c3c" if prediction==1 else "#2ecc71"},
                    'steps': [
                        {'range': [0, 30], 'color': 'rgba(46,204,113,0.3)'},
                        {'range': [30, 60], 'color': 'rgba(241,196,15,0.3)'},
                        {'range': [60, 100], 'color': 'rgba(231,76,60,0.3)'}
                    ],
                    'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 50}
                },
                number={'font': {'color': 'white', 'size': 40}, 'suffix': '%'}
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white'},
                height=300,
                margin=dict(t=40, b=0, l=20, r=20)
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_explain:
            st.markdown("**Risk Factors Analysis:**")

            risk_factors = []
            positive_factors = []

            if age > 55:
                risk_factors.append("Age > 55 - High risk factor")
            if chol > 240:
                risk_factors.append("Cholesterol > 240 - Abnormally high")
            if trestbps > 140:
                risk_factors.append("Blood Pressure > 140 - High")
            if thalach < 120:
                risk_factors.append("Max Heart Rate < 120 - Low")
            if exang == 1:
                risk_factors.append("Exercise Angina present")
            if oldpeak > 2:
                risk_factors.append("ST Depression > 2 - Abnormal")

            if age <= 45:
                positive_factors.append("Age <= 45 - Good")
            if chol <= 200:
                positive_factors.append("Cholesterol normal")
            if trestbps <= 120:
                positive_factors.append("Blood Pressure normal")
            if thalach >= 150:
                positive_factors.append("Max Heart Rate good")

            if risk_factors:
                st.markdown("**Warning Signs:**")
                for r in risk_factors:
                    st.markdown(f"- {r}")

            if positive_factors:
                st.markdown("**Positive Signs:**")
                for p in positive_factors:
                    st.markdown(f"- {p}")

            if not risk_factors and not positive_factors:
                st.markdown("All parameters within normal range.")

        # Bar chart
        st.markdown("**Input Parameters Overview:**")
        param_names = ['Age', 'Sex', 'Chest Pain', 'BP', 'Cholesterol',
                       'Blood Sugar', 'ECG', 'Max HR', 'Ex. Angina', 'ST Dep',
                       'ST Slope', 'Vessels', 'Thal']
        param_values = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        ranges = [(20,80),(0,1),(0,3),(90,200),(100,600),(0,1),(0,2),(70,210),(0,1),(0,6.5),(0,2),(0,4),(0,3)]
        norm_vals = [(v - mn) / (mx - mn) * 100 for v, (mn, mx) in zip(param_values, ranges)]
        colors = ['#e74c3c' if n > 70 else '#f39c12' if n > 40 else '#2ecc71' for n in norm_vals]

        fig2 = go.Figure(go.Bar(
            x=param_names, y=norm_vals, marker_color=colors,
            text=[str(v) for v in param_values], textposition='outside',
            textfont={'color': 'white'}
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(20,20,40,0.5)',
            font={'color': 'white'},
            yaxis={'title': 'Normalized Value (%)', 'gridcolor': 'rgba(255,255,255,0.1)', 'color': 'white'},
            xaxis={'color': 'white'}, height=300, margin=dict(t=30, b=0, l=20, r=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

        # PDF
        st.markdown("**Download Report:**")

        def generate_pdf():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 20)
            pdf.set_text_color(231, 76, 60)
            pdf.cell(0, 15, "Heart Disease Prediction Report", ln=True, align="C")
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
            pdf.ln(5)
            pdf.set_fill_color(231, 76, 60) if prediction == 1 else pdf.set_fill_color(46, 204, 113)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 14)
            result_text = f"RESULT: {'HIGH RISK' if prediction==1 else 'LOW RISK - Healthy'}"
            pdf.cell(0, 12, result_text, ln=True, align="C", fill=True)
            pdf.ln(5)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", "B", 13)
            pdf.cell(0, 10, "Prediction Probability:", ln=True)
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(0, 8, f"  Healthy: {probability[0]*100:.1f}%", ln=True)
            pdf.cell(0, 8, f"  Heart Disease: {probability[1]*100:.1f}%", ln=True)
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 13)
            pdf.cell(0, 10, "Patient Parameters:", ln=True)
            pdf.set_font("Helvetica", "", 11)
            params = [
                ("Age", age), ("Sex", "Male" if sex==1 else "Female"),
                ("Chest Pain Type", cp), ("Resting Blood Pressure", f"{trestbps} mmHg"),
                ("Cholesterol", f"{chol} mg/dl"), ("Fasting Blood Sugar > 120", "Yes" if fbs==1 else "No"),
                ("Resting ECG", restecg), ("Max Heart Rate", thalach),
                ("Exercise Induced Angina", "Yes" if exang==1 else "No"),
                ("ST Depression", oldpeak), ("ST Slope", slope), ("Major Vessels", ca), ("Thalassemia", thal)
            ]
            for name, val in params:
                pdf.cell(95, 8, f"  {name}:", border=0)
                pdf.cell(95, 8, str(val), ln=True)
            pdf.ln(5)
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(150, 150, 150)
            pdf.multi_cell(0, 7, "DISCLAIMER: This is an AI-based prediction tool only. Always consult a qualified medical professional.")
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            pdf.output(tmp.name)
            return tmp.name

        try:
            pdf_path = generate_pdf()
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download PDF Report",
                    data=f.read(),
                    file_name=f"heart_disease_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            os.unlink(pdf_path)
        except Exception as e:
            st.warning(f"PDF error: {e}. Make sure 'fpdf2' is in requirements.txt")

        st.warning("This is an AI prediction only. Please consult a doctor for medical advice.")

with tab2:
    st.markdown("### BMI Calculator")
    col_bmi1, col_bmi2 = st.columns(2)

    with col_bmi1:
        height_cm = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        weight_kg = st.number_input("Weight (kg)", min_value=20, max_value=300, value=70)

        if st.button("Calculate BMI", use_container_width=True):
            height_m = height_cm / 100
            bmi = weight_kg / (height_m ** 2)

            if bmi < 18.5:
                category, color, advice = "Underweight", "#3498db", "Weight barano dorkar. Pushtikor khabar khan."
            elif bmi < 25:
                category, color, advice = "Normal Weight", "#2ecc71", "Apnar ojon swabhabik! Sustho jibonjapan chaliye jan."
            elif bmi < 30:
                category, color, advice = "Overweight", "#f39c12", "Ojon komano uchit. Niyomito byayam korun."
            else:
                category, color, advice = "Obese", "#e74c3c", "Ojon onek beshi. Doctorer poramorsh nin."

            with col_bmi2:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.05); border:2px solid {color}; border-radius:15px; padding:1.5rem; text-align:center;">
                    <h2 style="color:{color}; margin:0;">BMI: {bmi:.1f}</h2>
                    <h3 style="color:white; margin:0.5rem 0;">{category}</h3>
                    <p style="color:rgba(255,255,255,0.7);">{advice}</p>
                </div>
                """, unsafe_allow_html=True)

                fig_bmi = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=bmi,
                    title={'text': "BMI", 'font': {'color': 'white'}},
                    gauge={
                        'axis': {'range': [10, 45], 'tickcolor': 'white'},
                        'bar': {'color': color},
                        'steps': [
                            {'range': [10, 18.5], 'color': 'rgba(52,152,219,0.3)'},
                            {'range': [18.5, 25], 'color': 'rgba(46,204,113,0.3)'},
                            {'range': [25, 30], 'color': 'rgba(241,196,15,0.3)'},
                            {'range': [30, 45], 'color': 'rgba(231,76,60,0.3)'}
                        ]
                    },
                    number={'font': {'color': 'white', 'size': 40}}
                ))
                fig_bmi.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': 'white'}, height=280, margin=dict(t=40, b=0, l=20, r=20)
                )
                st.plotly_chart(fig_bmi, use_container_width=True)

    st.markdown("""
    | BMI Range | Category |
    |-----------|----------|
    | < 18.5 | Underweight |
    | 18.5 - 24.9 | Normal Weight |
    | 25 - 29.9 | Overweight |
    | >= 30 | Obese |
    """)
