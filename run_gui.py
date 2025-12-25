"""
Simple launcher for the Medical Diagnosis Chatbot GUI
"""

import sys
import os

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

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['pandas', 'sklearn', 'chardet', 'numpy', 'tkinter']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            else:
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
    required_files = ['Training.csv', 'Diseases_Symptoms.csv', 'medical_chatbot.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True

def main():
    """Main launcher function."""
    print("🏥 Medical Diagnosis Chatbot GUI Launcher")
    print("=" * 45)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        return 1
    
    # Check data files
    print("📁 Checking data files...")
    if not check_data_files():
        return 1
    
    print("✅ All checks passed!")
    print("🚀 Starting Medical Diagnosis Chatbot GUI...\n")
    
    # Import and run the GUI
    try:
        from medical_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ Error importing GUI: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error running GUI: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
