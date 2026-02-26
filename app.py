import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile
import os
from datetime import datetime

st.set_page_config(page_title="HealthAI by Morsalin", page_icon="❤️", layout="wide")

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #f0ece4;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }

/* ── LANDING ── */
.landing-wrap {
    min-height: 100vh;
    background: radial-gradient(ellipse at 20% 50%, #1a0a2e 0%, #0a0a0f 60%),
                radial-gradient(ellipse at 80% 20%, #200a1a 0%, transparent 50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.landing-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        radial-gradient(circle at 15% 85%, rgba(180,30,60,0.12) 0%, transparent 40%),
        radial-gradient(circle at 85% 15%, rgba(100,20,160,0.10) 0%, transparent 40%);
    pointer-events: none;
}
.grid-bg {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
}
.landing-badge {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c0507a;
    background: rgba(192,80,122,0.12);
    border: 1px solid rgba(192,80,122,0.3);
    padding: 0.4rem 1.2rem;
    border-radius: 100px;
    margin-bottom: 2rem;
}
.landing-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(3rem, 7vw, 5.5rem);
    font-weight: 900;
    line-height: 1.05;
    text-align: center;
    margin-bottom: 1.2rem;
    background: linear-gradient(135deg, #f0ece4 30%, #c0507a 70%, #7b2ff7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.landing-sub {
    font-size: 1.1rem;
    font-weight: 300;
    color: rgba(240,236,228,0.55);
    text-align: center;
    max-width: 480px;
    line-height: 1.7;
    margin-bottom: 3.5rem;
}

/* Hearts container */
.hearts-row {
    display: flex;
    gap: 2.5rem;
    justify-content: center;
    align-items: stretch;
    margin-bottom: 3.5rem;
    flex-wrap: wrap;
}
.heart-card {
    width: 280px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 2.5rem 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.35s cubic-bezier(0.34,1.56,0.64,1);
    position: relative;
    overflow: hidden;
    text-decoration: none;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.heart-card::before {
    content: '';
    position: absolute;
    inset: 0;
    opacity: 0;
    transition: opacity 0.35s ease;
    border-radius: 24px;
}
.heart-card:hover { transform: translateY(-8px) scale(1.02); }
.heart-card:hover::before { opacity: 1; }

.card-healthy::before { background: linear-gradient(135deg, rgba(46,180,100,0.12), rgba(20,120,60,0.08)); }
.card-healthy { border-color: rgba(46,180,100,0.25); }
.card-healthy:hover { border-color: rgba(46,180,100,0.6); box-shadow: 0 20px 60px rgba(46,180,100,0.2); }

.card-damaged::before { background: linear-gradient(135deg, rgba(220,50,80,0.15), rgba(150,20,40,0.08)); }
.card-damaged { border-color: rgba(220,50,80,0.25); }
.card-damaged:hover { border-color: rgba(220,50,80,0.6); box-shadow: 0 20px 60px rgba(220,50,80,0.2); }

.card-bmi::before { background: linear-gradient(135deg, rgba(100,120,255,0.15), rgba(60,80,200,0.08)); }
.card-bmi { border-color: rgba(100,120,255,0.25); }
.card-bmi:hover { border-color: rgba(100,120,255,0.6); box-shadow: 0 20px 60px rgba(100,120,255,0.2); }

.heart-svg { width: 90px; height: 90px; margin-bottom: 1.5rem; }
.card-label {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.6rem;
    color: #f0ece4;
}
.card-desc {
    font-size: 0.85rem;
    color: rgba(240,236,228,0.45);
    line-height: 1.6;
}
.card-arrow {
    margin-top: 1.5rem;
    font-size: 1.4rem;
    opacity: 0.4;
    transition: opacity 0.3s, transform 0.3s;
}
.heart-card:hover .card-arrow { opacity: 1; transform: translateX(4px); }

.landing-footer {
    font-size: 0.78rem;
    color: rgba(240,236,228,0.25);
    letter-spacing: 0.08em;
}
.landing-footer span { color: rgba(192,80,122,0.7); }

/* ── PAGE WRAPPERS ── */
.page-wrap {
    min-height: 100vh;
    padding: 2.5rem 2rem 4rem;
    position: relative;
}
.page-heart {
    background: linear-gradient(160deg, #0d0010 0%, #0a0a0f 40%, #130008 100%);
}
.page-bmi {
    background: linear-gradient(160deg, #00001a 0%, #0a0a0f 40%, #050018 100%);
}
.page-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
}

.back-btn-wrap { margin-bottom: 2rem; position: relative; z-index: 1; }

.page-header {
    text-align: center;
    margin-bottom: 3rem;
    position: relative;
    z-index: 1;
}
.page-eyebrow {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.eyebrow-red { color: #c0507a; }
.eyebrow-blue { color: #6478ff; }

.page-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}
.title-red { background: linear-gradient(135deg, #f0ece4, #e05070); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.title-blue { background: linear-gradient(135deg, #f0ece4, #6478ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

.page-byline {
    font-size: 0.85rem;
    color: rgba(240,236,228,0.35);
    letter-spacing: 0.06em;
}

/* Form panels */
.form-panel {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 1.8rem 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    z-index: 1;
}
.panel-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(240,236,228,0.35);
    margin-bottom: 1.2rem;
}

/* Result cards */
.res-high {
    background: linear-gradient(135deg, rgba(220,50,80,0.15), rgba(150,20,40,0.1));
    border: 1.5px solid rgba(220,50,80,0.5);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin: 1.5rem 0;
}
.res-low {
    background: linear-gradient(135deg, rgba(46,180,100,0.15), rgba(20,120,60,0.1));
    border: 1.5px solid rgba(46,180,100,0.5);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin: 1.5rem 0;
}
.res-title { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 700; margin: 0 0 0.3rem; }
.res-sub { font-size: 0.9rem; color: rgba(240,236,228,0.6); margin: 0 0 1rem; }
.res-pct { font-family: 'Playfair Display', serif; font-size: 3.5rem; font-weight: 900; margin: 0; }

/* stButton overrides */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #b03060, #7b2ff7) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(176,48,96,0.35) !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(176,48,96,0.5) !important;
}

/* slider / selectbox theming */
[data-testid="stSlider"] > div > div > div { background: rgba(176,48,96,0.6) !important; }
label[data-testid="stWidgetLabel"] > div { color: rgba(240,236,228,0.7) !important; font-size: 0.85rem !important; }
[data-testid="stSelectbox"] > div > div { background: rgba(255,255,255,0.04) !important; border-color: rgba(255,255,255,0.1) !important; color: #f0ece4 !important; border-radius: 10px !important; }
[data-testid="stNumberInput"] input { background: rgba(255,255,255,0.04) !important; border-color: rgba(255,255,255,0.1) !important; color: #f0ece4 !important; border-radius: 10px !important; }

div[data-testid="stTabs"] [data-testid="stMarkdownContainer"] { display: none; }

/* download button */
div[data-testid="stDownloadButton"] > button {
    background: rgba(46,180,100,0.15) !important;
    color: #2eb464 !important;
    border: 1px solid rgba(46,180,100,0.4) !important;
    box-shadow: none !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: rgba(46,180,100,0.25) !important;
    box-shadow: 0 4px 20px rgba(46,180,100,0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "landing"

# ── Model loader ──────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model = joblib.load('heart_disease_model.pkl')
    scaler = joblib.load('scaler.pkl')
    return model, scaler

model, scaler = load_model()

# ════════════════════════════════════════════════════════════════
# LANDING PAGE
# ════════════════════════════════════════════════════════════════
if st.session_state.page == "landing":

    st.markdown("""
    <div class="landing-wrap">
        <div class="grid-bg"></div>
        <div class="landing-badge">AI Health Platform</div>
        <h1 class="landing-title">Know Your Heart.<br>Know Your Body.</h1>
        <p class="landing-sub">Advanced machine-learning tools to assess cardiovascular risk and body composition — designed for everyone.</p>
    </div>
    """, unsafe_allow_html=True)

    col_space1, col1, col2, col_space2 = st.columns([1, 2, 2, 1])

    with col1:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(46,180,100,0.3);border-radius:24px;padding:2.5rem 2rem;text-align:center;">
            <svg viewBox="0 0 100 90" style="width:80px;height:80px;margin-bottom:1rem;">
                <defs>
                    <linearGradient id="hg1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#2eb464"/>
                        <stop offset="100%" style="stop-color:#1a7a40"/>
                    </linearGradient>
                </defs>
                <path d="M50 85 C50 85 5 55 5 28 C5 15 15 5 28 5 C38 5 46 11 50 20 C54 11 62 5 72 5 C85 5 95 15 95 28 C95 55 50 85 50 85Z" fill="url(#hg1)" opacity="0.9"/>
                <path d="M25 38 L38 38 L44 28 L50 48 L56 32 L62 38 L75 38" stroke="white" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div style="font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;color:#f0ece4;margin-bottom:0.5rem;">Check Your Heart</div>
            <div style="font-size:0.83rem;color:rgba(240,236,228,0.45);line-height:1.6;margin-bottom:0.5rem;">AI-powered cardiovascular risk assessment using Random Forest ML</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Heart Check →", key="go_heart", use_container_width=True):
            st.session_state.page = "heart"
            st.rerun()

    with col2:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(100,120,255,0.3);border-radius:24px;padding:2.5rem 2rem;text-align:center;">
            <svg viewBox="0 0 100 100" style="width:80px;height:80px;margin-bottom:1rem;">
                <defs>
                    <linearGradient id="bg1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#6478ff"/>
                        <stop offset="100%" style="stop-color:#3040c0"/>
                    </linearGradient>
                </defs>
                <circle cx="50" cy="28" r="14" fill="url(#bg1)" opacity="0.9"/>
                <rect x="32" y="46" width="36" height="38" rx="8" fill="url(#bg1)" opacity="0.85"/>
                <line x1="50" y1="46" x2="50" y2="84" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
                <rect x="18" y="90" width="64" height="5" rx="2.5" fill="url(#bg1)" opacity="0.6"/>
            </svg>
            <div style="font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;color:#f0ece4;margin-bottom:0.5rem;">Your BMI</div>
            <div style="font-size:0.83rem;color:rgba(240,236,228,0.45);line-height:1.6;margin-bottom:0.5rem;">Calculate Body Mass Index and understand your weight health status</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open BMI Check →", key="go_bmi", use_container_width=True):
            st.session_state.page = "bmi"
            st.rerun()

    st.markdown("""
    <div style="text-align:center;padding:2rem 0 1rem;font-size:0.75rem;color:rgba(240,236,228,0.2);letter-spacing:0.1em;">
        CRAFTED WITH CARE &nbsp;·&nbsp; <span style="color:rgba(192,80,122,0.6);">HEALTHAI by MORSALIN</span>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# HEART DISEASE PAGE
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "heart":

    st.markdown('<div class="page-wrap page-heart">', unsafe_allow_html=True)

    # Back
    if st.button("← Back to Home", key="back_heart"):
        st.session_state.page = "landing"
        st.rerun()

    st.markdown("""
    <div class="page-header">
        <div class="page-eyebrow eyebrow-red">Cardiovascular AI</div>
        <div class="page-title title-red">Heart Checking</div>
        <div class="page-byline">Made by Morsalin &nbsp;·&nbsp; Random Forest Model</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="form-panel"><div class="panel-title">Basic Info</div>', unsafe_allow_html=True)
        age = st.slider("Age", 20, 80, 50)
        sex = st.selectbox("Sex", options=[0,1], format_func=lambda x: "Female" if x==0 else "Male")
        cp = st.selectbox("Chest Pain Type", options=[0,1,2,3],
                          format_func=lambda x: {0:"Typical Angina",1:"Atypical Angina",2:"Non-anginal",3:"Asymptomatic"}[x])
        trestbps = st.slider("Resting Blood Pressure (mmHg)", 90, 200, 130)
        chol = st.slider("Cholesterol (mg/dl)", 100, 600, 246)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="form-panel"><div class="panel-title">Blood & ECG</div>', unsafe_allow_html=True)
        fbs = st.selectbox("Fasting Blood Sugar > 120?", options=[0,1], format_func=lambda x: "No" if x==0 else "Yes")
        restecg = st.selectbox("Resting ECG", options=[0,1,2],
                               format_func=lambda x: {0:"Normal",1:"ST-T Abnormality",2:"LV Hypertrophy"}[x])
        thalach = st.slider("Max Heart Rate", 70, 210, 150)
        exang = st.selectbox("Exercise Induced Angina", options=[0,1], format_func=lambda x: "No" if x==0 else "Yes")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="form-panel"><div class="panel-title">Advanced</div>', unsafe_allow_html=True)
        oldpeak = st.slider("ST Depression", 0.0, 6.5, 1.0, 0.1)
        slope = st.selectbox("ST Slope", options=[0,1,2],
                             format_func=lambda x: {0:"Upsloping",1:"Flat",2:"Downsloping"}[x])
        ca = st.selectbox("Major Vessels (0-4)", options=[0,1,2,3,4])
        thal = st.selectbox("Thalassemia", options=[0,1,2,3],
                            format_func=lambda x: {0:"Normal",1:"Fixed Defect",2:"Reversible Defect",3:"Unknown"}[x])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Analyze Heart Risk", use_container_width=True, key="predict_btn"):
        input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0]

        if prediction == 1:
            st.markdown(f"""
            <div class="res-high">
                <div class="res-title" style="color:#e05070;">⚠️ High Risk Detected</div>
                <div class="res-sub">Heart disease risk identified — please consult a doctor</div>
                <div class="res-pct" style="color:#e05070;">{probability[1]*100:.1f}%</div>
                <div style="font-size:0.8rem;color:rgba(240,236,228,0.4);margin-top:0.3rem;">Risk Probability</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="res-low">
                <div class="res-title" style="color:#2eb464;">✅ Low Risk</div>
                <div class="res-sub">No significant heart disease risk detected</div>
                <div class="res-pct" style="color:#2eb464;">{probability[0]*100:.1f}%</div>
                <div style="font-size:0.8rem;color:rgba(240,236,228,0.4);margin-top:0.3rem;">Healthy Probability</div>
            </div>
            """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=probability[1]*100,
                title={'text': "Risk %", 'font': {'color': '#f0ece4', 'size': 14}},
                gauge={
                    'axis': {'range': [0,100], 'tickcolor': '#f0ece4', 'tickfont': {'color': '#f0ece4'}},
                    'bar': {'color': "#e05070" if prediction==1 else "#2eb464"},
                    'bgcolor': 'rgba(255,255,255,0.03)',
                    'steps': [
                        {'range': [0,30], 'color': 'rgba(46,180,100,0.15)'},
                        {'range': [30,60], 'color': 'rgba(241,196,15,0.15)'},
                        {'range': [60,100], 'color': 'rgba(220,50,80,0.15)'}
                    ],
                    'threshold': {'line': {'color': 'white', 'width': 3}, 'value': 50, 'thickness': 0.75}
                },
                number={'font': {'color': '#f0ece4', 'size': 36}, 'suffix': '%'}
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': '#f0ece4'}, height=280, margin=dict(t=40,b=0,l=20,r=20))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown("**Risk Factor Analysis**")
            risk_factors = []
            good_factors = []
            if age > 55: risk_factors.append("Age > 55")
            if chol > 240: risk_factors.append("Cholesterol > 240 mg/dl")
            if trestbps > 140: risk_factors.append("Blood Pressure > 140")
            if thalach < 120: risk_factors.append("Low Max Heart Rate")
            if exang == 1: risk_factors.append("Exercise Angina present")
            if oldpeak > 2: risk_factors.append("ST Depression > 2")
            if age <= 45: good_factors.append("Healthy age range")
            if chol <= 200: good_factors.append("Normal cholesterol")
            if trestbps <= 120: good_factors.append("Normal blood pressure")
            if thalach >= 150: good_factors.append("Good heart rate")

            for r in risk_factors:
                st.markdown(f"🔴 {r}")
            for g in good_factors:
                st.markdown(f"🟢 {g}")
            if not risk_factors and not good_factors:
                st.markdown("All parameters within normal range.")

        # Bar chart
        param_names = ['Age','Sex','CP','BP','Chol','FBS','ECG','HR','ExAng','STPk','Slope','CA','Thal']
        param_values = [age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
        ranges = [(20,80),(0,1),(0,3),(90,200),(100,600),(0,1),(0,2),(70,210),(0,1),(0,6.5),(0,2),(0,4),(0,3)]
        norm_vals = [(v-mn)/(mx-mn)*100 for v,(mn,mx) in zip(param_values, ranges)]
        bar_colors = ['#e05070' if n>70 else '#f0a030' if n>40 else '#2eb464' for n in norm_vals]

        fig2 = go.Figure(go.Bar(x=param_names, y=norm_vals, marker_color=bar_colors,
                                text=[str(v) for v in param_values], textposition='outside',
                                textfont={'color':'#f0ece4','size':11}))
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)',
                           font={'color':'#f0ece4'}, height=280,
                           yaxis={'title':'Normalized %','gridcolor':'rgba(255,255,255,0.06)','color':'#f0ece4'},
                           xaxis={'color':'#f0ece4'}, margin=dict(t=20,b=0,l=0,r=0))
        st.plotly_chart(fig2, use_container_width=True)

        # PDF
        def generate_pdf():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica","B",20)
            pdf.set_text_color(180,40,80)
            pdf.cell(0,15,"Heart Disease Prediction Report",ln=True,align="C")
            pdf.set_font("Helvetica","",10)
            pdf.set_text_color(120,120,120)
            pdf.cell(0,7,f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Made by Morsalin",ln=True,align="C")
            pdf.ln(4)
            if prediction==1:
                pdf.set_fill_color(200,50,80)
            else:
                pdf.set_fill_color(46,180,100)
            pdf.set_text_color(255,255,255)
            pdf.set_font("Helvetica","B",13)
            pdf.cell(0,11,f"RESULT: {'HIGH RISK' if prediction==1 else 'LOW RISK - Healthy'}",ln=True,align="C",fill=True)
            pdf.ln(4)
            pdf.set_text_color(0,0,0)
            pdf.set_font("Helvetica","B",12)
            pdf.cell(0,9,"Probabilities:",ln=True)
            pdf.set_font("Helvetica","",11)
            pdf.cell(0,7,f"  Healthy: {probability[0]*100:.1f}%",ln=True)
            pdf.cell(0,7,f"  Heart Disease: {probability[1]*100:.1f}%",ln=True)
            pdf.ln(4)
            pdf.set_font("Helvetica","B",12)
            pdf.cell(0,9,"Parameters:",ln=True)
            pdf.set_font("Helvetica","",10)
            for name,val in [("Age",age),("Sex","Male" if sex else "Female"),("Chest Pain",cp),
                             ("BP",f"{trestbps} mmHg"),("Cholesterol",f"{chol} mg/dl"),
                             ("FBS>120","Yes" if fbs else "No"),("ECG",restecg),("Max HR",thalach),
                             ("Ex.Angina","Yes" if exang else "No"),("ST Dep",oldpeak),
                             ("Slope",slope),("Vessels",ca),("Thal",thal)]:
                pdf.cell(80,7,f"  {name}:")
                pdf.cell(0,7,str(val),ln=True)
            pdf.ln(4)
            pdf.set_font("Helvetica","I",9)
            pdf.set_text_color(130,130,130)
            pdf.multi_cell(0,6,"DISCLAIMER: AI prediction only. Consult a qualified medical professional for diagnosis.")
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            pdf.output(tmp.name)
            return tmp.name

        try:
            pdf_path = generate_pdf()
            with open(pdf_path,"rb") as f:
                st.download_button("📥 Download PDF Report", data=f.read(),
                                   file_name=f"heart_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                   mime="application/pdf", use_container_width=True)
            os.unlink(pdf_path)
        except Exception as e:
            st.info("Add 'fpdf2' to requirements.txt to enable PDF download.")

        st.markdown("""
        <div style="background:rgba(200,50,80,0.08);border:1px solid rgba(200,50,80,0.25);border-radius:12px;padding:1rem 1.2rem;margin-top:1rem;font-size:0.83rem;color:rgba(240,236,228,0.55);">
            This is an AI prediction only. For medical decisions, always consult a licensed physician.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# BMI PAGE
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "bmi":

    st.markdown('<div class="page-wrap page-bmi">', unsafe_allow_html=True)

    if st.button("← Back to Home", key="back_bmi"):
        st.session_state.page = "landing"
        st.rerun()

    st.markdown("""
    <div class="page-header">
        <div class="page-eyebrow eyebrow-blue">Body Composition</div>
        <div class="page-title title-blue">Check Your BMI</div>
        <div class="page-byline">Made by Morsalin &nbsp;·&nbsp; Body Mass Index Calculator</div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1,1])

    with col_left:
        st.markdown('<div class="form-panel"><div class="panel-title">Your Measurements</div>', unsafe_allow_html=True)
        height_cm = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        weight_kg = st.number_input("Weight (kg)", min_value=20, max_value=300, value=70)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Calculate My BMI", use_container_width=True, key="calc_bmi"):
            bmi = weight_kg / ((height_cm/100)**2)
            st.session_state.bmi_result = bmi

    with col_right:
        if "bmi_result" in st.session_state:
            bmi = st.session_state.bmi_result
            if bmi < 18.5:
                cat, col, advice = "Underweight", "#6478ff", "Consider a nutritious diet plan to reach a healthy weight."
            elif bmi < 25:
                cat, col, advice = "Normal Weight", "#2eb464", "Great job! Maintain your healthy lifestyle."
            elif bmi < 30:
                cat, col, advice = "Overweight", "#f0a030", "Consider regular exercise and a balanced diet."
            else:
                cat, col, advice = "Obese", "#e05070", "Please consult a doctor for a personalized health plan."

            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:1.5px solid {col}40;border-radius:20px;padding:2rem;text-align:center;margin-bottom:1rem;">
                <div style="font-family:'Playfair Display',serif;font-size:3.5rem;font-weight:900;color:{col};margin:0;">{bmi:.1f}</div>
                <div style="font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;color:#f0ece4;margin:0.3rem 0;">{cat}</div>
                <div style="font-size:0.85rem;color:rgba(240,236,228,0.5);line-height:1.6;">{advice}</div>
            </div>
            """, unsafe_allow_html=True)

            fig_bmi = go.Figure(go.Indicator(
                mode="gauge+number",
                value=bmi,
                title={'text': "BMI", 'font': {'color': '#f0ece4', 'size': 14}},
                gauge={
                    'axis': {'range': [10,45], 'tickcolor': '#f0ece4', 'tickfont': {'color': '#f0ece4'}},
                    'bar': {'color': col},
                    'bgcolor': 'rgba(255,255,255,0.02)',
                    'steps': [
                        {'range': [10,18.5], 'color': 'rgba(100,120,255,0.15)'},
                        {'range': [18.5,25], 'color': 'rgba(46,180,100,0.15)'},
                        {'range': [25,30], 'color': 'rgba(240,160,48,0.15)'},
                        {'range': [30,45], 'color': 'rgba(220,50,80,0.15)'}
                    ]
                },
                number={'font': {'color': '#f0ece4', 'size': 40}}
            ))
            fig_bmi.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color':'#f0ece4'}, height=260, margin=dict(t=40,b=0,l=20,r=20))
            st.plotly_chart(fig_bmi, use_container_width=True)

    st.markdown("""
    <div style="margin-top:2rem;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.5rem;position:relative;z-index:1;">
        <div style="font-size:0.68rem;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:rgba(240,236,228,0.3);margin-bottom:1rem;">BMI Reference Chart</div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.8rem;text-align:center;">
            <div style="background:rgba(100,120,255,0.1);border:1px solid rgba(100,120,255,0.25);border-radius:12px;padding:0.8rem;">
                <div style="font-size:0.75rem;color:#6478ff;font-weight:600;">UNDERWEIGHT</div>
                <div style="font-size:1.1rem;font-weight:700;color:#f0ece4;margin-top:0.2rem;">&lt; 18.5</div>
            </div>
            <div style="background:rgba(46,180,100,0.1);border:1px solid rgba(46,180,100,0.25);border-radius:12px;padding:0.8rem;">
                <div style="font-size:0.75rem;color:#2eb464;font-weight:600;">NORMAL</div>
                <div style="font-size:1.1rem;font-weight:700;color:#f0ece4;margin-top:0.2rem;">18.5 – 24.9</div>
            </div>
            <div style="background:rgba(240,160,48,0.1);border:1px solid rgba(240,160,48,0.25);border-radius:12px;padding:0.8rem;">
                <div style="font-size:0.75rem;color:#f0a030;font-weight:600;">OVERWEIGHT</div>
                <div style="font-size:1.1rem;font-weight:700;color:#f0ece4;margin-top:0.2rem;">25 – 29.9</div>
            </div>
            <div style="background:rgba(220,50,80,0.1);border:1px solid rgba(220,50,80,0.25);border-radius:12px;padding:0.8rem;">
                <div style="font-size:0.75rem;color:#e05070;font-weight:600;">OBESE</div>
                <div style="font-size:1.1rem;font-weight:700;color:#f0ece4;margin-top:0.2rem;">&ge; 30</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
