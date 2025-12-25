# AI-Based Medical Diagnosis Assistant 🏥

A professional, interactive medical diagnosis chatbot that uses machine learning to analyze symptoms and provide preliminary disease predictions. Built with a focus on user experience, safety, and educational value.

## ⚠️ Important Disclaimer
**This AI assistant is for educational and informational purposes only. It should NEVER replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for any medical concerns.**

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Required CSV data files: `Training.csv` and `Diseases_Symptoms.csv`

### Installation
1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the chatbot:

   **🎨 Beautiful GUI (Recommended):**
   ```bash
   python run_beautiful_gui.py
   ```
   Or directly:
   ```bash
   python beautiful_chat_gui.py
   ```

   **🎨 Professional GUI:**
   ```bash
   python run_gui.py
   ```
   Or directly:
   ```bash
   python medical_gui.py
   ```

   **💻 Command Line Mode:**
   ```bash
   python run_chatbot.py
   ```
   Or directly:
   ```bash
   python medical_chatbot.py
   ```

## 🔍 Features

### Core Functionality
- **🎨 Beautiful GUI Interface**: Clean, modern, and professional chat interface
- **🎨 Professional GUI Interface**: Gemini-inspired advanced interface
- **💻 Command Line Interface**: Traditional terminal-based interaction
- **Interactive Chat Interface**: Natural conversation flow for symptom input
- **Machine Learning Model**: Random Forest classifier trained on symptom-disease data
- **Multi-symptom Analysis**: Handles multiple symptoms simultaneously
- **Confidence Scoring**: Shows probability scores for top 3 disease predictions
- **Treatment Suggestions**: Provides preliminary treatment recommendations

### Advanced Features
- **Symptom Validation**: Smart matching and validation of user input
- **Fuzzy Matching**: Handles variations in symptom descriptions
- **Symptom Suggestions**: Auto-complete and suggestion system
- **Data Quality Handling**: Filters out diseases with insufficient training data
- **Professional Reports**: Formatted medical-style reports with disclaimers
- **Error Handling**: Robust error handling and user guidance

### Safety Features
- **Medical Disclaimers**: Clear warnings about AI limitations
- **Professional Recommendations**: Always suggests consulting healthcare providers
- **Input Validation**: Prevents invalid or dangerous inputs
- **Confidence Thresholds**: Shows uncertainty levels in predictions

## 📊 Technical Details

### Model Architecture
- **Algorithm**: Random Forest Classifier
- **Features**: Binary symptom indicators
- **Validation**: Train-test split with stratification
- **Performance**: Accuracy reporting and model evaluation

### Data Processing
- **Encoding Detection**: Automatic CSV encoding detection
- **Data Cleaning**: Handles missing values and inconsistencies
- **Feature Engineering**: Binary symptom encoding
- **Quality Control**: Filters diseases with insufficient data

## 🎯 Usage Examples

### GUI Usage (Recommended)
1. **Launch the GUI**: Run `python run_gui.py`
2. **Wait for initialization**: The AI model will load automatically
3. **Enter symptoms**: Type symptoms in the text box (e.g., "fever, headache, nausea")
4. **Click Analyze**: Get instant diagnosis results
5. **Use features**:
   - 📋 Show Symptoms: View all available symptoms
   - 👤 Patient Info: Set your personal information
   - 🗑️ Clear Chat: Start a new conversation
   - ❓ Help: Get assistance

### Command Line Usage
```
👤 What's your name? John Doe
🎂 What's your age? 35
⚥ What's your gender? Male
🔍 What symptoms are you experiencing? fever, headache, nausea
```

### Advanced Features
- Type `help` for assistance menu
- Type `suggestions` to see available symptoms
- Type `quit` to exit
- Enter multiple symptoms separated by commas

## 📁 File Structure
```
├── medical_chatbot.py        # Core chatbot implementation
├── beautiful_chat_gui.py     # Beautiful and clean GUI interface
├── medical_gui.py           # Professional GUI interface
├── run_beautiful_gui.py     # Beautiful GUI launcher
├── run_gui.py              # Professional GUI launcher
├── run_chatbot.py          # Command line launcher script
├── requirements.txt        # Python dependencies
├── Training.csv           # Symptom-disease training data
├── Diseases_Symptoms.csv  # Treatment information
└── README.md             # This file
```

## 🔧 Configuration

### Model Parameters
The Random Forest model uses these default parameters:
- `n_estimators=100`: Number of trees
- `max_depth=10`: Maximum tree depth
- `min_samples_split=5`: Minimum samples to split
- `min_samples_leaf=2`: Minimum samples per leaf

### Data Requirements
- **Training.csv**: Must contain 'prognosis' column and symptom columns
- **Diseases_Symptoms.csv**: Must contain 'Code'/'Name' and 'Treatments' columns

## 🛠️ Troubleshooting

### Common Issues
1. **Missing CSV files**: Ensure `Training.csv` and `Diseases_Symptoms.csv` are in the same directory
2. **Encoding errors**: The system automatically detects and handles various encodings
3. **Import errors**: Run `pip install -r requirements.txt` to install dependencies
4. **Low accuracy**: Check data quality and consider retraining with more data

### Performance Tips
- Use specific symptom names for better matching
- Enter multiple related symptoms for more accurate predictions
- Check the suggestions menu for valid symptom names

## 📈 Future Enhancements
- Integration with medical databases
- Multi-language support
- Voice input/output capabilities
- Mobile app interface
- Integration with electronic health records

## 🤝 Contributing
This is an educational project. Contributions are welcome for:
- Improving the machine learning model
- Enhancing the user interface
- Adding new features
- Improving documentation

## 📄 License
This project is for educational purposes. Please ensure compliance with medical software regulations in your jurisdiction.

---
**Remember: This AI is a learning tool, not a replacement for professional medical care!** 🏥
