#!/usr/bin/env python3
"""
AI-Based Medical Diagnosis Assistant
A professional chatbot for medical symptom analysis and disease prediction.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings
import chardet
import sys
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        # Try to set UTF-8 encoding for Windows console
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        # Fallback for older Python versions
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Suppress warnings for cleaner output
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

class MedicalDiagnosisChatbot:
    """
    A professional medical diagnosis assistant chatbot.
    """
    
    def __init__(self):
        self.model = None
        self.treatment_dict = {}
        self.all_symptoms = []
        self.disease_classes = []
        self.model_accuracy = 0.0
        self.is_trained = False
        
        # Safety and disclaimer messages
        self.disclaimer = """
⚠️  IMPORTANT MEDICAL DISCLAIMER ⚠️
This AI assistant is for informational purposes only and should NOT replace 
professional medical advice, diagnosis, or treatment. Always consult with a 
qualified healthcare provider for any medical concerns.
        """
        
        self.welcome_message = """
🏥 Welcome to AI Medical Diagnosis Assistant 🏥

I'm here to help analyze your symptoms and provide preliminary insights.
Remember: This is for educational purposes only - always consult a doctor!

Let's start with some basic information about you.
        """
    
    def load_csv_auto(self, file_path: str) -> pd.DataFrame:
        """
        Automatically detect and load CSV files with proper encoding.
        """
        encodings_to_try = []
        
        try:
            with open(file_path, "rb") as f:
                raw_data = f.read(100000)
                result = chardet.detect(raw_data)
                detected_encoding = result.get("encoding")
                print(f"📁 Detected encoding for {file_path}: {detected_encoding}")
                if detected_encoding:
                    encodings_to_try.append(detected_encoding)
        except Exception as e:
            print(f"⚠️  Could not detect encoding for {file_path}: {e}")
        
        encodings_to_try.extend(["utf-8", "cp1252", "ISO-8859-1", "MacRoman"])
        
        for enc in encodings_to_try:
            try:
                df = pd.read_csv(file_path, encoding=enc)
                print(f"✅ Successfully loaded {file_path} with encoding: {enc}")
                return df
            except Exception as e:
                print(f"❌ Failed to load {file_path} with encoding {enc}: {e}")
        
        raise ValueError(f"Unable to read CSV file {file_path} with any of the tried encodings.")
    
    def load_data(self, train_csv: str = 'Training.csv', symptoms_csv: str = 'Diseases_Symptoms.csv') -> bool:
        """
        Load and preprocess the training data and treatment information.
        """
        try:
            print("🔄 Loading training data...")
            df_model_data = self.load_csv_auto(train_csv)
            
            print("🔄 Loading treatment data...")
            df_treatments = self.load_csv_auto(symptoms_csv)
            
            # Process training data
            if 'prognosis' in df_model_data.columns:
                df_model_data.rename(columns={'prognosis': 'name'}, inplace=True)
            else:
                raise ValueError(f"The dataset '{train_csv}' must contain a 'prognosis' column.")
            
            df_model_data.columns = [str(col).lower().strip() for col in df_model_data.columns]
            
            # Process treatment data
            if 'Code' in df_treatments.columns:
                df_treatments.rename(columns={'Code': 'Name'}, inplace=True)
            elif 'Name' not in df_treatments.columns:
                raise ValueError(f"The treatment dataset must contain 'Code' or 'Name'.")
            
            if 'Treatments' not in df_treatments.columns:
                raise ValueError(f"The treatment dataset must contain 'Treatments' column.")
            
            # Clean treatment data
            df_treatments['Name'] = df_treatments['Name'].apply(
                lambda x: str(x).strip().lower() if x is not None and str(x).strip() != 'nan' else ''
            )
            df_treatments['Treatments'] = df_treatments['Treatments'].apply(
                lambda x: str(x).strip() if x is not None and str(x).strip() != 'nan' else ''
            )
            
            # Build treatment dictionary

            if len(df_treatments) > 0:
                self.treatment_dict = dict(zip(df_treatments['Name'], df_treatments['Treatments']))
            
            # Prepare features and labels
            self.X = df_model_data.drop(columns=['name'])
            self.y = df_model_data['name']
            self.all_symptoms = [col for col in self.X.columns if col != 'name']
            self.X.fillna(0, inplace=True)
            
            # Filter diseases with insufficient data
            disease_counts = self.y.value_counts()
            single_entry_diseases = disease_counts[disease_counts < 2].index.tolist()
            
            if single_entry_diseases:
                print(f"\n⚠️  Found {len(single_entry_diseases)} diseases with insufficient data:")
                for disease in single_entry_diseases[:5]:  # Show first 5
                    print(f"   - {disease}")
                if len(single_entry_diseases) > 5:
                    print(f"   ... and {len(single_entry_diseases) - 5} more")
                
                indices_to_keep = self.y[~self.y.isin(single_entry_diseases)].index
                self.X = self.X.loc[indices_to_keep]
                self.y = self.y.loc[indices_to_keep]
            
            if self.X.empty or self.y.empty:
                raise ValueError("No data remains after filtering.")
            
            print(f"✅ Data loaded successfully!")
            print(f"   📊 Total samples: {len(self.X)}")
            print(f"   🦠 Unique diseases: {len(self.y.unique())}")
            print(f"   🔍 Total symptoms: {len(self.all_symptoms)}")
            
            return True
            
        except FileNotFoundError as e:
            print(f"❌ CSV file not found: {e}")
            return False
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def train_model(self) -> bool:
        """
        Train the Random Forest model and evaluate its performance.
        """
        try:
            print("\n🤖 Training AI model...")
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
            )
            
            # Train model
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2
            )
            
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            self.model_accuracy = accuracy_score(y_test, y_pred)
            self.disease_classes = self.model.classes_
            
            print(f"✅ Model training completed!")
            print(f"   🎯 Accuracy: {self.model_accuracy:.2%}")
            print(f"   📈 Classes: {len(self.disease_classes)}")
            
            # Show top diseases by frequency
            disease_counts = self.y.value_counts().head(5)
            print(f"\n📊 Top 5 most common diseases in dataset:")
            for disease, count in disease_counts.items():
                print(f"   - {disease}: {count} cases")
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"❌ Error training model: {e}")
            return False
    
    def validate_symptoms(self, symptoms: List[str]) -> Tuple[List[str], List[str]]:
        """
        Validate and match symptoms against the model's known symptoms.
        """
        valid_symptoms = []
        invalid_symptoms = []
        
        # Common symptom mappings for better matching
        symptom_mappings = {
            'fever': ['high_fever', 'mild_fever'],
            'cold': ['cold_hands_and_feets'],
            'sweating': ['sweating'],
            'trembling': ['trembling'],
            'headache': ['headache'],
            'nausea': ['nausea'],
            'vomiting': ['vomiting'],
            'diarrhea': ['diarrhoea'],
            'diarrhoea': ['diarrhoea'],
            'constipation': ['constipation'],
            'cough': ['cough'],
            'sneezing': ['continuous_sneezing'],
            'rash': ['skin_rash'],
            'fatigue': ['fatigue'],
            'weakness': ['muscle_weakness', 'weakness_in_limbs'],
            'pain': ['joint_pain', 'stomach_pain', 'back_pain', 'chest_pain'],
            'breathing': ['breathlessness'],
            'dizziness': ['dizziness'],
            'anxiety': ['anxiety'],
            'depression': ['depression']
        }
        
        for symptom in symptoms:
            symptom_clean = str(symptom).strip().lower()
            
            # Direct match
            if symptom_clean in self.all_symptoms:
                valid_symptoms.append(symptom_clean)
            else:
                # Check mappings first
                found_match = False
                if symptom_clean in symptom_mappings:
                    for mapped_symptom in symptom_mappings[symptom_clean]:
                        if mapped_symptom in self.all_symptoms:
                            valid_symptoms.append(mapped_symptom)
                            found_match = True
                            break
                
                if not found_match:
                    # Fuzzy matching for common variations
                    for known_symptom in self.all_symptoms:
                        if (symptom_clean in known_symptom or 
                            known_symptom in symptom_clean or
                            self._similarity(symptom_clean, known_symptom) > 0.6):
                            valid_symptoms.append(known_symptom)
                            found_match = True
                            break
                
                if not found_match:
                    invalid_symptoms.append(symptom)
        
        return valid_symptoms, invalid_symptoms
    
    def _similarity(self, a: str, b: str) -> float:
        """
        Calculate simple string similarity.
        """
        a_words = set(a.split())
        b_words = set(b.split())
        if not a_words or not b_words:
            return 0.0
        return len(a_words.intersection(b_words)) / len(a_words.union(b_words))
    
    def diagnose(self, symptoms: List[str]) -> Dict:
        """
        Perform diagnosis based on symptoms.
        """
        if not self.is_trained:
            return {"error": "Model not trained"}
        
        # Validate symptoms
        valid_symptoms, invalid_symptoms = self.validate_symptoms(symptoms)
        
        if not valid_symptoms:
            return {
                "error": "No valid symptoms provided",
                "invalid_symptoms": invalid_symptoms
            }
        
        # Create input vector
        input_vector = [1 if symptom in valid_symptoms else 0 for symptom in self.all_symptoms]
        
        try:
            # Get predictions
            probabilities = self.model.predict_proba([input_vector])[0]
            disease_probs = list(zip(self.disease_classes, probabilities))
            disease_probs.sort(key=lambda x: x[1], reverse=True)
            
            # Get top predictions
            top_predictions = disease_probs[:3]
            
            # Get treatment for top prediction
            top_disease = top_predictions[0][0]
            treatment = self.treatment_dict.get(top_disease.lower(), 
                                              "Consult a medical professional for proper treatment.")
            
            return {
                "top_predictions": top_predictions,
                "treatment": treatment,
                "valid_symptoms": valid_symptoms,
                "invalid_symptoms": invalid_symptoms,
                "confidence": top_predictions[0][1] if top_predictions else 0.0
            }
            
        except Exception as e:
            return {"error": f"Prediction error: {e}"}
    
    def format_diagnosis_report(self, diagnosis: Dict, patient_info: Dict) -> str:
        """
        Format the diagnosis results into a professional report.
        """
        if "error" in diagnosis:
            return f"❌ Error: {diagnosis['error']}"
        
        report = f"""
{'='*60}
🏥 AI MEDICAL DIAGNOSIS REPORT
{'='*60}
👤 Patient: {patient_info.get('name', 'Anonymous')}
🎂 Age: {patient_info.get('age', 'Not specified')}
⚥ Gender: {patient_info.get('gender', 'Not specified')}
📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 Reported Symptoms:
   {', '.join(diagnosis['valid_symptoms'])}
"""
        
        if diagnosis['invalid_symptoms']:
            report += f"\n⚠️  Unrecognized symptoms (ignored):\n   {', '.join(diagnosis['invalid_symptoms'])}"
        
        report += f"\n\n🔍 DIAGNOSIS RESULTS:\n"
        
        for i, (disease, confidence) in enumerate(diagnosis['top_predictions'], 1):
            confidence_pct = confidence * 100
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            report += f"   {emoji} {disease} ({confidence_pct:.1f}% confidence)\n"
        
        report += f"\n💊 TREATMENT SUGGESTION:\n   {diagnosis['treatment']}"
        
        report += f"\n\n{self.disclaimer}"
        report += f"\n{'='*60}\n"
        
        return report
    
    def get_symptom_suggestions(self, partial_symptom: str) -> List[str]:
        """
        Get symptom suggestions based on partial input.
        """
        partial = partial_symptom.lower().strip()
        suggestions = []
        
        for symptom in self.all_symptoms:
            if partial in symptom.lower():
                suggestions.append(symptom)
        
        return suggestions[:10]  # Return top 10 matches
    
    def interactive_chat(self):
        """
        Start the interactive chatbot session.
        """
        print(self.welcome_message)
        print(self.disclaimer)
        
        # Get patient information
        print("\n" + "="*50)
        print("📋 PATIENT INFORMATION")
        print("="*50)
        
        name = input("👤 What's your name? ").strip() or "Anonymous"
        age = input("🎂 What's your age? ").strip() or "Not specified"
        gender = input("⚥ What's your gender? ").strip() or "Not specified"
        
        patient_info = {"name": name, "age": age, "gender": gender}
        
        print(f"\n✅ Thank you, {name}! Now let's talk about your symptoms.")
        print("💡 Tip: You can enter multiple symptoms separated by commas.")
        print("💡 Type 'help' for assistance, 'quit' to exit, 'suggestions' for symptom ideas.")
        
        while True:
            print("\n" + "-"*50)
            user_input = input("🔍 What symptoms are you experiencing? ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Thank you for using AI Medical Diagnosis Assistant!")
                print("Remember: Always consult a healthcare professional for medical advice.")
                break
            
            elif user_input.lower() == 'help':
                print("""
📖 HELP MENU:
• Enter your symptoms (e.g., "fever, headache, nausea")
• Type 'suggestions' to see available symptoms
• Type 'quit' to exit
• Type 'help' to see this menu again

⚠️  Remember: This is for educational purposes only!
                """)
                continue
            
            elif user_input.lower() == 'suggestions':
                print(f"\n📋 Common symptoms you can try:")
                common_symptoms = [
                    'fever', 'headache', 'nausea', 'vomiting', 'cough', 'sneezing',
                    'rash', 'fatigue', 'weakness', 'pain', 'breathing', 'dizziness',
                    'anxiety', 'depression', 'constipation', 'diarrhea', 'sweating'
                ]
                for i, symptom in enumerate(common_symptoms, 1):
                    print(f"   {i:2d}. {symptom}")
                
                print(f"\n📋 Or try these specific symptoms (first 15):")
                for i, symptom in enumerate(self.all_symptoms[:15], 1):
                    print(f"   {i:2d}. {symptom}")
                if len(self.all_symptoms) > 15:
                    print(f"   ... and {len(self.all_symptoms) - 15} more")
                continue
            
            elif not user_input:
                print("❌ Please enter some symptoms to analyze.")
                continue
            
            # Process symptoms
            symptoms = [s.strip() for s in user_input.split(',')]
            symptoms = [s for s in symptoms if s]  # Remove empty strings
            
            print(f"\n🔄 Analyzing symptoms: {', '.join(symptoms)}")
            
            # Get diagnosis
            diagnosis = self.diagnose(symptoms)
            
            # Display results
            if "error" in diagnosis:
                print(f"❌ {diagnosis['error']}")
                if diagnosis.get('invalid_symptoms'):
                    print(f"💡 Invalid symptoms: {', '.join(diagnosis['invalid_symptoms'])}")
                    print(f"💡 Try these common symptoms instead:")
                    common_suggestions = ['fever', 'headache', 'nausea', 'cough', 'fatigue', 'pain', 'sweating', 'dizziness']
                    print(f"   {', '.join(common_suggestions)}")
                    print(f"💡 Or type 'suggestions' to see all available symptoms")
            else:
                report = self.format_diagnosis_report(diagnosis, patient_info)
                print(report)
            
            # Ask if user wants to continue
            continue_choice = input("\n🔄 Would you like to analyze more symptoms? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes']:
                print("👋 Thank you for using AI Medical Diagnosis Assistant!")
                print("Remember: Always consult a healthcare professional for medical advice.")
                break

def main():
    """
    Main function to run the medical diagnosis chatbot.
    """
    print("🏥 AI Medical Diagnosis Assistant")
    print("=" * 50)
    
    # Initialize chatbot
    chatbot = MedicalDiagnosisChatbot()
    
    # Load data
    if not chatbot.load_data():
        print("❌ Failed to load data. Please check your CSV files.")
        return
    
    # Train model
    if not chatbot.train_model():
        print("❌ Failed to train model.")
        return
    
    # Start interactive session
    try:
        chatbot.interactive_chat()
    except KeyboardInterrupt:
        print("\n\n👋 Session interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
