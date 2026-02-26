# ❤️ Heart Disease Predictor — AI-Powered Cardiovascular Risk Assessment

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-RandomForest-F7931E?style=for-the-badge&logo=scikit-learn)
![Accuracy](https://img.shields.io/badge/Model%20Accuracy-95.54%25-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A machine learning web application that predicts cardiovascular disease risk using Random Forest classification.**

[🚀 Live Demo](https://heart-disease-predictor-7npize4ygtdgeyfruycnuj.streamlit.app) • [📊 Dataset](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset) • [👤 Author](https://github.com/dip143218)

</div>

---

## 📌 Overview

This project is a full-stack ML web application that leverages a **Random Forest classifier** trained on the UCI Heart Disease Dataset to predict whether a patient is at risk of heart disease. Built with **Streamlit**, the app provides an interactive UI where users input clinical parameters and receive instant AI-powered predictions with probability scores, risk factor analysis, and downloadable PDF reports.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 Heart Disease Prediction | 13-parameter clinical input with instant AI prediction |
| 📊 Risk Gauge Chart | Visual risk probability meter (0–100%) |
| 📋 Risk Factor Analysis | Identifies individual risk and healthy factors |
| 📄 PDF Report Download | Generates a professional health report |
| 🧮 BMI Calculator | Body Mass Index calculator with category visualization |
| 🎨 Professional UI | Dark-themed, responsive design with Plotly charts |
| 🏠 Landing Page | Beautiful home screen with navigation |

---

## 🧠 Model Performance

| Metric | Score |
|---|---|
| ✅ Accuracy | **95.54%** |
| 🎯 Precision | High |
| 📈 Recall | High |
| 🔬 Algorithm | Random Forest Classifier |
| 📦 Dataset | UCI Heart Disease (Cleveland) |
| 🔢 Features | 13 clinical parameters |
| 📊 Train/Test Split | 80% / 20% |

---

## 🏥 Input Parameters

The model uses 13 clinical features:

1. **Age** — Patient age in years
2. **Sex** — Gender (Male/Female)
3. **Chest Pain Type** — 4 types (Typical Angina, Atypical, Non-anginal, Asymptomatic)
4. **Resting Blood Pressure** — mmHg
5. **Cholesterol** — Serum cholesterol in mg/dl
6. **Fasting Blood Sugar** — > 120 mg/dl (True/False)
7. **Resting ECG** — Electrocardiographic results
8. **Max Heart Rate** — Maximum heart rate achieved
9. **Exercise Induced Angina** — Yes/No
10. **ST Depression** — Oldpeak value
11. **ST Slope** — Slope of peak exercise ST segment
12. **Major Vessels** — Number of major vessels (0–4)
13. **Thalassemia** — Blood disorder type

---

## 🚀 Run Locally

```bash
# Clone the repository
git clone https://github.com/dip143218/heart-disease-predictor.git
cd heart-disease-predictor

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 🗂️ Project Structure

```
heart-disease-predictor/
│
├── app.py                  # Main Streamlit application
├── heart_disease_model.pkl # Trained Random Forest model
├── scaler.pkl              # StandardScaler for preprocessing
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit, Plotly, Custom CSS
- **Backend / ML:** Scikit-learn, NumPy, Joblib
- **Model:** Random Forest Classifier
- **Report:** FPDF2
- **Deployment:** Streamlit Community Cloud

---

## 👨‍💻 Author

**Morsalin Hossain Dip**
- 🎓 Chittagong University of Engineering & Technology (CUET)
- 💻 GitHub: [@dip143218](https://github.com/dip143218)
- 🌐 Live App: [heart-disease-predictor.streamlit.app](https://heart-disease-predictor-7npize4ygtdgeyfruycnuj.streamlit.app)

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
Made with ❤️ by <b>Morsalin Hossain Dip</b> | CUET
</div>
