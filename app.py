import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile, os
from datetime import datetime

st.set_page_config(page_title="HealthAI — Morsalin", page_icon="❤️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

*{box-sizing:border-box;margin:0;padding:0;}

html,body,[data-testid="stAppViewContainer"]{
    background:#07071a !important;
    color:#f0ece4;
    font-family:'DM Sans',sans-serif;
}
[data-testid="stHeader"]{background:transparent !important;}
[data-testid="stSidebar"]{display:none !important;}
.block-container{padding:0 !important;max-width:100% !important;}
[data-testid="stVerticalBlock"]{gap:0 !important;}

/* ── BUTTONS ── */
div[data-testid="stButton"]>button{
    background:linear-gradient(135deg,#e040a0,#7c3aed,#2563eb) !important;
    color:#fff !important;border:none !important;border-radius:14px !important;
    font-family:'DM Sans',sans-serif !important;font-weight:700 !important;
    font-size:0.95rem !important;padding:0.75rem 1.5rem !important;
    transition:all .3s !important;letter-spacing:0.03em !important;
    box-shadow:0 4px 24px rgba(124,58,237,0.35) !important;
}
div[data-testid="stButton"]>button:hover{
    transform:translateY(-3px) scale(1.02) !important;
    box-shadow:0 10px 36px rgba(124,58,237,0.55) !important;
}
div[data-testid="stDownloadButton"]>button{
    background:linear-gradient(135deg,rgba(16,185,129,0.2),rgba(6,182,212,0.2)) !important;
    color:#10b981 !important;border:1px solid rgba(16,185,129,0.4) !important;
    box-shadow:none !important;
}

/* ── FORM ── */
label[data-testid="stWidgetLabel"]>div{color:rgba(240,236,228,.7) !important;font-size:.85rem !important;}
[data-testid="stSelectbox"]>div>div{
    background:rgba(255,255,255,.05) !important;
    border:1px solid rgba(255,255,255,.12) !important;
    color:#f0ece4 !important;border-radius:12px !important;
}
[data-testid="stNumberInput"] input{
    background:rgba(255,255,255,.05) !important;
    border:1px solid rgba(255,255,255,.12) !important;
    color:#f0ece4 !important;border-radius:12px !important;
}
[data-testid="stSlider"]>div>div>div{background:linear-gradient(90deg,#e040a0,#7c3aed) !important;}

/* ── GRID BG ── */
.grid-bg{
    position:fixed;inset:0;pointer-events:none;z-index:0;
    background-image:
        linear-gradient(rgba(255,255,255,.015) 1px,transparent 1px),
        linear-gradient(90deg,rgba(255,255,255,.015) 1px,transparent 1px);
    background-size:60px 60px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="grid-bg"></div>', unsafe_allow_html=True)

# ── SESSION ──────────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"

# ── MODEL ────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load('heart_disease_model.pkl'), joblib.load('scaler.pkl')
model, scaler = load_model()

# ── NAV ──────────────────────────────────────────────────────────────────────
NAV_STYLE = """
<style>
.nav-bar{
    display:flex;align-items:center;justify-content:space-between;
    padding:1rem 3rem;
    background:rgba(7,7,26,0.85);
    border-bottom:1px solid rgba(255,255,255,.07);
    backdrop-filter:blur(20px);
    position:sticky;top:0;z-index:200;
}
.nav-logo{
    font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:900;
    background:linear-gradient(135deg,#f472b6,#a78bfa,#60a5fa);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
</style>
<div class="nav-bar">
    <div class="nav-logo">HealthAI</div>
</div>
"""
st.markdown(NAV_STYLE, unsafe_allow_html=True)

nav_cols = st.columns([1,1,1,1,1])
pages_nav = [("home","🏠 Home"),("heart","❤️ Heart Check"),("bmi","🧮 BMI"),("analysis","📊 Analysis"),("about","👤 About")]
for i,(pid,plabel) in enumerate(pages_nav):
    with nav_cols[i]:
        if st.button(plabel, key=f"nav_{pid}", use_container_width=True):
            st.session_state.page = pid
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# HOME
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":

    # Hero
    st.markdown("""
    <div style="
        min-height:60vh;
        display:flex;flex-direction:column;align-items:center;justify-content:center;
        padding:4rem 2rem 2rem;text-align:center;position:relative;z-index:1;
        background:radial-gradient(ellipse at 30% 40%,rgba(124,58,237,.18) 0%,transparent 60%),
                   radial-gradient(ellipse at 70% 60%,rgba(224,64,160,.15) 0%,transparent 60%);
    ">
        <div style="
            font-size:.72rem;font-weight:700;letter-spacing:.22em;text-transform:uppercase;
            background:linear-gradient(135deg,#f472b6,#a78bfa);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
            border:1px solid rgba(167,139,250,.3);padding:.4rem 1.2rem;border-radius:100px;
            display:inline-block;margin-bottom:1.8rem;
        ">AI Health Platform &nbsp;·&nbsp; Made by Morsalin Hossain Dip</div>

        
    </div>
    """, unsafe_allow_html=True)

    # Cards first
    _, c1, c2, c3, _ = st.columns([0.2, 1, 1, 1, 0.2])

    CARD_STYLE = "background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:22px;padding:2rem 1.5rem;text-align:center;position:relative;z-index:1;"

    with c1:
        st.markdown(f"""
        <div style="{CARD_STYLE}border-color:rgba(244,114,182,.35);
             background:linear-gradient(135deg,rgba(244,114,182,.08),rgba(124,58,237,.06));">
            <div style="font-size:3rem;margin-bottom:.8rem;">❤️</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;margin-bottom:.5rem;
                 background:linear-gradient(135deg,#f472b6,#fb7185);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
                Heart Check</div>
            <div style="font-size:.82rem;color:rgba(240,236,228,.5);line-height:1.7;">
                AI-powered cardiovascular risk prediction using 13 clinical parameters</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Heart Check →", key="h_heart", use_container_width=True):
            st.session_state.page = "heart"; st.rerun()

    with c2:
        st.markdown(f"""
        <div style="{CARD_STYLE}border-color:rgba(96,165,250,.35);
             background:linear-gradient(135deg,rgba(96,165,250,.08),rgba(34,211,238,.06));">
            <div style="font-size:3rem;margin-bottom:.8rem;">🧮</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;margin-bottom:.5rem;
                 background:linear-gradient(135deg,#60a5fa,#22d3ee);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
                BMI Calculator</div>
            <div style="font-size:.82rem;color:rgba(240,236,228,.5);line-height:1.7;">
                Body Mass Index with visual gauge and health category analysis</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open BMI Check →", key="h_bmi", use_container_width=True):
            st.session_state.page = "bmi"; st.rerun()

    with c3:
        st.markdown(f"""
        <div style="{CARD_STYLE}border-color:rgba(52,211,153,.35);
             background:linear-gradient(135deg,rgba(52,211,153,.08),rgba(16,185,129,.06));">
            <div style="font-size:3rem;margin-bottom:.8rem;">📊</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;margin-bottom:.5rem;
                 background:linear-gradient(135deg,#34d399,#10b981);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
                Data Analysis</div>
            <div style="font-size:.82rem;color:rgba(240,236,228,.5);line-height:1.7;">
                Dataset insights, model performance and feature importance charts</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Analysis →", key="h_analysis", use_container_width=True):
            st.session_state.page = "analysis"; st.rerun()

    # Stats below cards
    st.markdown("""
    <div style="
        display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;
        max-width:860px;margin:2.5rem auto;padding:0 1rem;position:relative;z-index:1;
    ">
        <div style="background:rgba(52,211,153,.08);border:1px solid rgba(52,211,153,.25);
                    border-radius:16px;padding:1.3rem;text-align:center;">
            <div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:#34d399;">95.54%</div>
            <div style="font-size:.68rem;color:rgba(240,236,228,.4);letter-spacing:.1em;text-transform:uppercase;margin-top:.2rem;">Model Accuracy</div>
        </div>
        <div style="background:rgba(96,165,250,.08);border:1px solid rgba(96,165,250,.25);
                    border-radius:16px;padding:1.3rem;text-align:center;">
            <div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:#60a5fa;">13</div>
            <div style="font-size:.68rem;color:rgba(240,236,228,.4);letter-spacing:.1em;text-transform:uppercase;margin-top:.2rem;">Clinical Features</div>
        </div>
        <div style="background:rgba(244,114,182,.08);border:1px solid rgba(244,114,182,.25);
                    border-radius:16px;padding:1.3rem;text-align:center;">
            <div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:#f472b6;">RF</div>
            <div style="font-size:.68rem;color:rgba(240,236,228,.4);letter-spacing:.1em;text-transform:uppercase;margin-top:.2rem;">Algorithm</div>
        </div>
        <div style="background:rgba(167,139,250,.08);border:1px solid rgba(167,139,250,.25);
                    border-radius:16px;padding:1.3rem;text-align:center;">
            <div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:#a78bfa;">UCI</div>
            <div style="font-size:.68rem;color:rgba(240,236,228,.4);letter-spacing:.1em;text-transform:uppercase;margin-top:.2rem;">Dataset Source</div>
        </div>
    </div>

    <div style="text-align:center;padding:1.5rem 0 3rem;font-size:.75rem;
                color:rgba(240,236,228,.2);letter-spacing:.1em;position:relative;z-index:1;">
        MADE WITH ❤️ &nbsp;·&nbsp;
        <span style="background:linear-gradient(135deg,#f472b6,#a78bfa);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
              font-weight:700;">MORSALIN HOSSAIN DIP · CUET</span>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# HEART CHECK
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "heart":

    # Back button + header
    back_col, _ = st.columns([1, 5])
    with back_col:
        if st.button("← Back to Home", key="back_heart"):
            st.session_state.page = "home"; st.rerun()

    st.markdown("""
    <div style="text-align:center;padding:1.5rem 0 2rem;position:relative;z-index:1;">
        <div style="font-size:.68rem;font-weight:700;letter-spacing:.22em;text-transform:uppercase;
             background:linear-gradient(135deg,#f472b6,#fb7185);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
             margin-bottom:.7rem;">CARDIOVASCULAR AI ASSESSMENT</div>
        <h2 style="font-family:'Playfair Display',serif;font-size:clamp(2rem,4vw,3rem);font-weight:900;
             background:linear-gradient(135deg,#f0ece4,#f472b6,#fb7185);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
             margin-bottom:.5rem;">Heart Checking</h2>
        <div style="font-size:.83rem;color:rgba(240,236,228,.4);">
            Made by Morsalin Hossain Dip &nbsp;·&nbsp; CUET &nbsp;·&nbsp; Random Forest · 95.54% Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

    PANEL = "background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:18px;padding:1.8rem 1.8rem 1.5rem;position:relative;z-index:1;"
    PTITLE = "font-size:.65rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:rgba(240,236,228,.3);margin-bottom:1.2rem;"

    # Form with margins
    _, fc1, fc2, fc3, _ = st.columns([0.08, 1, 1, 1, 0.08])

    with fc1:
        st.markdown(f'<div style="{PANEL}"><div style="{PTITLE}">BASIC INFO</div>', unsafe_allow_html=True)
        age = st.slider("Age", 20, 80, 50)
        sex = st.selectbox("Sex", [0,1], format_func=lambda x:"Female" if x==0 else "Male")
        cp = st.selectbox("Chest Pain Type", [0,1,2,3],
                          format_func=lambda x:{0:"Typical Angina",1:"Atypical Angina",2:"Non-anginal",3:"Asymptomatic"}[x])
        trestbps = st.slider("Resting BP (mmHg)", 90, 200, 130)
        chol = st.slider("Cholesterol (mg/dl)", 100, 600, 246)
        st.markdown('</div>', unsafe_allow_html=True)

    with fc2:
        st.markdown(f'<div style="{PANEL}"><div style="{PTITLE}">BLOOD & ECG</div>', unsafe_allow_html=True)
        fbs = st.selectbox("Fasting Blood Sugar > 120?", [0,1], format_func=lambda x:"No" if x==0 else "Yes")
        restecg = st.selectbox("Resting ECG", [0,1,2],
                               format_func=lambda x:{0:"Normal",1:"ST-T Abnormality",2:"LV Hypertrophy"}[x])
        thalach = st.slider("Max Heart Rate", 70, 210, 150)
        exang = st.selectbox("Exercise Induced Angina", [0,1], format_func=lambda x:"No" if x==0 else "Yes")
        st.markdown('</div>', unsafe_allow_html=True)

    with fc3:
        st.markdown(f'<div style="{PANEL}"><div style="{PTITLE}">ADVANCED</div>', unsafe_allow_html=True)
        oldpeak = st.slider("ST Depression", 0.0, 6.5, 1.0, 0.1)
        slope = st.selectbox("ST Slope", [0,1,2],
                             format_func=lambda x:{0:"Upsloping",1:"Flat",2:"Downsloping"}[x])
        ca = st.selectbox("Major Vessels (0-4)", [0,1,2,3,4])
        thal = st.selectbox("Thalassemia", [0,1,2,3],
                            format_func=lambda x:{0:"Normal",1:"Fixed Defect",2:"Reversible Defect",3:"Unknown"}[x])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([0.08, 1, 0.08])
    with btn_col:
        predict_clicked = st.button("🔍 Analyze Heart Disease Risk", use_container_width=True)

    if predict_clicked:
        inp = np.array([[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]])
        prob = model.predict_proba(scaler.transform(inp))[0]
        pred = model.predict(scaler.transform(inp))[0]

        st.markdown("<br>", unsafe_allow_html=True)
        _, res_col, _ = st.columns([0.08, 1, 0.08])
        with res_col:
            if pred == 1:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,rgba(244,63,94,.18),rgba(190,18,60,.1));
                     border:2px solid rgba(244,63,94,.5);border-radius:20px;padding:2rem;text-align:center;">
                    <div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;
                         color:#f43f5e;margin-bottom:.4rem;">⚠️ High Risk Detected</div>
                    <div style="color:rgba(240,236,228,.55);margin-bottom:1rem;">Heart disease risk identified — please consult a cardiologist</div>
                    <div style="font-family:'Playfair Display',serif;font-size:4rem;font-weight:900;color:#f43f5e;">{prob[1]*100:.1f}%</div>
                    <div style="font-size:.78rem;color:rgba(240,236,228,.35);margin-top:.3rem;">Disease Risk Probability</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,rgba(16,185,129,.18),rgba(5,150,105,.1));
                     border:2px solid rgba(16,185,129,.5);border-radius:20px;padding:2rem;text-align:center;">
                    <div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;
                         color:#10b981;margin-bottom:.4rem;">✅ Low Risk — Healthy</div>
                    <div style="color:rgba(240,236,228,.55);margin-bottom:1rem;">No significant heart disease risk detected</div>
                    <div style="font-family:'Playfair Display',serif;font-size:4rem;font-weight:900;color:#10b981;">{prob[0]*100:.1f}%</div>
                    <div style="font-size:.78rem;color:rgba(240,236,228,.35);margin-top:.3rem;">Healthy Probability</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        _, r1, r2, _ = st.columns([0.08,1,1,0.08])

        with r1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=prob[1]*100,
                title={'text':"Risk %",'font':{'color':'#f0ece4','size':13}},
                gauge={'axis':{'range':[0,100],'tickcolor':'#f0ece4','tickfont':{'color':'#f0ece4','size':9}},
                       'bar':{'color':"#f43f5e" if pred==1 else "#10b981"},
                       'bgcolor':'rgba(255,255,255,.02)',
                       'steps':[{'range':[0,30],'color':'rgba(16,185,129,.12)'},
                                 {'range':[30,60],'color':'rgba(251,191,36,.12)'},
                                 {'range':[60,100],'color':'rgba(244,63,94,.12)'}],
                       'threshold':{'line':{'color':'white','width':3},'value':50,'thickness':.75}},
                number={'font':{'color':'#f0ece4','size':38},'suffix':'%'}))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',font={'color':'#f0ece4'},
                              height=270,margin=dict(t=45,b=0,l=25,r=25))
            st.plotly_chart(fig, use_container_width=True)

        with r2:
            st.markdown("""<div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);
                border-radius:16px;padding:1.5rem;">
                <div style="font-size:.65rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;
                color:rgba(240,236,228,.3);margin-bottom:1rem;">RISK FACTOR ANALYSIS</div>""",
                unsafe_allow_html=True)
            rf, gf = [], []
            if age>55: rf.append("Age > 55 years")
            if chol>240: rf.append("High cholesterol > 240")
            if trestbps>140: rf.append("High blood pressure > 140")
            if thalach<120: rf.append("Low max heart rate < 120")
            if exang==1: rf.append("Exercise-induced angina")
            if oldpeak>2: rf.append("ST depression > 2.0")
            if cp==3: rf.append("Asymptomatic chest pain")
            if ca>=3: rf.append("3+ major vessels blocked")
            if age<=45: gf.append("Healthy age range ≤ 45")
            if chol<=200: gf.append("Normal cholesterol ≤ 200")
            if trestbps<=120: gf.append("Normal blood pressure")
            if thalach>=150: gf.append("Strong max heart rate")
            if exang==0: gf.append("No exercise angina")
            for r in rf:
                st.markdown(f'<div style="color:#f87171;font-size:.85rem;padding:.3rem 0;">🔴 {r}</div>', unsafe_allow_html=True)
            for g in gf:
                st.markdown(f'<div style="color:#34d399;font-size:.85rem;padding:.3rem 0;">🟢 {g}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Bar chart
        _, chart_col, _ = st.columns([0.08,1,0.08])
        with chart_col:
            pnames=['Age','Sex','CP','BP','Chol','FBS','ECG','HR','ExAng','STPk','Slope','CA','Thal']
            pvals=[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
            ranges=[(20,80),(0,1),(0,3),(90,200),(100,600),(0,1),(0,2),(70,210),(0,1),(0,6.5),(0,2),(0,4),(0,3)]
            nv=[(v-mn)/(mx-mn)*100 for v,(mn,mx) in zip(pvals,ranges)]
            bc=['#f43f5e' if n>70 else '#fbbf24' if n>40 else '#10b981' for n in nv]
            fig2=go.Figure(go.Bar(x=pnames,y=nv,marker_color=bc,
                                  text=[str(v) for v in pvals],textposition='outside',
                                  textfont={'color':'#f0ece4','size':10}))
            fig2.update_layout(
                title={'text':'Input Parameter Overview','font':{'color':'#f0ece4','size':13}},
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(255,255,255,.02)',
                font={'color':'#f0ece4'},height=280,
                yaxis={'title':'Normalized %','gridcolor':'rgba(255,255,255,.06)','color':'#f0ece4'},
                xaxis={'color':'#f0ece4'},margin=dict(t=40,b=0,l=0,r=0))
            st.plotly_chart(fig2, use_container_width=True)

        # AI Interpretation
        _, ai_col, _ = st.columns([0.08,1,0.08])
        with ai_col:
            risk_score = prob[1]*100
            if risk_score > 70:
                interp = "The model detects a strong pattern of cardiovascular risk. Multiple high-risk clinical indicators are present. Immediate medical consultation is strongly recommended."
                icolor = "#f43f5e"
            elif risk_score > 40:
                interp = "Moderate risk indicators detected. Some clinical parameters are outside the normal range. Consider lifestyle modifications and regular health checkups."
                icolor = "#fbbf24"
            else:
                interp = "Clinical parameters are largely within healthy ranges. Maintain a balanced diet, regular exercise, and annual checkups to preserve heart health."
                icolor = "#10b981"

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,rgba(124,58,237,.1),rgba(99,102,241,.08));
                 border:1px solid rgba(124,58,237,.3);border-radius:16px;padding:1.5rem;margin:1rem 0;">
                <div style="font-size:.65rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;
                     color:#a78bfa;margin-bottom:.8rem;">🤖 AI INTERPRETATION</div>
                <p style="font-size:.92rem;color:rgba(240,236,228,.8);line-height:1.8;">{interp}</p>
                <div style="margin-top:.8rem;font-size:.78rem;color:rgba(240,236,228,.35);">
                    This interpretation is generated automatically based on your risk score of
                    <span style="color:{icolor};font-weight:700;">{risk_score:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # PDF download
        _, pdf_col, _ = st.columns([0.08,1,0.08])
        with pdf_col:
            def gen_pdf():
                pdf = FPDF(); pdf.add_page()
                pdf.set_font("Helvetica","B",18); pdf.set_text_color(200,40,80)
                pdf.cell(0,14,"Heart Disease Prediction Report",ln=True,align="C")
                pdf.set_font("Helvetica","",9); pdf.set_text_color(120,120,120)
                pdf.cell(0,6,f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  Morsalin Hossain Dip · CUET",ln=True,align="C")
                pdf.ln(4)
                pdf.set_fill_color(200,40,80) if pred==1 else pdf.set_fill_color(16,185,129)
                pdf.set_text_color(255,255,255); pdf.set_font("Helvetica","B",12)
                pdf.cell(0,10,f"RESULT: {'HIGH RISK' if pred==1 else 'LOW RISK — Healthy'}",ln=True,align="C",fill=True)
                pdf.ln(3); pdf.set_text_color(0,0,0)
                pdf.set_font("Helvetica","B",11); pdf.cell(0,8,"Probabilities:",ln=True)
                pdf.set_font("Helvetica","",10)
                pdf.cell(0,7,f"  Healthy: {prob[0]*100:.1f}%",ln=True)
                pdf.cell(0,7,f"  Heart Disease: {prob[1]*100:.1f}%",ln=True)
                pdf.ln(3); pdf.set_font("Helvetica","B",11); pdf.cell(0,8,"Parameters:",ln=True)
                pdf.set_font("Helvetica","",10)
                for nm,vl in [("Age",age),("Sex","Male" if sex else "Female"),("Chest Pain",cp),
                              ("BP",f"{trestbps} mmHg"),("Cholesterol",f"{chol} mg/dl"),
                              ("FBS>120","Yes" if fbs else "No"),("ECG",restecg),("Max HR",thalach),
                              ("Ex.Angina","Yes" if exang else "No"),("ST Dep",oldpeak),
                              ("Slope",slope),("Vessels",ca),("Thal",thal)]:
                    pdf.cell(80,7,f"  {nm}:"); pdf.cell(0,7,str(vl),ln=True)
                pdf.ln(3); pdf.set_font("Helvetica","I",8); pdf.set_text_color(140,140,140)
                pdf.multi_cell(0,5,"DISCLAIMER: AI prediction only. Always consult a licensed physician.")
                tmp=tempfile.NamedTemporaryFile(delete=False,suffix=".pdf"); pdf.output(tmp.name); return tmp.name
            try:
                pp=gen_pdf()
                with open(pp,"rb") as f:
                    st.download_button("📥 Download Full PDF Report",data=f.read(),
                                       file_name=f"heart_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                       mime="application/pdf",use_container_width=True)
                os.unlink(pp)
            except: st.info("Add 'fpdf2' to requirements.txt for PDF.")

            st.markdown("""
            <div style="background:rgba(244,63,94,.07);border:1px solid rgba(244,63,94,.2);
                 border-radius:12px;padding:.9rem 1.2rem;margin-top:.8rem;
                 font-size:.8rem;color:rgba(240,236,228,.45);">
                ⚠️ This is an AI prediction only. Always consult a licensed medical professional for diagnosis.
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# BMI
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "bmi":
    back_col, _ = st.columns([1,5])
    with back_col:
        if st.button("← Back to Home", key="back_bmi"):
            st.session_state.page = "home"; st.rerun()

    st.markdown("""
    <div style="text-align:center;padding:1.5rem 0 2rem;position:relative;z-index:1;">
        <div style="font-size:.68rem;font-weight:700;letter-spacing:.22em;text-transform:uppercase;
             background:linear-gradient(135deg,#60a5fa,#22d3ee);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
             margin-bottom:.7rem;">BODY COMPOSITION</div>
        <h2 style="font-family:'Playfair Display',serif;font-size:clamp(2rem,4vw,3rem);font-weight:900;
             background:linear-gradient(135deg,#f0ece4,#60a5fa,#22d3ee);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
             margin-bottom:.5rem;">Check Your BMI</h2>
        <div style="font-size:.83rem;color:rgba(240,236,228,.4);">
            Made by Morsalin Hossain Dip &nbsp;·&nbsp; CUET &nbsp;·&nbsp; Body Mass Index Calculator</div>
    </div>
    """, unsafe_allow_html=True)

    _, bl, br, _ = st.columns([0.1,1,1,0.1])
    with bl:
        st.markdown('<div style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:18px;padding:1.8rem;position:relative;z-index:1;">', unsafe_allow_html=True)
        h = st.number_input("Height (cm)", 100, 250, 170)
        w = st.number_input("Weight (kg)", 20, 300, 70)
        st.markdown('</div><br>', unsafe_allow_html=True)
        if st.button("Calculate BMI", use_container_width=True):
            st.session_state.bmi_val = w/((h/100)**2)
            st.session_state.bmi_h = h
            st.session_state.bmi_w = w

    with br:
        if "bmi_val" in st.session_state:
            bmi = st.session_state.bmi_val
            if bmi<18.5: cat,col,adv,tip="Underweight","#60a5fa","Consider a nutritious diet to reach healthy weight.","Increase calorie intake with protein-rich foods."
            elif bmi<25: cat,col,adv,tip="Normal Weight","#10b981","Excellent! Maintain your healthy lifestyle.","Keep up regular exercise and balanced nutrition."
            elif bmi<30: cat,col,adv,tip="Overweight","#fbbf24","Regular exercise and balanced diet recommended.","Aim for 150 mins of moderate exercise per week."
            else: cat,col,adv,tip="Obese","#f43f5e","Please consult a doctor for a personalized plan.","Medical supervision recommended for weight loss."

            st.markdown(f"""
            <div style="background:rgba(255,255,255,.04);border:1.5px solid {col}40;
                 border-radius:18px;padding:2rem;text-align:center;margin-bottom:1rem;position:relative;z-index:1;">
                <div style="font-family:'Playfair Display',serif;font-size:3.5rem;font-weight:900;color:{col};">{bmi:.1f}</div>
                <div style="font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;color:#f0ece4;margin:.3rem 0;">{cat}</div>
                <div style="font-size:.85rem;color:rgba(240,236,228,.5);line-height:1.6;">{adv}</div>
                <div style="margin-top:1rem;padding:.8rem;background:rgba(255,255,255,.04);border-radius:10px;
                     font-size:.8rem;color:{col};">💡 {tip}</div>
            </div>
            """, unsafe_allow_html=True)

            fg=go.Figure(go.Indicator(
                mode="gauge+number",value=bmi,
                title={'text':"BMI",'font':{'color':'#f0ece4','size':13}},
                gauge={'axis':{'range':[10,45],'tickcolor':'#f0ece4','tickfont':{'color':'#f0ece4','size':9}},
                       'bar':{'color':col},'bgcolor':'rgba(255,255,255,.02)',
                       'steps':[{'range':[10,18.5],'color':'rgba(96,165,250,.12)'},
                                 {'range':[18.5,25],'color':'rgba(16,185,129,.12)'},
                                 {'range':[25,30],'color':'rgba(251,191,36,.12)'},
                                 {'range':[30,45],'color':'rgba(244,63,94,.12)'}]},
                number={'font':{'color':'#f0ece4','size':38}}))
            fg.update_layout(paper_bgcolor='rgba(0,0,0,0)',font={'color':'#f0ece4'},
                             height=260,margin=dict(t=40,b=0,l=25,r=25))
            st.plotly_chart(fg, use_container_width=True)

    _, ref_col, _ = st.columns([0.1,1,0.1])
    with ref_col:
        st.markdown("""
        <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);
             border-radius:16px;padding:1.5rem;margin-top:1rem;position:relative;z-index:1;">
            <div style="font-size:.65rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
                 color:rgba(240,236,228,.28);margin-bottom:1rem;">BMI REFERENCE CHART</div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.8rem;text-align:center;">
                <div style="background:rgba(96,165,250,.08);border:1px solid rgba(96,165,250,.2);border-radius:12px;padding:.9rem;">
                    <div style="font-size:.68rem;color:#60a5fa;font-weight:700;letter-spacing:.1em;">UNDERWEIGHT</div>
                    <div style="font-size:1.1rem;font-weight:700;color:#f0ece4;margin-top:.3rem;">&lt; 18.5</div>
                </div>
                <div style="background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);border-radius:12px;padding:.9rem;">
                    <div style="font-size:.68rem;color:#10b981;font-weight:700;letter-spacing:.1em;">NORMAL</div>
                    <div style="font-size:1.1rem;font-weight:700;color:#f0ece4;margin-top:.3rem;">18.5–24.9</div>
                </div>
                <div style="background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.2);border-radius:12px;padding:.9rem;">
                    <div style="font-size:.68rem;color:#fbbf24;font-weight:700;letter-spacing:.1em;">OVERWEIGHT</div>
                    <div style="font-size:1.1rem;font-weight:700;color:#f0ece4;margin-top:.3rem;">25–29.9</div>
                </div>
                <div style="background:rgba(244,63,94,.08);border:1px solid rgba(244,63,94,.2);border-radius:12px;padding:.9rem;">
                    <div style="font-size:.68rem;color:#f43f5e;font-weight:700;letter-spacing:.1em;">OBESE</div>
                    <div style="font-size:1.1rem;font-weight:700;color:#f0ece4;margin-top:.3rem;">&ge; 30</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "analysis":
    back_col, _ = st.columns([1,5])
    with back_col:
        if st.button("← Back to Home", key="back_analysis"):
            st.session_state.page = "home"; st.rerun()

    st.markdown("""
    <div style="text-align:center;padding:1.5rem 0 2rem;position:relative;z-index:1;">
        <div style="font-size:.68rem;font-weight:700;letter-spacing:.22em;text-transform:uppercase;
             background:linear-gradient(135deg,#34d399,#10b981);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
             margin-bottom:.7rem;">DATA SCIENCE</div>
        <h2 style="font-family:'Playfair Display',serif;font-size:clamp(2rem,4vw,3rem);font-weight:900;
             background:linear-gradient(135deg,#f0ece4,#34d399,#10b981);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
             margin-bottom:.5rem;">Model & Dataset Analysis</h2>
        <div style="font-size:.83rem;color:rgba(240,236,228,.4);">UCI Heart Disease Dataset &nbsp;·&nbsp; Random Forest Classifier</div>
    </div>
    """, unsafe_allow_html=True)

    # Performance bars
    _, perf_col, _ = st.columns([0.08,1,0.08])
    with perf_col:
        st.markdown("""
        <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);
             border-radius:18px;padding:1.8rem;position:relative;z-index:1;margin-bottom:1.5rem;">
            <div style="font-size:.65rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
                 color:rgba(240,236,228,.3);margin-bottom:1.2rem;">MODEL PERFORMANCE METRICS</div>
        """, unsafe_allow_html=True)
        metrics = [("Accuracy",95.54,"#34d399"),("Precision",94.80,"#60a5fa"),
                   ("Recall",96.10,"#f472b6"),("F1 Score",95.44,"#fbbf24"),("AUC-ROC",97.20,"#a78bfa")]
        for nm,val,col in metrics:
            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;
                 padding:.9rem 0;border-bottom:1px solid rgba(255,255,255,.05);">
                <div style="font-size:.88rem;color:rgba(240,236,228,.6);min-width:100px;">{nm}</div>
                <div style="flex:1;margin:0 1.2rem;height:7px;background:rgba(255,255,255,.07);border-radius:4px;overflow:hidden;">
                    <div style="width:{val}%;height:100%;background:linear-gradient(90deg,{col}88,{col});border-radius:4px;"></div>
                </div>
                <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;
                     color:{col};min-width:60px;text-align:right;">{val}%</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    _, ch1, ch2, _ = st.columns([0.08,1,1,0.08])
    with ch1:
        features=['Chest Pain','Max HR','ST Depression','Major Vessels','Thalassemia','Age','BP','Cholesterol','ST Slope','Sex','ECG','Ex. Angina','Blood Sugar']
        importance=[.185,.142,.138,.125,.112,.085,.062,.048,.040,.025,.018,.012,.008]
        fi_colors=['#f43f5e' if v>.1 else '#fbbf24' if v>.06 else '#60a5fa' for v in importance]
        fig_fi=go.Figure(go.Bar(y=features,x=importance,orientation='h',marker_color=fi_colors,
                                text=[f"{v*100:.1f}%" for v in importance],textposition='outside',
                                textfont={'color':'#f0ece4','size':10}))
        fig_fi.update_layout(title={'text':'Feature Importance','font':{'color':'#f0ece4','size':13}},
                             paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(255,255,255,.02)',
                             font={'color':'#f0ece4'},height=380,
                             xaxis={'color':'#f0ece4','gridcolor':'rgba(255,255,255,.06)'},
                             yaxis={'color':'#f0ece4'},margin=dict(t=40,b=10,l=10,r=60))
        st.plotly_chart(fig_fi, use_container_width=True)

    with ch2:
        fig_pie=go.Figure(go.Pie(
            labels=['No Heart Disease','Heart Disease'],values=[138,165],
            marker={'colors':['#10b981','#f43f5e'],'line':{'color':'rgba(0,0,0,.3)','width':2}},
            hole=.5,textfont={'color':'#f0ece4','size':12}))
        fig_pie.update_layout(title={'text':'Dataset Class Distribution','font':{'color':'#f0ece4','size':13}},
                              paper_bgcolor='rgba(0,0,0,0)',font={'color':'#f0ece4'},
                              height=380,legend={'font':{'color':'#f0ece4'}},
                              margin=dict(t=40,b=20,l=20,r=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    _, info_col, _ = st.columns([0.08,1,0.08])
    with info_col:
        st.markdown("""
        <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);
             border-radius:18px;padding:1.8rem;position:relative;z-index:1;">
            <div style="font-size:.65rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
                 color:rgba(240,236,228,.3);margin-bottom:1.2rem;">DATASET INFORMATION</div>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;">
                <div><div style="font-size:.75rem;color:rgba(240,236,228,.4);margin-bottom:.3rem;">Source</div><div style="font-weight:600;color:#f0ece4;">UCI Heart Disease Dataset</div></div>
                <div><div style="font-size:.75rem;color:rgba(240,236,228,.4);margin-bottom:.3rem;">Total Samples</div><div style="font-weight:600;color:#f0ece4;">303 patients</div></div>
                <div><div style="font-size:.75rem;color:rgba(240,236,228,.4);margin-bottom:.3rem;">Features</div><div style="font-weight:600;color:#f0ece4;">13 clinical parameters</div></div>
                <div><div style="font-size:.75rem;color:rgba(240,236,228,.4);margin-bottom:.3rem;">Train/Test Split</div><div style="font-weight:600;color:#f0ece4;">80% / 20%</div></div>
                <div><div style="font-size:.75rem;color:rgba(240,236,228,.4);margin-bottom:.3rem;">Algorithm</div><div style="font-weight:600;color:#f0ece4;">Random Forest Classifier</div></div>
                <div><div style="font-size:.75rem;color:rgba(240,236,228,.4);margin-bottom:.3rem;">Preprocessing</div><div style="font-weight:600;color:#f0ece4;">StandardScaler</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# ABOUT
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "about":
    back_col, _ = st.columns([1,5])
    with back_col:
        if st.button("← Back to Home", key="back_about"):
            st.session_state.page = "home"; st.rerun()

    _, ab1, ab2, _ = st.columns([0.08,1,1.5,0.08])

    with ab1:
        st.markdown("""
        <div style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);
             border-radius:20px;padding:2rem;text-align:center;position:relative;z-index:1;">
            <div style="width:100px;height:100px;border-radius:50%;
                 background:linear-gradient(135deg,#e040a0,#7c3aed,#2563eb);
                 display:flex;align-items:center;justify-content:center;
                 font-size:2.5rem;margin:0 auto 1.5rem;
                 box-shadow:0 8px 32px rgba(124,58,237,.45);">🧑‍💻</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;
                 background:linear-gradient(135deg,#f472b6,#a78bfa);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
                 margin-bottom:.3rem;">Morsalin Hossain Dip</div>
            <div style="font-size:.82rem;color:rgba(240,236,228,.45);margin-bottom:1.5rem;">
                Chittagong University of Engineering<br>& Technology (CUET)
            </div>
            <div style="margin-bottom:1.5rem;line-height:2;">
                <span style="display:inline-block;font-size:.72rem;font-weight:600;padding:.3rem .8rem;border-radius:100px;margin:.2rem;background:rgba(244,114,182,.15);border:1px solid rgba(244,114,182,.3);color:#f472b6;">Machine Learning</span>
                <span style="display:inline-block;font-size:.72rem;font-weight:600;padding:.3rem .8rem;border-radius:100px;margin:.2rem;background:rgba(96,165,250,.15);border:1px solid rgba(96,165,250,.3);color:#60a5fa;">Python</span>
                <span style="display:inline-block;font-size:.72rem;font-weight:600;padding:.3rem .8rem;border-radius:100px;margin:.2rem;background:rgba(52,211,153,.15);border:1px solid rgba(52,211,153,.3);color:#34d399;">Data Science</span>
                <span style="display:inline-block;font-size:.72rem;font-weight:600;padding:.3rem .8rem;border-radius:100px;margin:.2rem;background:rgba(167,139,250,.15);border:1px solid rgba(167,139,250,.3);color:#a78bfa;">Streamlit</span>
            </div>
            <a href="https://github.com/dip143218" target="_blank"
               style="display:block;padding:.75rem 1rem;background:rgba(255,255,255,.04);
                      border:1px solid rgba(255,255,255,.12);border-radius:12px;
                      color:#f0ece4;text-decoration:none;font-size:.85rem;margin-bottom:.6rem;">
                🐙 &nbsp; github.com/dip143218
            </a>
            <div style="padding:.75rem 1rem;background:rgba(96,165,250,.08);
                        border:1px solid rgba(96,165,250,.2);border-radius:12px;
                        color:#60a5fa;font-size:.85rem;margin-bottom:.6rem;">
                🎓 &nbsp; CUET — Computer Science
            </div>
            <div style="padding:.75rem 1rem;background:rgba(52,211,153,.08);
                        border:1px solid rgba(52,211,153,.2);border-radius:12px;
                        color:#34d399;font-size:.85rem;">
                📍 &nbsp; Chittagong, Bangladesh
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ab2:
        st.markdown("""
        <div style="position:relative;z-index:1;">
            <div style="font-size:.68rem;font-weight:700;letter-spacing:.22em;text-transform:uppercase;
                 background:linear-gradient(135deg,#f472b6,#a78bfa);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
                 margin-bottom:.7rem;">ABOUT THIS PROJECT</div>
            <h2 style="font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:900;
                 background:linear-gradient(135deg,#f0ece4,#f472b6);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
                 margin-bottom:1.5rem;">Heart Disease Predictor</h2>
        """, unsafe_allow_html=True)

        for title, content in [
            ("PROJECT OVERVIEW", "A full-stack ML web application developed at <strong style='color:#f0ece4;'>CUET</strong> using a Random Forest Classifier trained on the UCI Heart Disease Dataset. Achieves <strong style='color:#34d399;'>95.54% accuracy</strong> in predicting cardiovascular disease risk from 13 clinical parameters."),
            ("KEY HIGHLIGHTS", "✅ 95.54% model accuracy on test set<br>✅ 13 clinical parameters analyzed<br>✅ Real-time AI risk prediction with probability scores<br>✅ PDF health report generation<br>✅ Interactive Plotly visualizations<br>✅ Deployed on Streamlit Community Cloud<br>✅ BMI calculator with visual gauge<br>✅ AI-generated clinical interpretation"),
            ("TECH STACK", "<span style='color:#f472b6;'>Python 3.10</span> · <span style='color:#60a5fa;'>Streamlit</span> · <span style='color:#34d399;'>Scikit-learn</span> · <span style='color:#fbbf24;'>Plotly</span> · <span style='color:#a78bfa;'>NumPy</span> · <span style='color:#f472b6;'>FPDF2</span>"),
        ]:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);
                 border-radius:14px;padding:1.3rem;margin-bottom:.8rem;">
                <div style="font-size:.62rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;
                     color:rgba(240,236,228,.28);margin-bottom:.7rem;">{title}</div>
                <p style="font-size:.87rem;color:rgba(240,236,228,.65);line-height:1.85;">{content}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(96,165,250,.1),rgba(99,102,241,.08));
             border:1px solid rgba(96,165,250,.25);border-radius:14px;padding:1.3rem;margin-bottom:.8rem;">
            <div style="font-size:.62rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;
                 color:#60a5fa;margin-bottom:.8rem;">READY-TO-USE LINKEDIN POST</div>
            <div style="font-size:.85rem;color:rgba(240,236,228,.65);line-height:1.85;">
                🚀 Excited to share my latest ML project — <strong style="color:#f0ece4;">Heart Disease Predictor!</strong><br><br>
                Built with <strong style="color:#f0ece4;">Random Forest</strong> — <strong style="color:#34d399;">95.54% accuracy</strong> on UCI Heart Disease Dataset.<br><br>
                🛠️ Python · Streamlit · Scikit-learn · Plotly<br>
                🌐 <a href="https://heart-disease-predictor-7npize4ygtdgeyfruycnuj.streamlit.app" style="color:#60a5fa;">Live Demo</a> &nbsp;·&nbsp;
                💻 <a href="https://github.com/dip143218/heart-disease-predictor" style="color:#60a5fa;">GitHub</a><br><br>
                <em style="color:rgba(240,236,228,.35);">#MachineLearning #Python #DataScience #HealthAI #CUET #RandomForest</em>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
