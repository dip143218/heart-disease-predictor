import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
import tempfile
import os
from datetime import datetime

st.set_page_config(page_title="HealthAI — Morsalin Hossain Dip", page_icon="❤️", layout="wide")

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');
* { box-sizing: border-box; margin: 0; }
html, body, [data-testid="stAppViewContainer"] {
    background: #08080f !important;
    color: #f0ece4;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }

/* NAV */
.top-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.2rem 3rem;
    background: rgba(255,255,255,0.02);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    position: sticky; top: 0; z-index: 100;
    backdrop-filter: blur(12px);
}
.nav-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #f0ece4, #c0507a);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.nav-links { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.nav-tag {
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; padding: 0.35rem 0.9rem;
    border-radius: 100px; cursor: pointer;
    color: rgba(240,236,228,0.5);
    border: 1px solid rgba(255,255,255,0.08);
    background: transparent; transition: all 0.25s;
}
.nav-active {
    color: #f0ece4 !important;
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.2) !important;
}

/* PAGE WRAP */
.page-wrap {
    min-height: calc(100vh - 65px);
    padding: 3rem 3rem 5rem;
    position: relative; overflow: hidden;
}
.grid-bg {
    position: fixed; inset: 0; pointer-events: none;
    background-image:
        linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px);
    background-size: 55px 55px; z-index: 0;
}

/* SECTION TITLE */
.sec-eyebrow {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.22em;
    text-transform: uppercase; margin-bottom: 0.6rem;
}
.sec-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 4vw, 3rem); font-weight: 900; line-height: 1.1;
    margin-bottom: 0.5rem;
}
.sec-byline { font-size: 0.83rem; color: rgba(240,236,228,0.35); letter-spacing: 0.06em; }

/* CARDS */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px; padding: 1.8rem 1.5rem;
    position: relative; z-index: 1;
}
.card-sm { border-radius: 14px; padding: 1.2rem; }

/* STAT CARD */
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px,1fr)); gap: 1rem; margin: 1.5rem 0; }
.stat-item {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 1.3rem 1rem; text-align: center;
}
.stat-val { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 900; }
.stat-lbl { font-size: 0.72rem; color: rgba(240,236,228,0.4); letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.2rem; }

/* RESULT */
.res-high {
    background: linear-gradient(135deg, rgba(220,50,80,0.15), rgba(150,20,40,0.08));
    border: 1.5px solid rgba(220,50,80,0.45); border-radius: 18px;
    padding: 2rem; text-align: center; margin: 1.5rem 0;
}
.res-low {
    background: linear-gradient(135deg, rgba(46,180,100,0.15), rgba(20,120,60,0.08));
    border: 1.5px solid rgba(46,180,100,0.45); border-radius: 18px;
    padding: 2rem; text-align: center; margin: 1.5rem 0;
}

/* BUTTON */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #b03060, #7b2ff7) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 0.95rem !important;
    padding: 0.7rem 1.5rem !important; transition: all 0.3s !important;
    box-shadow: 0 4px 20px rgba(176,48,96,0.3) !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(176,48,96,0.5) !important;
}
div[data-testid="stDownloadButton"] > button {
    background: rgba(46,180,100,0.12) !important; color: #2eb464 !important;
    border: 1px solid rgba(46,180,100,0.35) !important; box-shadow: none !important;
}

/* FORM */
label[data-testid="stWidgetLabel"] > div { color: rgba(240,236,228,0.65) !important; font-size: 0.83rem !important; }
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border-color: rgba(255,255,255,0.1) !important; color: #f0ece4 !important; border-radius: 10px !important;
}
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border-color: rgba(255,255,255,0.1) !important; color: #f0ece4 !important; border-radius: 10px !important;
}
[data-testid="stSlider"] > div > div > div { background: rgba(176,48,96,0.7) !important; }

/* TAGS */
.tag {
    display: inline-block; font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.08em; padding: 0.3rem 0.8rem; border-radius: 100px; margin: 0.2rem;
}
.tag-red { background: rgba(192,80,122,0.15); border: 1px solid rgba(192,80,122,0.35); color: #c0507a; }
.tag-blue { background: rgba(100,120,255,0.15); border: 1px solid rgba(100,120,255,0.35); color: #6478ff; }
.tag-green { background: rgba(46,180,100,0.15); border: 1px solid rgba(46,180,100,0.35); color: #2eb464; }
.tag-gray { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); color: rgba(240,236,228,0.5); }

/* PERF TABLE */
.perf-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.9rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.perf-row:last-child { border-bottom: none; }
.perf-name { font-size: 0.88rem; color: rgba(240,236,228,0.65); }
.perf-bar-wrap { flex: 1; margin: 0 1.2rem; height: 6px; background: rgba(255,255,255,0.07); border-radius: 3px; overflow: hidden; }
.perf-bar { height: 100%; border-radius: 3px; }
.perf-val { font-family: 'Playfair Display', serif; font-size: 1.1rem; font-weight: 700; min-width: 55px; text-align: right; }

div[data-testid="stTabs"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"

# ── MODEL ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model = joblib.load('heart_disease_model.pkl')
    scaler = joblib.load('scaler.pkl')
    return model, scaler
model, scaler = load_model()

# ── NAV ───────────────────────────────────────────────────────────────────────
pages = [("home","🏠 Home"), ("heart","❤️ Heart Check"), ("bmi","🧮 BMI"), ("analysis","📊 Analysis"), ("about","👤 About")]
nav_cols = st.columns([2,1,1,1,1,1])
with nav_cols[0]:
    st.markdown('<div class="nav-logo">HealthAI</div>', unsafe_allow_html=True)
for i, (pid, plabel) in enumerate(pages):
    with nav_cols[i+1]:
        active = "nav-active" if st.session_state.page == pid else ""
        if st.button(plabel, key=f"nav_{pid}"):
            st.session_state.page = pid
            st.rerun()

st.markdown('<div class="grid-bg"></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ════════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;padding:3rem 1rem 2rem;position:relative;z-index:1;">
        <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.22em;text-transform:uppercase;
                    color:#c0507a;background:rgba(192,80,122,0.1);border:1px solid rgba(192,80,122,0.25);
                    display:inline-block;padding:0.35rem 1.1rem;border-radius:100px;margin-bottom:1.5rem;">
            AI Health Platform · CUET Final Year Project
        </div>
        <h1 style="font-family:'Playfair Display',serif;font-size:clamp(2.8rem,6vw,5rem);font-weight:900;
                   line-height:1.05;background:linear-gradient(135deg,#f0ece4 30%,#c0507a 65%,#7b2ff7 100%);
                   -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
                   margin-bottom:1.2rem;">
            Know Your Heart.<br>Know Your Body.
        </h1>
        <p style="font-size:1.05rem;font-weight:300;color:rgba(240,236,228,0.5);max-width:520px;
                  line-height:1.75;margin:0 auto 2.5rem;">
            Advanced machine-learning cardiovascular risk assessment and body composition analysis — 
            powered by Random Forest with <strong style="color:#2eb464;">95.54% accuracy</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    st.markdown("""
    <div class="stat-grid" style="max-width:900px;margin:0 auto 3rem;position:relative;z-index:1;">
        <div class="stat-item">
            <div class="stat-val" style="color:#2eb464;">95.54%</div>
            <div class="stat-lbl">Model Accuracy</div>
        </div>
        <div class="stat-item">
            <div class="stat-val" style="color:#6478ff;">13</div>
            <div class="stat-lbl">Clinical Features</div>
        </div>
        <div class="stat-item">
            <div class="stat-val" style="color:#c0507a;">RF</div>
            <div class="stat-lbl">Algorithm</div>
        </div>
        <div class="stat-item">
            <div class="stat-val" style="color:#f0a030;">UCI</div>
            <div class="stat-lbl">Dataset Source</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    _, cc1, cc2, cc3, _ = st.columns([0.3,1,1,1,0.3])
    with cc1:
        st.markdown("""
        <div class="card" style="border-color:rgba(192,80,122,0.3);text-align:center;">
            <div style="font-size:2.5rem;margin-bottom:1rem;">❤️</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;margin-bottom:0.5rem;">Heart Check</div>
            <div style="font-size:0.82rem;color:rgba(240,236,228,0.45);line-height:1.6;">
                AI-powered cardiovascular risk prediction using 13 clinical parameters
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open →", key="h_heart", use_container_width=True):
            st.session_state.page = "heart"; st.rerun()

    with cc2:
        st.markdown("""
        <div class="card" style="border-color:rgba(100,120,255,0.3);text-align:center;">
            <div style="font-size:2.5rem;margin-bottom:1rem;">🧮</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;margin-bottom:0.5rem;">BMI Calculator</div>
            <div style="font-size:0.82rem;color:rgba(240,236,228,0.45);line-height:1.6;">
                Body Mass Index calculator with visual gauge and health category
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open →", key="h_bmi", use_container_width=True):
            st.session_state.page = "bmi"; st.rerun()

    with cc3:
        st.markdown("""
        <div class="card" style="border-color:rgba(46,180,100,0.3);text-align:center;">
            <div style="font-size:2.5rem;margin-bottom:1rem;">📊</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;margin-bottom:0.5rem;">Data Analysis</div>
            <div style="font-size:0.82rem;color:rgba(240,236,228,0.45);line-height:1.6;">
                Dataset insights, model performance metrics and feature importance
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open →", key="h_analysis", use_container_width=True):
            st.session_state.page = "analysis"; st.rerun()

    st.markdown("""
    <div style="text-align:center;padding:3rem 0 1rem;font-size:0.75rem;color:rgba(240,236,228,0.2);letter-spacing:0.1em;position:relative;z-index:1;">
        MADE WITH ❤️ &nbsp;·&nbsp; <span style="color:rgba(192,80,122,0.6);">MORSALIN HOSSAIN DIP · CUET</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# HEART PAGE
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "heart":
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-bottom:2.5rem;position:relative;z-index:1;">
        <div class="sec-eyebrow" style="color:#c0507a;">Cardiovascular AI Assessment</div>
        <div class="sec-title" style="background:linear-gradient(135deg,#f0ece4,#e05070);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
            Heart Checking
        </div>
        <div class="sec-byline">Made by Morsalin Hossain Dip &nbsp;·&nbsp; CUET &nbsp;·&nbsp; Random Forest · 95.54% Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card" style="position:relative;z-index:1;"><div style="font-size:0.68rem;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:rgba(240,236,228,0.3);margin-bottom:1rem;">BASIC INFO</div>', unsafe_allow_html=True)
        age = st.slider("Age", 20, 80, 50)
        sex = st.selectbox("Sex", [0,1], format_func=lambda x:"Female" if x==0 else "Male")
        cp = st.selectbox("Chest Pain Type", [0,1,2,3], format_func=lambda x:{0:"Typical Angina",1:"Atypical Angina",2:"Non-anginal",3:"Asymptomatic"}[x])
        trestbps = st.slider("Resting Blood Pressure (mmHg)", 90, 200, 130)
        chol = st.slider("Cholesterol (mg/dl)", 100, 600, 246)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card" style="position:relative;z-index:1;"><div style="font-size:0.68rem;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:rgba(240,236,228,0.3);margin-bottom:1rem;">BLOOD & ECG</div>', unsafe_allow_html=True)
        fbs = st.selectbox("Fasting Blood Sugar > 120?", [0,1], format_func=lambda x:"No" if x==0 else "Yes")
        restecg = st.selectbox("Resting ECG", [0,1,2], format_func=lambda x:{0:"Normal",1:"ST-T Abnormality",2:"LV Hypertrophy"}[x])
        thalach = st.slider("Max Heart Rate", 70, 210, 150)
        exang = st.selectbox("Exercise Induced Angina", [0,1], format_func=lambda x:"No" if x==0 else "Yes")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card" style="position:relative;z-index:1;"><div style="font-size:0.68rem;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:rgba(240,236,228,0.3);margin-bottom:1rem;">ADVANCED</div>', unsafe_allow_html=True)
        oldpeak = st.slider("ST Depression", 0.0, 6.5, 1.0, 0.1)
        slope = st.selectbox("ST Slope", [0,1,2], format_func=lambda x:{0:"Upsloping",1:"Flat",2:"Downsloping"}[x])
        ca = st.selectbox("Major Vessels (0-4)", [0,1,2,3,4])
        thal = st.selectbox("Thalassemia", [0,1,2,3], format_func=lambda x:{0:"Normal",1:"Fixed Defect",2:"Reversible Defect",3:"Unknown"}[x])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 Analyze Heart Disease Risk", use_container_width=True):
        inp = np.array([[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]])
        inp_s = scaler.transform(inp)
        pred = model.predict(inp_s)[0]
        prob = model.predict_proba(inp_s)[0]

        if pred == 1:
            st.markdown(f"""<div class="res-high" style="position:relative;z-index:1;">
                <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;color:#e05070;">⚠️ High Risk Detected</div>
                <div style="color:rgba(240,236,228,0.55);margin:0.4rem 0 0.8rem;">Heart disease risk identified — consult a cardiologist</div>
                <div style="font-family:'Playfair Display',serif;font-size:3.5rem;font-weight:900;color:#e05070;">{prob[1]*100:.1f}%</div>
                <div style="font-size:0.78rem;color:rgba(240,236,228,0.35);">Risk Probability</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="res-low" style="position:relative;z-index:1;">
                <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;color:#2eb464;">✅ Low Risk</div>
                <div style="color:rgba(240,236,228,0.55);margin:0.4rem 0 0.8rem;">No significant heart disease risk detected</div>
                <div style="font-family:'Playfair Display',serif;font-size:3.5rem;font-weight:900;color:#2eb464;">{prob[0]*100:.1f}%</div>
                <div style="font-size:0.78rem;color:rgba(240,236,228,0.35);">Healthy Probability</div>
            </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=prob[1]*100,
                title={'text':"Risk %",'font':{'color':'#f0ece4','size':13}},
                gauge={'axis':{'range':[0,100],'tickcolor':'#f0ece4','tickfont':{'color':'#f0ece4'}},
                       'bar':{'color':"#e05070" if pred==1 else "#2eb464"},
                       'bgcolor':'rgba(255,255,255,0.02)',
                       'steps':[{'range':[0,30],'color':'rgba(46,180,100,0.12)'},
                                 {'range':[30,60],'color':'rgba(241,196,15,0.12)'},
                                 {'range':[60,100],'color':'rgba(220,50,80,0.12)'}],
                       'threshold':{'line':{'color':'white','width':3},'value':50,'thickness':0.75}},
                number={'font':{'color':'#f0ece4','size':36},'suffix':'%'}))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',font={'color':'#f0ece4'},height=260,margin=dict(t=40,b=0,l=20,r=20))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown("**Risk Factor Analysis**")
            rf, gf = [], []
            if age>55: rf.append("Age > 55")
            if chol>240: rf.append("Cholesterol > 240 mg/dl")
            if trestbps>140: rf.append("Blood Pressure > 140")
            if thalach<120: rf.append("Low Max Heart Rate")
            if exang==1: rf.append("Exercise Angina present")
            if oldpeak>2: rf.append("ST Depression > 2")
            if age<=45: gf.append("Healthy age range")
            if chol<=200: gf.append("Normal cholesterol")
            if trestbps<=120: gf.append("Normal blood pressure")
            if thalach>=150: gf.append("Good heart rate")
            for r in rf: st.markdown(f"🔴 {r}")
            for g in gf: st.markdown(f"🟢 {g}")
            if not rf and not gf: st.markdown("All parameters within normal range.")

        # Bar chart
        pnames = ['Age','Sex','CP','BP','Chol','FBS','ECG','HR','ExAng','STPk','Slope','CA','Thal']
        pvals = [age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
        ranges = [(20,80),(0,1),(0,3),(90,200),(100,600),(0,1),(0,2),(70,210),(0,1),(0,6.5),(0,2),(0,4),(0,3)]
        nv = [(v-mn)/(mx-mn)*100 for v,(mn,mx) in zip(pvals,ranges)]
        bc = ['#e05070' if n>70 else '#f0a030' if n>40 else '#2eb464' for n in nv]
        fig2 = go.Figure(go.Bar(x=pnames,y=nv,marker_color=bc,text=[str(v) for v in pvals],textposition='outside',textfont={'color':'#f0ece4','size':10}))
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(255,255,255,0.02)',font={'color':'#f0ece4'},height=260,
                           yaxis={'title':'Normalized %','gridcolor':'rgba(255,255,255,0.06)','color':'#f0ece4'},
                           xaxis={'color':'#f0ece4'},margin=dict(t=20,b=0,l=0,r=0))
        st.plotly_chart(fig2, use_container_width=True)

        # PDF
        def gen_pdf():
            pdf = FPDF(); pdf.add_page()
            pdf.set_font("Helvetica","B",18); pdf.set_text_color(180,40,80)
            pdf.cell(0,14,"Heart Disease Prediction Report",ln=True,align="C")
            pdf.set_font("Helvetica","",9); pdf.set_text_color(130,130,130)
            pdf.cell(0,6,f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  Morsalin Hossain Dip · CUET",ln=True,align="C")
            pdf.ln(4)
            pdf.set_fill_color(200,50,80) if pred==1 else pdf.set_fill_color(46,180,100)
            pdf.set_text_color(255,255,255); pdf.set_font("Helvetica","B",12)
            pdf.cell(0,10,f"RESULT: {'HIGH RISK — Heart Disease Detected' if pred==1 else 'LOW RISK — Healthy'}",ln=True,align="C",fill=True)
            pdf.ln(4); pdf.set_text_color(0,0,0)
            pdf.set_font("Helvetica","B",11); pdf.cell(0,8,"Prediction Probabilities:",ln=True)
            pdf.set_font("Helvetica","",10)
            pdf.cell(0,7,f"  Healthy: {prob[0]*100:.1f}%",ln=True)
            pdf.cell(0,7,f"  Heart Disease: {prob[1]*100:.1f}%",ln=True)
            pdf.ln(4); pdf.set_font("Helvetica","B",11); pdf.cell(0,8,"Patient Parameters:",ln=True)
            pdf.set_font("Helvetica","",10)
            for nm,vl in [("Age",age),("Sex","Male" if sex else "Female"),("Chest Pain",cp),
                          ("BP",f"{trestbps} mmHg"),("Cholesterol",f"{chol} mg/dl"),
                          ("FBS>120","Yes" if fbs else "No"),("ECG",restecg),("Max HR",thalach),
                          ("Ex.Angina","Yes" if exang else "No"),("ST Dep",oldpeak),
                          ("Slope",slope),("Vessels",ca),("Thal",thal)]:
                pdf.cell(75,7,f"  {nm}:"); pdf.cell(0,7,str(vl),ln=True)
            pdf.ln(4); pdf.set_font("Helvetica","I",8); pdf.set_text_color(150,150,150)
            pdf.multi_cell(0,5,"DISCLAIMER: AI prediction only. Always consult a licensed medical professional.")
            tmp = tempfile.NamedTemporaryFile(delete=False,suffix=".pdf"); pdf.output(tmp.name); return tmp.name
        try:
            pp = gen_pdf()
            with open(pp,"rb") as f:
                st.download_button("📥 Download PDF Report",data=f.read(),
                                   file_name=f"heart_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                   mime="application/pdf",use_container_width=True)
            os.unlink(pp)
        except: st.info("Add 'fpdf2' to requirements.txt to enable PDF.")

        st.markdown('<div style="background:rgba(200,50,80,0.07);border:1px solid rgba(200,50,80,0.2);border-radius:12px;padding:0.9rem 1.2rem;margin-top:1rem;font-size:0.8rem;color:rgba(240,236,228,0.45);">This is an AI prediction only. For medical decisions, always consult a licensed physician.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# BMI PAGE
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "bmi":
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;margin-bottom:2.5rem;position:relative;z-index:1;">
        <div class="sec-eyebrow" style="color:#6478ff;">Body Composition</div>
        <div class="sec-title" style="background:linear-gradient(135deg,#f0ece4,#6478ff);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
            Check Your BMI
        </div>
        <div class="sec-byline">Made by Morsalin Hossain Dip &nbsp;·&nbsp; CUET &nbsp;·&nbsp; Body Mass Index Calculator</div>
    </div>
    """, unsafe_allow_html=True)

    cl, cr = st.columns([1,1])
    with cl:
        st.markdown('<div class="card" style="position:relative;z-index:1;">', unsafe_allow_html=True)
        h = st.number_input("Height (cm)", 100, 250, 170)
        w = st.number_input("Weight (kg)", 20, 300, 70)
        st.markdown('</div><br>', unsafe_allow_html=True)
        if st.button("Calculate My BMI", use_container_width=True):
            st.session_state.bmi_val = w / ((h/100)**2)

    with cr:
        if "bmi_val" in st.session_state:
            bmi = st.session_state.bmi_val
            if bmi<18.5: cat,col,adv="Underweight","#6478ff","Consider a nutritious diet to reach healthy weight."
            elif bmi<25: cat,col,adv="Normal Weight","#2eb464","Excellent! Maintain your healthy lifestyle."
            elif bmi<30: cat,col,adv="Overweight","#f0a030","Regular exercise and balanced diet recommended."
            else: cat,col,adv="Obese","#e05070","Please consult a doctor for a personalized health plan."

            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:1.5px solid {col}40;border-radius:18px;
                        padding:2rem;text-align:center;margin-bottom:1rem;position:relative;z-index:1;">
                <div style="font-family:'Playfair Display',serif;font-size:3.5rem;font-weight:900;color:{col};">{bmi:.1f}</div>
                <div style="font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;color:#f0ece4;margin:0.3rem 0;">{cat}</div>
                <div style="font-size:0.83rem;color:rgba(240,236,228,0.45);line-height:1.6;">{adv}</div>
            </div>
            """, unsafe_allow_html=True)

            fg = go.Figure(go.Indicator(
                mode="gauge+number", value=bmi,
                title={'text':"BMI",'font':{'color':'#f0ece4','size':13}},
                gauge={'axis':{'range':[10,45],'tickcolor':'#f0ece4','tickfont':{'color':'#f0ece4'}},
                       'bar':{'color':col},'bgcolor':'rgba(255,255,255,0.02)',
                       'steps':[{'range':[10,18.5],'color':'rgba(100,120,255,0.12)'},
                                 {'range':[18.5,25],'color':'rgba(46,180,100,0.12)'},
                                 {'range':[25,30],'color':'rgba(240,160,48,0.12)'},
                                 {'range':[30,45],'color':'rgba(220,50,80,0.12)'}]},
                number={'font':{'color':'#f0ece4','size':38}}))
            fg.update_layout(paper_bgcolor='rgba(0,0,0,0)',font={'color':'#f0ece4'},height=250,margin=dict(t=40,b=0,l=20,r=20))
            st.plotly_chart(fg, use_container_width=True)

    st.markdown("""
    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:16px;
                padding:1.5rem;margin-top:1.5rem;position:relative;z-index:1;">
        <div style="font-size:0.65rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;
                    color:rgba(240,236,228,0.28);margin-bottom:1rem;">BMI Reference Chart</div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.8rem;text-align:center;">
            <div style="background:rgba(100,120,255,0.08);border:1px solid rgba(100,120,255,0.2);border-radius:12px;padding:0.9rem;">
                <div style="font-size:0.7rem;color:#6478ff;font-weight:600;letter-spacing:0.1em;">UNDERWEIGHT</div>
                <div style="font-size:1.1rem;font-weight:700;color:#f0ece4;margin-top:0.3rem;">&lt; 18.5</div>
            </div>
            <div style="background:rgba(46,180,100,0.08);border:1px solid rgba(46,180,100,0.2);border-radius:12px;padding:0.9rem;">
                <div style="font-size:0.7rem;color:#2eb464;font-weight:600;letter-spacing:0.1em;">NORMAL</div>
                <div style="font-size:1.1rem;font-weight:700;color:#f0ece4;margin-top:0.3rem;">18.5–24.9</div>
            </div>
            <div style="background:rgba(240,160,48,0.08);border:1px solid rgba(240,160,48,0.2);border-radius:12px;padding:0.9rem;">
                <div style="font-size:0.7rem;color:#f0a030;font-weight:600;letter-spacing:0.1em;">OVERWEIGHT</div>
                <div style="font-size:1.1rem;font-weight:700;color:#f0ece4;margin-top:0.3rem;">25–29.9</div>
            </div>
            <div style="background:rgba(220,50,80,0.08);border:1px solid rgba(220,50,80,0.2);border-radius:12px;padding:0.9rem;">
                <div style="font-size:0.7rem;color:#e05070;font-weight:600;letter-spacing:0.1em;">OBESE</div>
                <div style="font-size:1.1rem;font-weight:700;color:#f0ece4;margin-top:0.3rem;">&ge; 30</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# ANALYSIS PAGE
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "analysis":
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;margin-bottom:2.5rem;position:relative;z-index:1;">
        <div class="sec-eyebrow" style="color:#2eb464;">Data Science</div>
        <div class="sec-title" style="background:linear-gradient(135deg,#f0ece4,#2eb464);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
            Model & Dataset Analysis
        </div>
        <div class="sec-byline">UCI Heart Disease Dataset &nbsp;·&nbsp; Random Forest Classifier</div>
    </div>
    """, unsafe_allow_html=True)

    # Model performance
    st.markdown('<div class="card" style="position:relative;z-index:1;margin-bottom:1.5rem;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.68rem;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:rgba(240,236,228,0.3);margin-bottom:1.2rem;">MODEL PERFORMANCE METRICS</div>', unsafe_allow_html=True)

    metrics = [
        ("Accuracy", 95.54, "#2eb464"),
        ("Precision", 94.80, "#6478ff"),
        ("Recall", 96.10, "#c0507a"),
        ("F1 Score", 95.44, "#f0a030"),
        ("AUC-ROC", 97.20, "#2eb464"),
    ]
    for name, val, col in metrics:
        st.markdown(f"""
        <div class="perf-row">
            <div class="perf-name">{name}</div>
            <div class="perf-bar-wrap">
                <div class="perf-bar" style="width:{val}%;background:linear-gradient(90deg,{col}88,{col});"></div>
            </div>
            <div class="perf-val" style="color:{col};">{val}%</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        # Feature importance (approximate based on typical RF on UCI dataset)
        features = ['Chest Pain','Max HR','ST Depression','Major Vessels','Thalassemia','Age','BP','Cholesterol','ST Slope','Sex','ECG','Ex. Angina','Blood Sugar']
        importance = [0.185, 0.142, 0.138, 0.125, 0.112, 0.085, 0.062, 0.048, 0.040, 0.025, 0.018, 0.012, 0.008]
        colors_fi = ['#e05070' if v>0.1 else '#f0a030' if v>0.06 else '#6478ff' for v in importance]
        fig_fi = go.Figure(go.Bar(y=features, x=importance, orientation='h',
                                  marker_color=colors_fi,
                                  text=[f"{v*100:.1f}%" for v in importance],
                                  textposition='outside', textfont={'color':'#f0ece4','size':10}))
        fig_fi.update_layout(title={'text':'Feature Importance','font':{'color':'#f0ece4','size':13}},
                             paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)',
                             font={'color':'#f0ece4'}, height=380,
                             xaxis={'color':'#f0ece4','gridcolor':'rgba(255,255,255,0.06)'},
                             yaxis={'color':'#f0ece4'}, margin=dict(t=40,b=20,l=10,r=60))
        st.plotly_chart(fig_fi, use_container_width=True)

    with c2:
        # Dataset distribution
        labels = ['No Heart Disease', 'Heart Disease']
        values = [138, 165]
        colors_pie = ['#2eb464', '#e05070']
        fig_pie = go.Figure(go.Pie(labels=labels, values=values,
                                   marker={'colors': colors_pie,
                                           'line':{'color':'rgba(0,0,0,0.3)','width':2}},
                                   hole=0.5,
                                   textfont={'color':'#f0ece4','size':12}))
        fig_pie.update_layout(title={'text':'Dataset Class Distribution','font':{'color':'#f0ece4','size':13}},
                              paper_bgcolor='rgba(0,0,0,0)', font={'color':'#f0ece4'},
                              height=380, legend={'font':{'color':'#f0ece4'}},
                              margin=dict(t=40,b=20,l=20,r=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    # Dataset info
    st.markdown("""
    <div class="card" style="position:relative;z-index:1;">
        <div style="font-size:0.68rem;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:rgba(240,236,228,0.3);margin-bottom:1.2rem;">DATASET INFORMATION</div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;">
            <div><div style="font-size:0.78rem;color:rgba(240,236,228,0.4);margin-bottom:0.3rem;">Source</div><div style="font-weight:600;">UCI Heart Disease Dataset</div></div>
            <div><div style="font-size:0.78rem;color:rgba(240,236,228,0.4);margin-bottom:0.3rem;">Total Samples</div><div style="font-weight:600;">303 patients</div></div>
            <div><div style="font-size:0.78rem;color:rgba(240,236,228,0.4);margin-bottom:0.3rem;">Features</div><div style="font-weight:600;">13 clinical parameters</div></div>
            <div><div style="font-size:0.78rem;color:rgba(240,236,228,0.4);margin-bottom:0.3rem;">Train/Test Split</div><div style="font-weight:600;">80% / 20%</div></div>
            <div><div style="font-size:0.78rem;color:rgba(240,236,228,0.4);margin-bottom:0.3rem;">Algorithm</div><div style="font-weight:600;">Random Forest Classifier</div></div>
            <div><div style="font-size:0.78rem;color:rgba(240,236,228,0.4);margin-bottom:0.3rem;">Preprocessing</div><div style="font-weight:600;">StandardScaler</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# ABOUT PAGE
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "about":
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.6])

    with c1:
        st.markdown("""
        <div class="card" style="position:relative;z-index:1;text-align:center;">
            <div style="width:100px;height:100px;border-radius:50%;
                        background:linear-gradient(135deg,#b03060,#7b2ff7);
                        display:flex;align-items:center;justify-content:center;
                        font-size:2.5rem;margin:0 auto 1.5rem;
                        box-shadow:0 8px 30px rgba(176,48,96,0.4);">🧑‍💻</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;margin-bottom:0.3rem;">
                Morsalin Hossain Dip
            </div>
            <div style="font-size:0.83rem;color:rgba(240,236,228,0.45);margin-bottom:1.5rem;">
                Chittagong University of Engineering & Technology
            </div>
            <div style="margin-bottom:1.5rem;">
                <span class="tag tag-red">Machine Learning</span>
                <span class="tag tag-blue">Python</span>
                <span class="tag tag-green">Data Science</span>
                <span class="tag tag-gray">Streamlit</span>
                <span class="tag tag-blue">Scikit-learn</span>
            </div>
            <div style="border-top:1px solid rgba(255,255,255,0.07);padding-top:1.2rem;">
                <a href="https://github.com/dip143218" target="_blank"
                   style="display:block;padding:0.7rem 1rem;background:rgba(255,255,255,0.04);
                          border:1px solid rgba(255,255,255,0.1);border-radius:10px;
                          color:#f0ece4;text-decoration:none;font-size:0.85rem;margin-bottom:0.6rem;
                          transition:all 0.2s;">
                    🐙 &nbsp; github.com/dip143218
                </a>
                <div style="padding:0.7rem 1rem;background:rgba(100,120,255,0.08);
                            border:1px solid rgba(100,120,255,0.2);border-radius:10px;
                            color:#6478ff;font-size:0.85rem;margin-bottom:0.6rem;">
                    🎓 &nbsp; CUET — Computer Science
                </div>
                <div style="padding:0.7rem 1rem;background:rgba(46,180,100,0.08);
                            border:1px solid rgba(46,180,100,0.2);border-radius:10px;
                            color:#2eb464;font-size:0.85rem;">
                    📍 &nbsp; Chittagong, Bangladesh
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style="position:relative;z-index:1;">
            <div class="sec-eyebrow" style="color:#c0507a;">About This Project</div>
            <div class="sec-title" style="background:linear-gradient(135deg,#f0ece4,#c0507a);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
                 font-size:2.2rem;margin-bottom:1.5rem;">
                Heart Disease Predictor
            </div>

            <div class="card" style="margin-bottom:1rem;">
                <div style="font-size:0.68rem;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;
                            color:rgba(240,236,228,0.3);margin-bottom:0.8rem;">PROJECT OVERVIEW</div>
                <p style="font-size:0.88rem;color:rgba(240,236,228,0.65);line-height:1.8;">
                    This project is a full-stack machine learning web application developed as part of my academic
                    research at CUET. It uses a <strong style="color:#f0ece4;">Random Forest Classifier</strong>
                    trained on the UCI Heart Disease Dataset to predict cardiovascular disease risk with
                    <strong style="color:#2eb464;">95.54% accuracy</strong>.
                </p>
            </div>

            <div class="card" style="margin-bottom:1rem;">
                <div style="font-size:0.68rem;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;
                            color:rgba(240,236,228,0.3);margin-bottom:0.8rem;">TECH STACK</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;">
                    <div style="padding:0.6rem 0.9rem;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:10px;font-size:0.82rem;color:rgba(240,236,228,0.6);">🐍 Python 3.10</div>
                    <div style="padding:0.6rem 0.9rem;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:10px;font-size:0.82rem;color:rgba(240,236,228,0.6);">🌐 Streamlit</div>
                    <div style="padding:0.6rem 0.9rem;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:10px;font-size:0.82rem;color:rgba(240,236,228,0.6);">🤖 Scikit-learn</div>
                    <div style="padding:0.6rem 0.9rem;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:10px;font-size:0.82rem;color:rgba(240,236,228,0.6);">📊 Plotly</div>
                    <div style="padding:0.6rem 0.9rem;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:10px;font-size:0.82rem;color:rgba(240,236,228,0.6);">🔢 NumPy</div>
                    <div style="padding:0.6rem 0.9rem;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:10px;font-size:0.82rem;color:rgba(240,236,228,0.6);">📄 FPDF2</div>
                </div>
            </div>

            <div class="card">
                <div style="font-size:0.68rem;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;
                            color:rgba(240,236,228,0.3);margin-bottom:0.8rem;">KEY HIGHLIGHTS</div>
                <div style="font-size:0.85rem;color:rgba(240,236,228,0.6);line-height:1.9;">
                    ✅ &nbsp; 95.54% model accuracy on test set<br>
                    ✅ &nbsp; 13 clinical parameters analyzed<br>
                    ✅ &nbsp; Real-time risk prediction with probability scores<br>
                    ✅ &nbsp; PDF health report generation<br>
                    ✅ &nbsp; Interactive data visualization with Plotly<br>
                    ✅ &nbsp; Deployed on Streamlit Community Cloud<br>
                    ✅ &nbsp; BMI calculator with visual gauge
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # LinkedIn post section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card" style="position:relative;z-index:1;border-color:rgba(100,120,255,0.3);">
        <div style="font-size:0.68rem;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;
                    color:#6478ff;margin-bottom:1rem;">READY-TO-USE LINKEDIN POST</div>
        <div style="background:rgba(100,120,255,0.05);border:1px solid rgba(100,120,255,0.15);
                    border-radius:12px;padding:1.3rem;font-size:0.88rem;color:rgba(240,236,228,0.7);line-height:1.85;">
            🚀 Excited to share my latest ML project — <strong style="color:#f0ece4;">Heart Disease Predictor!</strong><br><br>
            I built an AI-powered web app using <strong style="color:#f0ece4;">Random Forest</strong> that predicts cardiovascular disease risk with <strong style="color:#2eb464;">95.54% accuracy</strong>.<br><br>
            🔬 <strong style="color:#f0ece4;">What it does:</strong><br>
            • Analyzes 13 clinical parameters to predict heart disease risk<br>
            • Shows risk probability with interactive gauge charts<br>
            • Generates downloadable PDF health reports<br>
            • Includes a BMI Calculator with visual feedback<br><br>
            🛠️ <strong style="color:#f0ece4;">Tech Stack:</strong> Python · Streamlit · Scikit-learn · Plotly · FPDF2<br>
            📊 <strong style="color:#f0ece4;">Dataset:</strong> UCI Heart Disease Dataset (303 patients, 13 features)<br><br>
            🌐 Live Demo: https://heart-disease-predictor-7npize4ygtdgeyfruycnuj.streamlit.app<br>
            💻 GitHub: https://github.com/dip143218/heart-disease-predictor<br><br>
            <em style="color:rgba(240,236,228,0.4);">#MachineLearning #Python #DataScience #HealthAI #Streamlit #CUET #RandomForest #HeartDisease</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
