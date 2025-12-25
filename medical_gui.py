"""
Medical Diagnosis Chatbot - Professional 2025 GUI Interface
A cutting-edge, modern interface for the medical diagnosis assistant.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
import sys
import os

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Import our chatbot
try:
    from medical_chatbot import MedicalDiagnosisChatbot
except ImportError:
    print("❌ Error: medical_chatbot.py not found!")
    sys.exit(1)

class ModernCard(tk.Frame):
    """Modern card widget with shadow effect."""
    def __init__(self, parent, **kwargs):
        # Extract frame-specific options
        bg = kwargs.pop('bg', '#ffffff')
        relief = kwargs.pop('relief', 'flat')
        borderwidth = kwargs.pop('borderwidth', 0)
        # Remove padx/pady if present (should be used in grid/pack, not constructor)
        kwargs.pop('padx', None)
        kwargs.pop('pady', None)
        
        super().__init__(parent, bg=bg, relief=relief, borderwidth=borderwidth, **kwargs)
        self.configure(highlightbackground='#e0e0e0', highlightthickness=1)

class MedicalChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.chatbot = None
        self.patient_info = {}
        self.is_initialized = False
        self.conversation_history = []
        self.current_session = []
        
        # Sky Blue Color Palette 2025
        self.colors = {
            'primary': '#0ea5e9',      # Sky blue
            'primary_dark': '#0284c7',
            'primary_light': '#38bdf8',
            'secondary': '#7dd3fc',    # Light sky blue
            'success': '#22c55e',      # Green
            'warning': '#f59e0b',      # Amber
            'error': '#ef4444',        # Red
            'background': '#e0f2fe',   # Very light sky blue
            'surface': '#ffffff',      # White
            'text_primary': '#0c4a6e', # Dark sky blue
            'text_secondary': '#075985', # Medium sky blue
            'text_tertiary': '#7dd3fc', # Light sky blue
            'border': '#bae6fd',       # Sky blue border
            'accent': '#0ea5e9',       # Sky blue accent
            'chat_user': '#bae6fd',    # Sky blue tint
            'chat_ai': '#e0f7fa',      # Light cyan/sky blue
        }
        
        # Configure main window
        self.root.title("AI Medical Diagnosis Assistant 2025")
        self.root.geometry("1400x900")
        self.root.configure(bg=self.colors['background'])
        
        # Modern window settings
        self.root.resizable(True, True)
        self.root.minsize(1200, 800)
        
        # Configure modern styles
        self.setup_styles()
        
        # Create GUI elements
        self.create_widgets()
        
        # Initialize chatbot in background
        self.initialize_chatbot()
    
    def setup_styles(self):
        """Configure modern 2025 visual styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Modern typography
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'),
                       background=self.colors['background'],
                       foreground=self.colors['text_primary'])
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 11),
                       background=self.colors['background'],
                       foreground=self.colors['text_secondary'])
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       background=self.colors['background'],
                       foreground=self.colors['text_primary'])
        
        style.configure('Body.TLabel',
                       font=('Segoe UI', 11),
                       background=self.colors['background'],
                       foreground=self.colors['text_primary'])
        
        style.configure('Info.TLabel',
                       font=('Segoe UI', 10),
                       background=self.colors['background'],
                       foreground=self.colors['text_secondary'])
        
        style.configure('Success.TLabel',
                       font=('Segoe UI', 11, 'bold'),
                       background=self.colors['background'],
                       foreground=self.colors['success'])
        
        style.configure('Error.TLabel',
                       font=('Segoe UI', 11, 'bold'),
                       background=self.colors['background'],
                       foreground=self.colors['error'])
        
        # Modern Primary Button - Sky Blue
        style.configure('Primary.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       padding=(20, 10),
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       anchor='center')
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['primary_dark']),
                           ('pressed', self.colors['primary_dark'])],
                 foreground=[('active', 'white'),
                           ('pressed', 'white')],
                 relief=[('pressed', 'sunken')])
        
        # Modern Secondary Button - Sky Blue Theme
        style.configure('Secondary.TButton',
                       font=('Segoe UI', 11),
                       padding=(18, 10),
                       background=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       borderwidth=2,
                       relief='solid',
                       anchor='center',
                       bordercolor=self.colors['border'])
        
        style.map('Secondary.TButton',
                 background=[('active', self.colors['background'])],
                 bordercolor=[('active', self.colors['primary']),
                            ('!active', self.colors['border'])],
                 foreground=[('active', self.colors['primary']),
                           ('!active', self.colors['text_primary'])])
        
        # Modern Entry
        style.configure('Modern.TEntry',
                       font=('Segoe UI', 12),
                       padding=(12, 10),
                       borderwidth=1,
                       relief='solid',
                       fieldbackground=self.colors['surface'])
        
        style.map('Modern.TEntry',
                 bordercolor=[('focus', self.colors['primary']),
                             ('!focus', self.colors['border'])],
                 lightcolor=[('focus', self.colors['primary'])],
                 darkcolor=[('focus', self.colors['primary'])])
    
    def create_widgets(self):
        """Create all GUI widgets with modern 2025 design."""
        # Main container with modern padding
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)
        
        # Configure grid
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Header Section - Modern Design
        header_card = ModernCard(main_container, bg=self.colors['surface'], relief='flat', borderwidth=0)
        header_card.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_card.columnconfigure(0, weight=1)
        
        header_content = tk.Frame(header_card, bg=self.colors['surface'], padx=32, pady=24)
        header_content.grid(row=0, column=0, sticky=(tk.W, tk.E))
        header_content.columnconfigure(1, weight=1)
        
        # Title with icon
        title_frame = tk.Frame(header_content, bg=self.colors['surface'])
        title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 8))
        
        title_label = ttk.Label(title_frame, 
                               text="🏥 AI Medical Diagnosis Assistant",
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle_label = ttk.Label(header_content,
                                 text="Powered by Advanced Machine Learning • Professional Medical AI • 2025",
                                 style='Subtitle.TLabel')
        subtitle_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 16))
        
        # Status Card - Modern Design
        status_card = ModernCard(header_content, bg=self.colors['surface'], relief='flat', borderwidth=0)
        status_card.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(8, 0))
        
        status_content = tk.Frame(status_card, bg=self.colors['surface'], padx=20, pady=16)
        status_content.pack(fill=tk.BOTH, expand=True)
        status_content.columnconfigure(1, weight=1)
        
        # Status label
        self.status_label = ttk.Label(status_content, 
                                     text="🔄 Initializing AI model...",
                                     style='Info.TLabel')
        self.status_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 16))
        
        # Modern progress bar
        progress_frame = tk.Frame(status_content, bg=self.colors['surface'])
        progress_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        self.progress = ttk.Progressbar(progress_frame, 
                                        mode='indeterminate',
                                        length=300,
                                        style='Modern.Horizontal.TProgressbar')
        self.progress.pack(fill=tk.X, expand=True)
        self.progress.start(10)
        
        # Chat Section - Modern Card Design
        chat_card = ModernCard(main_container, bg=self.colors['surface'], relief='flat', borderwidth=0)
        chat_card.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        chat_card.columnconfigure(0, weight=1)
        chat_card.rowconfigure(1, weight=1)
        
        # Chat Header
        chat_header = tk.Frame(chat_card, bg=self.colors['surface'], padx=24, pady=20)
        chat_header.grid(row=0, column=0, sticky=(tk.W, tk.E))
        chat_header.columnconfigure(0, weight=1)
        
        chat_title = ttk.Label(chat_header,
                              text="💬 AI Doctor Consultation",
                              style='Header.TLabel')
        chat_title.grid(row=0, column=0, sticky=tk.W)
        
        # Chat Display - Modern Styling
        chat_display_frame = tk.Frame(chat_card, bg=self.colors['surface'], padx=24)
        chat_display_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 24))
        chat_display_frame.columnconfigure(0, weight=1)
        chat_display_frame.rowconfigure(0, weight=1)
        
        # Modern chat text widget
        self.chat_display = scrolledtext.ScrolledText(chat_display_frame,
                                                     height=25,
                                                     width=100,
                                                     font=('Segoe UI', 11),
                                                     bg=self.colors['surface'],
                                                     fg=self.colors['text_primary'],
                                                     wrap=tk.WORD,
                                                     state=tk.DISABLED,
                                                     relief='flat',
                                                     borderwidth=1,
                                                     highlightthickness=1,
                                                     highlightbackground=self.colors['border'],
                                                     highlightcolor=self.colors['primary'],
                                                     padx=20,
                                                     pady=20,
                                                     spacing1=8,
                                                     spacing2=4,
                                                     spacing3=8)
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure modern text tags
        self.chat_display.tag_configure('user_header', 
                                       font=('Segoe UI', 10, 'bold'),
                                       foreground=self.colors['primary'],
                                       background=self.colors['chat_user'])
        self.chat_display.tag_configure('user_message',
                                       font=('Segoe UI', 11),
                                       foreground=self.colors['text_primary'],
                                       background=self.colors['chat_user'],
                                       lmargin1=24,
                                       lmargin2=24,
                                       rmargin=24,
                                       spacing1=4,
                                       spacing2=2,
                                       spacing3=4)
        self.chat_display.tag_configure('user_bubble',
                                       background=self.colors['chat_user'],
                                       relief='flat',
                                       borderwidth=0)
        
        self.chat_display.tag_configure('ai_header',
                                       font=('Segoe UI', 10, 'bold'),
                                       foreground=self.colors['success'],
                                       background=self.colors['chat_ai'])
        self.chat_display.tag_configure('ai_message',
                                       font=('Segoe UI', 11),
                                       foreground=self.colors['text_primary'],
                                       background=self.colors['chat_ai'],
                                       lmargin1=24,
                                       lmargin2=24,
                                       rmargin=24,
                                       spacing1=4,
                                       spacing2=2,
                                       spacing3=4)
        self.chat_display.tag_configure('ai_bubble',
                                       background=self.colors['chat_ai'],
                                       relief='flat',
                                       borderwidth=0)
        
        self.chat_display.tag_configure('system_header',
                                       font=('Segoe UI', 9),
                                       foreground=self.colors['text_tertiary'],
                                       background=self.colors['surface'])
        self.chat_display.tag_configure('system_message',
                                       font=('Segoe UI', 10),
                                       foreground=self.colors['text_secondary'],
                                       background=self.colors['surface'],
                                       lmargin1=20,
                                       spacing1=2)
        
        # Input Section - Modern Design
        input_section = tk.Frame(chat_card, bg=self.colors['surface'], padx=24)
        input_section.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 24))
        input_section.columnconfigure(0, weight=1)
        
        # Modern input container
        input_container = tk.Frame(input_section, bg=self.colors['surface'])
        input_container.grid(row=0, column=0, sticky=(tk.W, tk.E))
        input_container.columnconfigure(0, weight=1)
        
        # Modern entry field with placeholder
        entry_frame = tk.Frame(input_container, bg=self.colors['surface'], 
                              highlightbackground=self.colors['border'],
                              highlightthickness=1,
                              highlightcolor=self.colors['primary'])
        entry_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 12))
        entry_frame.columnconfigure(0, weight=1)
        
        self.symptom_entry = tk.Entry(entry_frame,
                                      font=('Segoe UI', 12),
                                      bg=self.colors['surface'],
                                      fg=self.colors['text_primary'],
                                      relief='flat',
                                      borderwidth=0,
                                      insertbackground=self.colors['primary'])
        self.symptom_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=16, pady=14)
        
        # Placeholder functionality
        self.placeholder_text = "Describe your symptoms (e.g., fever, headache, nausea)..."
        self.symptom_entry.insert(0, self.placeholder_text)
        self.symptom_entry.config(fg=self.colors['text_tertiary'])
        
        def on_entry_click(event):
            if self.symptom_entry.get() == self.placeholder_text:
                self.symptom_entry.delete(0, tk.END)
                self.symptom_entry.config(fg=self.colors['text_primary'])
        
        def on_focus_out(event):
            if not self.symptom_entry.get():
                self.symptom_entry.insert(0, self.placeholder_text)
                self.symptom_entry.config(fg=self.colors['text_tertiary'])
        
        def on_focus_in(event):
            entry_frame.config(highlightbackground=self.colors['primary'],
                             highlightthickness=2)
        
        def on_focus_out_frame(event):
            entry_frame.config(highlightbackground=self.colors['border'],
                             highlightthickness=1)
        
        self.symptom_entry.bind('<FocusIn>', on_entry_click)
        self.symptom_entry.bind('<FocusOut>', on_focus_out)
        entry_frame.bind('<FocusIn>', on_focus_in)
        entry_frame.bind('<FocusOut>', on_focus_out_frame)
        
        # Modern send button
        self.send_button = ttk.Button(input_container,
                                     text="🔍 Analyze",
                                     command=self.analyze_symptoms,
                                     style='Primary.TButton',
                                     width=15)
        self.send_button.grid(row=0, column=1)
        
        # Bind Enter key
        self.symptom_entry.bind('<Return>', lambda e: self.analyze_symptoms())
        
        # Control Buttons Section - Modern Layout
        controls_section = tk.Frame(main_container, bg=self.colors['background'])
        controls_section.grid(row=2, column=0, sticky=(tk.W, tk.E))
        controls_section.columnconfigure(0, weight=1)
        
        buttons_container = tk.Frame(controls_section, bg=self.colors['background'])
        buttons_container.pack()
        
        # Modern secondary buttons
        self.suggestions_button = ttk.Button(buttons_container,
                                           text="📋 Symptoms",
                                           command=self.show_suggestions,
                                           style='Secondary.TButton',
                                           width=14)
        self.suggestions_button.pack(side=tk.LEFT, padx=(0, 8))
        
        self.patient_button = ttk.Button(buttons_container,
                                        text="👤 Profile",
                                        command=self.set_patient_info,
                                        style='Secondary.TButton',
                                        width=14)
        self.patient_button.pack(side=tk.LEFT, padx=(0, 8))
        
        self.clear_button = ttk.Button(buttons_container,
                                      text="🗑️ Clear",
                                      command=self.clear_chat,
                                      style='Secondary.TButton',
                                      width=14)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 8))
        
        self.help_button = ttk.Button(buttons_container,
                                     text="❓ Help",
                                     command=self.show_help,
                                     style='Secondary.TButton',
                                     width=14)
        self.help_button.pack(side=tk.LEFT)
        
        # Initially disable input
        self.symptom_entry.config(state='disabled')
        self.send_button.config(state='disabled')
        self.suggestions_button.config(state='disabled')
        self.clear_button.config(state='disabled')
        self.patient_button.config(state='disabled')
    
    def initialize_chatbot(self):
        """Initialize the chatbot in a separate thread."""
        def init_thread():
            try:
                self.chatbot = MedicalDiagnosisChatbot()
                
                # Load data
                self.update_status("🔄 Loading medical data...")
                if not self.chatbot.load_data():
                    self.update_status("❌ Failed to load data files", error=True)
                    return
                
                # Train model
                self.update_status("🤖 Training AI model...")
                if not self.chatbot.train_model():
                    self.update_status("❌ Failed to train model", error=True)
                    return
                
                # Success
                self.update_status("✅ AI model ready! You can start chatting.", success=True)
                self.is_initialized = True
                self.enable_input()
                self.add_message("System", "🏥 AI Medical Diagnosis Assistant is ready!", 'system')
                self.add_message("System", "💡 Enter your symptoms to get started. Click 'Help' for assistance.", 'system')
                
            except Exception as e:
                self.update_status(f"❌ Error: {str(e)}", error=True)
                messagebox.showerror("Error", f"Failed to initialize chatbot:\n{str(e)}")
        
        # Start initialization thread
        thread = threading.Thread(target=init_thread, daemon=True)
        thread.start()
    
    def update_status(self, message, error=False, success=False):
        """Update the status label with modern styling."""
        def update():
            if error:
                self.status_label.config(text=message, style='Error.TLabel')
            elif success:
                self.status_label.config(text=message, style='Success.TLabel')
            else:
                self.status_label.config(text=message, style='Info.TLabel')
            
            if success or error:
                self.progress.stop()
                self.progress.pack_forget()
        
        self.root.after(0, update)
    
    def enable_input(self):
        """Enable input controls."""
        def enable():
            self.symptom_entry.config(state='normal')
            self.send_button.config(state='normal')
            self.suggestions_button.config(state='normal')
            self.clear_button.config(state='normal')
            self.patient_button.config(state='normal')
            self.symptom_entry.focus()
        
        self.root.after(0, enable)
    
    def add_message(self, sender, message, message_type='info'):
        """Add a message to the chat display with modern 2025 styling."""
        def add():
            self.chat_display.config(state='normal')
            
            # Add timestamp
            timestamp = datetime.now().strftime("%H:%M")
            
            # Store in conversation history
            self.current_session.append({
                'timestamp': timestamp,
                'sender': sender,
                'message': message,
                'type': message_type
            })
            
            # Format message based on type with modern bubbles
            if message_type == 'user':
                # User message with modern bubble
                self.chat_display.insert(tk.END, f"👤 You • {timestamp}\n", 'user_header')
                self.chat_display.insert(tk.END, f"{message}\n", 'user_message')
                self.chat_display.insert(tk.END, "\n", 'user_bubble')
            elif message_type == 'ai':
                # AI message with modern bubble
                self.chat_display.insert(tk.END, f"🤖 AI Doctor • {timestamp}\n", 'ai_header')
                self.chat_display.insert(tk.END, f"{message}\n", 'ai_message')
                self.chat_display.insert(tk.END, "\n", 'ai_bubble')
            else:
                # System message
                self.chat_display.insert(tk.END, f"💬 {sender} • {timestamp}\n", 'system_header')
                self.chat_display.insert(tk.END, f"{message}\n\n", 'system_message')
            
            # Scroll to bottom
            self.chat_display.see(tk.END)
            self.chat_display.config(state='disabled')
        
        self.root.after(0, add)
    
    def analyze_symptoms(self):
        """Analyze the entered symptoms."""
        if not self.is_initialized:
            messagebox.showwarning("Warning", "AI model is still initializing. Please wait.")
            return
        
        symptoms_text = self.symptom_entry.get().strip()
        if not symptoms_text or symptoms_text == self.placeholder_text:
            messagebox.showwarning("Warning", "Please enter some symptoms.")
            return
        
        # Clear input
        self.symptom_entry.delete(0, tk.END)
        self.symptom_entry.insert(0, self.placeholder_text)
        self.symptom_entry.config(fg=self.colors['text_tertiary'])
        
        # Add user message
        self.add_message("You", symptoms_text, 'user')
        
        # Disable input during analysis
        self.symptom_entry.config(state='disabled')
        self.send_button.config(state='disabled')
        self.send_button.config(text="⏳ Analyzing...")
        
        # Analyze in separate thread
        def analyze_thread():
            try:
                # Parse symptoms
                symptoms = [s.strip() for s in symptoms_text.split(',')]
                symptoms = [s for s in symptoms if s]
                
                # Get diagnosis
                diagnosis = self.chatbot.diagnose(symptoms)
                
                # Display results
                if "error" in diagnosis:
                    self.add_message("AI", f"❌ {diagnosis['error']}", 'ai')
                    if diagnosis.get('invalid_symptoms'):
                        self.add_message("AI", f"💡 Invalid symptoms: {', '.join(diagnosis['invalid_symptoms'])}", 'ai')
                        self.add_message("AI", "💡 Try these common symptoms: fever, headache, nausea, cough, fatigue, pain, sweating, dizziness", 'ai')
                else:
                    # Format diagnosis report
                    report = self.format_diagnosis_report(diagnosis)
                    self.add_message("AI", report, 'ai')
                
            except Exception as e:
                self.add_message("System", f"❌ Error: Analysis failed: {str(e)}", 'system')
            finally:
                # Re-enable input
                def re_enable():
                    self.symptom_entry.config(state='normal')
                    self.send_button.config(state='normal')
                    self.send_button.config(text="🔍 Analyze")
                    self.symptom_entry.focus()
                
                self.root.after(0, re_enable)
        
        # Start analysis thread
        thread = threading.Thread(target=analyze_thread, daemon=True)
        thread.start()
    
    def format_diagnosis_report(self, diagnosis):
        """Format the diagnosis results with modern styling."""
        report = "🔍 DIAGNOSIS RESULTS\n\n"
        
        # Valid symptoms
        report += f"✅ Valid Symptoms: {', '.join(diagnosis['valid_symptoms'])}\n\n"
        
        # Top predictions with modern formatting
        report += "🎯 Top 3 Predictions:\n"
        for i, (disease, confidence) in enumerate(diagnosis['top_predictions'], 1):
            confidence_pct = confidence * 100
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            report += f"   {emoji} {disease} ({confidence_pct:.1f}% confidence)\n"
        
        # Treatment
        report += f"\n💊 Treatment Suggestion:\n   {diagnosis['treatment']}"
        
        # Invalid symptoms
        if diagnosis.get('invalid_symptoms'):
            report += f"\n\n⚠️ Unrecognized symptoms: {', '.join(diagnosis['invalid_symptoms'])}"
        
        # Disclaimer
        report += f"\n\n⚠️ Remember: This is for educational purposes only. Always consult a healthcare professional."
        
        return report
    
    def show_suggestions(self):
        """Show available symptoms in a modern window."""
        if not self.is_initialized:
            messagebox.showwarning("Warning", "AI model is still initializing. Please wait.")
            return
        
        suggestions_window = tk.Toplevel(self.root)
        suggestions_window.title("📋 Available Symptoms")
        suggestions_window.geometry("700x600")
        suggestions_window.configure(bg=self.colors['background'])
        suggestions_window.resizable(True, True)
        
        # Center window
        suggestions_window.update_idletasks()
        x = (suggestions_window.winfo_screenwidth() // 2) - (suggestions_window.winfo_width() // 2)
        y = (suggestions_window.winfo_screenheight() // 2) - (suggestions_window.winfo_height() // 2)
        suggestions_window.geometry(f"+{x}+{y}")
        
        # Modern container
        main_frame = tk.Frame(suggestions_window, bg=self.colors['background'], padx=24, pady=24)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame,
                         text="📋 Available Symptoms",
                         style='Header.TLabel')
        title.pack(pady=(0, 16))
        
        # Modern text widget
        text_widget = scrolledtext.ScrolledText(main_frame,
                                               font=('Segoe UI', 10),
                                               bg=self.colors['surface'],
                                               fg=self.colors['text_primary'],
                                               wrap=tk.WORD,
                                               padx=16,
                                               pady=16,
                                               relief='flat',
                                               borderwidth=1,
                                               highlightthickness=1,
                                               highlightbackground=self.colors['border'])
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Add content
        text_widget.insert(tk.END, "🔍 COMMON SYMPTOMS YOU CAN TRY:\n", 'bold')
        text_widget.insert(tk.END, "=" * 60 + "\n\n")
        
        common_symptoms = [
            'fever', 'headache', 'nausea', 'vomiting', 'cough', 'sneezing',
            'rash', 'fatigue', 'weakness', 'pain', 'breathing', 'dizziness',
            'anxiety', 'depression', 'constipation', 'diarrhea', 'sweating',
            'trembling', 'cold', 'itching', 'swelling'
        ]
        
        for i, symptom in enumerate(common_symptoms, 1):
            text_widget.insert(tk.END, f"{i:2d}. {symptom}\n")
        
        text_widget.insert(tk.END, f"\n\n📋 ALL AVAILABLE SYMPTOMS ({len(self.chatbot.all_symptoms)}):\n", 'bold')
        text_widget.insert(tk.END, "=" * 60 + "\n\n")
        
        for i, symptom in enumerate(self.chatbot.all_symptoms, 1):
            text_widget.insert(tk.END, f"{i:3d}. {symptom}\n")
        
        text_widget.tag_configure('bold', font=('Segoe UI', 11, 'bold'))
        text_widget.config(state=tk.DISABLED)
    
    def clear_chat(self):
        """Clear the chat display."""
        self.chat_display.config(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state='disabled')
        self.current_session = []
        self.add_message("System", "💬 Chat cleared. Ready for new conversation.", 'system')
    
    def set_patient_info(self):
        """Set patient information in a modern dialog."""
        dialog = PatientInfoDialog(self.root, self.patient_info, self.colors)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.patient_info = dialog.result
            self.add_message("System", 
                           f"👤 Patient profile updated: {self.patient_info['name']}, {self.patient_info['age']}, {self.patient_info['gender']}", 
                           'system')
    
    def show_help(self):
        """Show help information in a modern dialog."""
        help_text = """🏥 AI Medical Diagnosis Assistant - Help Guide

HOW TO USE:
1. Enter your symptoms in the text box (e.g., "fever, headache, nausea")
2. Click "Analyze" or press Enter
3. View the AI's diagnosis and treatment suggestions

FEATURES:
• Enter symptoms separated by commas
• Click "Symptoms" to see all available symptoms
• Click "Profile" to set your information
• Click "Clear" to start over

TIPS:
• Use common symptom names (fever, headache, etc.)
• Enter multiple related symptoms for better accuracy
• The AI will suggest similar symptoms if yours aren't recognized

⚠️ IMPORTANT:
This is for educational purposes only. Always consult a healthcare professional for medical advice."""
        
        messagebox.showinfo("Help & Tips", help_text)

class PatientInfoDialog:
    def __init__(self, parent, current_info, colors):
        self.result = None
        self.colors = colors
        
        # Create modern dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Patient Information")
        self.dialog.geometry("500x450")
        self.dialog.configure(bg=self.colors['background'])
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Create form
        self.create_form(current_info)
    
    def create_form(self, current_info):
        """Create the modern patient information form."""
        main_frame = tk.Frame(self.dialog, bg=self.colors['background'], padx=32, pady=32)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, 
                               text="Patient Information",
                               font=('Segoe UI', 16, 'bold'),
                               bg=self.colors['background'],
                               fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 24))
        
        # Name
        name_frame = tk.Frame(main_frame, bg=self.colors['background'])
        name_frame.pack(fill=tk.X, pady=(0, 16))
        
        ttk.Label(name_frame, text="Name:", style='Body.TLabel').pack(anchor=tk.W, pady=(0, 6))
        self.name_entry = tk.Entry(name_frame,
                                   font=('Segoe UI', 11),
                                   bg=self.colors['surface'],
                                   fg=self.colors['text_primary'],
                                   relief='flat',
                                   borderwidth=1,
                                   highlightthickness=1,
                                   highlightbackground=self.colors['border'],
                                   highlightcolor=self.colors['primary'])
        self.name_entry.pack(fill=tk.X, padx=12, pady=10)
        self.name_entry.insert(0, current_info.get('name', ''))
        
        # Age
        age_frame = tk.Frame(main_frame, bg=self.colors['background'])
        age_frame.pack(fill=tk.X, pady=(0, 16))
        
        ttk.Label(age_frame, text="Age:", style='Body.TLabel').pack(anchor=tk.W, pady=(0, 6))
        self.age_entry = tk.Entry(age_frame,
                                  font=('Segoe UI', 11),
                                  bg=self.colors['surface'],
                                  fg=self.colors['text_primary'],
                                  relief='flat',
                                  borderwidth=1,
                                  highlightthickness=1,
                                  highlightbackground=self.colors['border'],
                                  highlightcolor=self.colors['primary'])
        self.age_entry.pack(fill=tk.X, padx=12, pady=10)
        self.age_entry.insert(0, current_info.get('age', ''))
        
        # Gender
        gender_frame = tk.Frame(main_frame, bg=self.colors['background'])
        gender_frame.pack(fill=tk.X, pady=(0, 24))
        
        ttk.Label(gender_frame, text="Gender:", style='Body.TLabel').pack(anchor=tk.W, pady=(0, 6))
        
        gender_container = tk.Frame(gender_frame, bg=self.colors['background'])
        gender_container.pack(fill=tk.X)
        
        self.gender_var = tk.StringVar(value=current_info.get('gender', 'Male'))
        ttk.Radiobutton(gender_container, text="Male", variable=self.gender_var, value="Male").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(gender_container, text="Female", variable=self.gender_var, value="Female").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(gender_container, text="Other", variable=self.gender_var, value="Other").pack(side=tk.LEFT)
        
        # Buttons - Modern layout with proper spacing
        button_frame = tk.Frame(main_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, pady=(24, 0))
        
        # Create button container with proper spacing
        button_container = tk.Frame(button_frame, bg=self.colors['background'])
        button_container.pack(side=tk.RIGHT)
        
        # Save button (primary action) - Sky blue with white text
        save_btn = tk.Button(button_container, 
                            text="Save", 
                            command=self.save_info,
                            font=('Segoe UI', 11, 'bold'),
                            bg=self.colors['primary'],
                            fg='white',
                            activebackground=self.colors['primary_dark'],
                            activeforeground='white',
                            relief='flat',
                            borderwidth=0,
                            padx=24,
                            pady=10,
                            cursor='hand2',
                            width=12)
        save_btn.pack(side=tk.RIGHT, padx=(12, 0))
        
        # Cancel button (secondary action) - White with sky blue border
        cancel_btn = tk.Button(button_container, 
                              text="Cancel", 
                              command=self.cancel,
                              font=('Segoe UI', 11),
                              bg=self.colors['surface'],
                              fg=self.colors['text_primary'],
                              activebackground=self.colors['background'],
                              activeforeground=self.colors['primary'],
                              relief='solid',
                              borderwidth=2,
                              highlightthickness=0,
                              padx=24,
                              pady=10,
                              cursor='hand2',
                              width=12)
        cancel_btn.pack(side=tk.RIGHT)
    
    def save_info(self):
        """Save the patient information."""
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        gender = self.gender_var.get()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter a name.")
            return
        
        self.result = {
            'name': name,
            'age': age or 'Not specified',
            'gender': gender or 'Not specified'
        }
        
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel the dialog."""
        self.dialog.destroy()

def main():
    """Main function to run the GUI."""
    # Check if required files exist
    required_files = ['Training.csv', 'Diseases_Symptoms.csv', 'medical_chatbot.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        messagebox.showerror("Error", f"Missing required files:\n{', '.join(missing_files)}")
        return
    
    # Create and run the GUI
    root = tk.Tk()
    app = MedicalChatbotGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
