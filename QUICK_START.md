# 🚀 Quick Start Guide - Deploy Your Medical Diagnosis App

## 📋 Prerequisites
- GitHub account (free)
- Python 3.8+ (for local testing)

## 🌐 Deploy to Streamlit Cloud (5 minutes)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - Medical Diagnosis Assistant"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Visit: https://share.streamlit.io
2. Click "Sign in" → Use GitHub
3. Click "New app"
4. Select your repository
5. Main file: `streamlit_app.py`
6. Click "Deploy" ⚡

### Step 3: Get Your Live URL
Your app will be live at:
```
https://YOUR_APP_NAME.streamlit.app
```

## 🧪 Test Locally First
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open: http://localhost:8501

## 📁 Required Files
Make sure these are in your repo:
- ✅ `streamlit_app.py`
- ✅ `medical_chatbot.py`
- ✅ `Training.csv`
- ✅ `Diseases_Symptoms.csv`
- ✅ `requirements.txt`

## 🎉 That's It!
Your app is now live and accessible from anywhere!

