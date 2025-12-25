"""
Simple launcher script for the Medical Diagnosis Chatbot
"""

import sys
import os

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['pandas', 'sklearn', 'chardet', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install them using: pip install -r requirements.txt")
        return False
    
    return True

def check_data_files():
    """Check if required data files exist."""
    required_files = ['Training.csv', 'Diseases_Symptoms.csv']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required data files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True

def main():
    """Main launcher function."""
    print("🏥 Medical Diagnosis Chatbot Launcher")
    print("=" * 40)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        return 1
    
    # Check data files
    print("📁 Checking data files...")
    if not check_data_files():
        return 1
    
    print("✅ All checks passed!")
    print("🚀 Starting Medical Diagnosis Chatbot...\n")
    
    # Import and run the chatbot
    try:
        from medical_chatbot import main as chatbot_main
        chatbot_main()
    except ImportError as e:
        print(f"❌ Error importing chatbot: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error running chatbot: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
