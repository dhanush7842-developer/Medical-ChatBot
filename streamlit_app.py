"""
Medical Diagnosis Chatbot - Web Application
Streamlit web interface for the AI Medical Diagnosis Assistant
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Page configuration
st.set_page_config(
    page_title="AI Medical Diagnosis Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for sky blue theme
st.markdown("""
<style>
    .main {
        background-color: #e0f2fe;
    }
    .stButton>button {
        background-color: #0ea5e9;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #0284c7;
    }
    .stTextInput>div>div>input {
        background-color: white;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #bae6fd;
        margin-left: 20%;
    }
    .ai-message {
        background-color: #e0f7fa;
        margin-right: 20%;
    }
    .status-box {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #bae6fd;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Import chatbot
try:
    from medical_chatbot import MedicalDiagnosisChatbot
except ImportError:
    st.error("❌ Error: medical_chatbot.py not found!")
    st.stop()

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
    st.session_state.is_initialized = False
    st.session_state.conversation_history = []
    st.session_state.patient_info = {'name': 'Anonymous', 'age': 'Not specified', 'gender': 'Not specified'}

# Initialize chatbot
@st.cache_resource
def initialize_chatbot():
    """Initialize the chatbot (cached to avoid re-initialization)."""
    chatbot = MedicalDiagnosisChatbot()
    
    # Load data
    if not chatbot.load_data():
        return None
    
    # Train model
    if not chatbot.train_model():
        return None
    
    return chatbot

# Initialize chatbot
if st.session_state.chatbot is None:
    with st.spinner("🔄 Initializing AI model..."):
        st.session_state.chatbot = initialize_chatbot()
        if st.session_state.chatbot:
            st.session_state.is_initialized = True
            st.success("✅ AI model ready!")
        else:
            st.error("❌ Failed to initialize chatbot. Please check your CSV files.")
            st.stop()

# Header
st.title("🏥 AI Medical Diagnosis Assistant")
st.markdown("**Powered by Advanced Machine Learning • Professional Medical AI • 2025**")
st.markdown("---")

# Sidebar for patient information
with st.sidebar:
    st.header("👤 Patient Information")
    
    name = st.text_input("Name", value=st.session_state.patient_info.get('name', 'Anonymous'))
    age = st.text_input("Age", value=st.session_state.patient_info.get('age', 'Not specified'))
    gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                         index=["Male", "Female", "Other"].index(st.session_state.patient_info.get('gender', 'Male')) 
                         if st.session_state.patient_info.get('gender', 'Male') in ["Male", "Female", "Other"] else 0)
    
    st.session_state.patient_info = {
        'name': name,
        'age': age,
        'gender': gender
    }
    
    st.markdown("---")
    st.markdown("### 📋 Quick Actions")
    
    if st.button("📋 Browse Symptoms"):
        st.session_state.show_symptoms = True
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.conversation_history = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### ⚠️ Disclaimer")
    st.info("""
    This AI assistant is for informational purposes only and should NOT replace 
    professional medical advice, diagnosis, or treatment. Always consult with a 
    qualified healthcare provider for any medical concerns.
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 AI Doctor Consultation")
    
    # Display conversation history
    chat_container = st.container()
    
    with chat_container:
        if not st.session_state.conversation_history:
            st.info("💡 Enter your symptoms below to get started. Click 'Browse Symptoms' to see available symptoms.")
        else:
            for message in st.session_state.conversation_history:
                if message['type'] == 'user':
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>👤 You</strong> • {message['timestamp']}<br>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                elif message['type'] == 'ai':
                    st.markdown(f"""
                    <div class="chat-message ai-message">
                        <strong>🤖 AI Doctor</strong> • {message['timestamp']}<br>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info(f"💬 {message['content']}")

# Symptom input
st.markdown("---")

# Handle symptom selection from buttons
selected_symptom = st.session_state.get('selected_symptom', '')
col_input1, col_input2 = st.columns([4, 1])

with col_input1:
    if selected_symptom:
        symptom_input = st.text_input(
            "Describe your symptoms",
            value=selected_symptom,
            placeholder="e.g., fever, headache, nausea",
            key="symptom_input"
        )
        st.session_state.selected_symptom = ''  # Clear after use
    else:
        symptom_input = st.text_input(
            "Describe your symptoms",
            placeholder="e.g., fever, headache, nausea",
            key="symptom_input"
        )

with col_input2:
    analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)

# Analyze symptoms
if analyze_button and symptom_input:
    if not st.session_state.is_initialized:
        st.warning("⚠️ AI model is still initializing. Please wait.")
    else:
        # Add user message
        st.session_state.conversation_history.append({
            'type': 'user',
            'content': symptom_input,
            'timestamp': datetime.now().strftime("%H:%M")
        })
        
        # Analyze symptoms
        with st.spinner("🔄 Analyzing symptoms..."):
            symptoms = [s.strip() for s in symptom_input.split(',')]
            symptoms = [s for s in symptoms if s]
            
            diagnosis = st.session_state.chatbot.diagnose(symptoms)
            
            if "error" in diagnosis:
                response = f"❌ {diagnosis['error']}"
                if diagnosis.get('invalid_symptoms'):
                    response += f"\n\n💡 Invalid symptoms: {', '.join(diagnosis['invalid_symptoms'])}"
                    response += "\n\n💡 Try these common symptoms: fever, headache, nausea, cough, fatigue, pain, sweating, dizziness"
            else:
                # Format diagnosis report
                response = "🔍 **DIAGNOSIS RESULTS**\n\n"
                response += f"✅ **Valid Symptoms:** {', '.join(diagnosis['valid_symptoms'])}\n\n"
                response += "🎯 **Top 3 Predictions:**\n"
                
                for i, (disease, confidence) in enumerate(diagnosis['top_predictions'], 1):
                    confidence_pct = confidence * 100
                    emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
                    response += f"   {emoji} **{disease}** ({confidence_pct:.1f}% confidence)\n"
                
                response += f"\n💊 **Treatment Suggestion:**\n   {diagnosis['treatment']}"
                
                if diagnosis.get('invalid_symptoms'):
                    response += f"\n\n⚠️ **Unrecognized symptoms:** {', '.join(diagnosis['invalid_symptoms'])}"
                
                response += "\n\n⚠️ **Remember:** This is for educational purposes only. Always consult a healthcare professional."
            
            # Add AI response
            st.session_state.conversation_history.append({
                'type': 'ai',
                'content': response,
                'timestamp': datetime.now().strftime("%H:%M")
            })
        
        st.rerun()

# Show symptoms if requested
if st.session_state.get('show_symptoms', False):
    st.markdown("---")
    st.subheader("📋 Available Symptoms")
    
    tab1, tab2 = st.tabs(["Common Symptoms", "All Symptoms"])
    
    with tab1:
        common_symptoms = [
            'fever', 'headache', 'nausea', 'vomiting', 'cough', 'sneezing',
            'rash', 'fatigue', 'weakness', 'pain', 'breathing', 'dizziness',
            'anxiety', 'depression', 'constipation', 'diarrhea', 'sweating',
            'trembling', 'cold', 'itching', 'swelling'
        ]
        
        cols = st.columns(3)
        for i, symptom in enumerate(common_symptoms):
            with cols[i % 3]:
                if st.button(symptom, key=f"common_{i}", use_container_width=True):
                    # Store selected symptom
                    current_input = st.session_state.get('symptom_input', '')
                    if current_input:
                        st.session_state.selected_symptom = f"{current_input}, {symptom}"
                    else:
                        st.session_state.selected_symptom = symptom
                    st.rerun()
    
    with tab2:
        if st.session_state.chatbot:
            all_symptoms = st.session_state.chatbot.all_symptoms
            symptom_text = "\n".join([f"{i+1}. {symptom}" for i, symptom in enumerate(all_symptoms)])
            st.text_area("All Available Symptoms", symptom_text, height=400, disabled=True)
    
    st.session_state.show_symptoms = False

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b;'>
    <p>🏥 AI Medical Diagnosis Assistant 2025</p>
    <p>Powered by Machine Learning • Educational Use Only</p>
</div>
""", unsafe_allow_html=True)

