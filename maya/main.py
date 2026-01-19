"""
MAYA - Desktop AI Assistant Application
Main entry point for the three-panel interface
"""

import sys
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor


class MAYAMainWindow(QMainWindow):
    """Main application window with three-panel layout"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MAYA - AI Assistant")
        self.setMinimumSize(1200, 800)
        
        # Set dark theme
        self.setup_theme()
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create three main panels
        from frontend.components.left_panel import LeftPanel
        from frontend.components.center_panel import CenterPanel
        from frontend.components.right_panel import RightPanel
        from frontend.components.voice_listener import VoiceListener
        
        self.left_panel = LeftPanel()
        self.center_panel = CenterPanel()
        self.right_panel = RightPanel()
        
        # Initialize voice listener
        self.voice_listener = VoiceListener(model_size="base", language="en")
        self.current_language = "en"  # Default language
        
        # Load Whisper model in background
        model_thread = threading.Thread(target=self.voice_listener.load_model)
        model_thread.daemon = True
        model_thread.start()
        
        # Connect signals
        self.left_panel.project_selected.connect(self.on_project_selected)
        self.right_panel.message_sent.connect(self.on_message_sent)
        self.right_panel.language_changed.connect(self.on_language_changed_ui)
        self.right_panel.voice_button_clicked.connect(self.on_voice_button_clicked)
        
        # Connect voice listener signals
        self.voice_listener.transcription_ready.connect(self.on_transcription_ready)
        self.voice_listener.listening_started.connect(self.on_listening_started)
        self.voice_listener.listening_stopped.connect(self.on_listening_stopped)
        self.voice_listener.error_occurred.connect(self.on_voice_error)
        
        # Add panels to layout with stretch factors
        main_layout.addWidget(self.left_panel, stretch=2)
        main_layout.addWidget(self.center_panel, stretch=3)
        main_layout.addWidget(self.right_panel, stretch=2)
    
    def setup_theme(self):
        """Configure dark theme for the application"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(10, 15, 30))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(200, 210, 230))
        palette.setColor(QPalette.ColorRole.Base, QColor(15, 20, 35))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(20, 25, 40))
        palette.setColor(QPalette.ColorRole.Text, QColor(200, 210, 230))
        palette.setColor(QPalette.ColorRole.Button, QColor(25, 35, 60))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(200, 210, 230))
        self.setPalette(palette)
    
    def on_project_selected(self, project_name: str):
        """Handle project selection from left panel"""
        print(f"Project selected: {project_name}")
        self.right_panel.add_message(f"Switched to project: {project_name}", is_user=False)
    
    def on_message_sent(self, message: str):
        """Handle message sent from right panel"""
        print(f"User message: {message}")
        
        # Check for language change commands
        if message.lower() in ['switch to english', 'english', 'en']:
            self.change_language('en')
            self.right_panel.add_message("Language switched to English", is_user=False)
            return
        elif message.lower() in ['switch to bangla', 'bangla', 'বাংলা', 'bn']:
            self.change_language('bn')
            self.right_panel.add_message("Language switched to Bangla (বাংলা)", is_user=False)
            return
        elif message.lower() in ['listen', 'start listening', 'voice']:
            self.start_voice_listening()
            return
        
        # Simulate AI processing
        self.center_panel.set_state('processing')
        
        # TODO: Integrate with actual AI backend
        # For now, simulate a response
        def simulate_response():
            import time
            time.sleep(1)
            self.center_panel.set_state('speaking')
            time.sleep(2)
            
            # Add AI response
            response = f"I received your message: '{message}'. This is a placeholder response."
            self.right_panel.add_message(response, is_user=False)
            
            self.center_panel.set_state('idle')
        
        thread = threading.Thread(target=simulate_response)
        thread.start()


    def change_language(self, language_code: str):
        """Change voice recognition language"""
        self.current_language = language_code
        self.voice_listener.set_language(language_code)
        lang_name = "English" if language_code == "en" else "Bangla"
        print(f"Language changed to: {lang_name}")
    
    def on_language_changed_ui(self, language_code: str):
        """Handle language change from UI"""
        self.change_language(language_code)
        lang_name = "English" if language_code == "en" else "বাংলা"
        self.right_panel.add_message(f"Language switched to {lang_name}", is_user=False)
    
    def on_voice_button_clicked(self):
        """Handle voice button click from UI"""
        self.start_voice_listening()
    
    def start_voice_listening(self, duration=5):
        """Start listening for voice input"""
        print("Starting voice listening...")
        self.center_panel.set_state('listening')
        self.voice_listener.start_listening(duration=duration)
    
    def on_transcription_ready(self, text: str):
        """Handle transcription result"""
        print(f"Transcription received: {text}")
        if text:
            # Add transcribed text as user message
            self.right_panel.add_message(text, is_user=True)
            # Process it as if user typed it
            self.on_message_sent(text)
        else:
            self.right_panel.add_message("No speech detected", is_user=False)
    
    def on_listening_started(self):
        """Handle listening started"""
        print("Listening started...")
        self.center_panel.set_state('listening')
    
    def on_listening_stopped(self):
        """Handle listening stopped"""
        print("Listening stopped")
        self.center_panel.set_state('processing')
    
    def on_voice_error(self, error_message: str):
        """Handle voice listener errors"""
        print(f"Voice error: {error_message}")
        self.right_panel.add_message(f"Voice error: {error_message}", is_user=False)
        self.center_panel.set_state('idle')


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use Fusion style for better dark theme support
    
    window = MAYAMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
