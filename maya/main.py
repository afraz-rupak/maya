"""
MAYA - Desktop AI Assistant Application
Main entry point for the three-panel interface with face authentication
"""

import sys
import os
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, 
    QVBoxLayout, QStackedWidget, QSplashScreen
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPalette, QColor, QPixmap, QFont


class MAYAMainWindow(QMainWindow):
    """Main application window with three-panel layout"""

    def __init__(self, skip_auth=False):
        super().__init__()
        self.setWindowTitle("MAYA - AI Assistant")
        self.setMinimumSize(1200, 800)
        self.skip_auth = skip_auth
        
        # Set dark theme
        self.setup_theme()
        
        # Create stacked widget for auth/main screens
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Initialize face recognizer
        from frontend.components.face_recognizer import FaceRecognizer
        from frontend.components.secure_storage import SecureStorage
        
        self.secure_storage = SecureStorage()
        self.face_recognizer = FaceRecognizer()
        
        # Load embeddings from secure storage
        embeddings = self.secure_storage.load_embeddings()
        if embeddings:
            self.face_recognizer.known_embeddings = embeddings
        
        # Check if first-time setup
        if self.secure_storage.check_first_time_setup() and not skip_auth:
            self.show_enrollment_screen()
        elif skip_auth:
            self.create_main_interface()
            self.stack.setCurrentWidget(self.main_widget)
        else:
            self.show_auth_screen()
    
    def show_enrollment_screen(self):
        """Show face enrollment screen for first-time setup"""
        from frontend.components.face_enrollment import FaceEnrollmentScreen
        
        self.enrollment_screen = FaceEnrollmentScreen(self.face_recognizer)
        self.enrollment_screen.enrollment_complete.connect(self.on_enrollment_complete)
        self.enrollment_screen.enrollment_cancelled.connect(self.close)
        
        self.stack.addWidget(self.enrollment_screen)
        self.stack.setCurrentWidget(self.enrollment_screen)
    
    def show_auth_screen(self):
        """Show face authentication screen"""
        from frontend.components.face_auth_screen import FaceAuthScreen
        
        self.auth_screen = FaceAuthScreen(self.face_recognizer)
        self.auth_screen.auth_success.connect(self.on_auth_success)
        self.auth_screen.auth_failed.connect(self.close)
        
        # Update PIN verification to use secure storage
        self.auth_screen.pin_screen.findChild(QWidget, 'verify_pin_btn')
        original_verify = self.auth_screen.verify_pin
        
        def secure_verify_pin():
            pin = self.auth_screen.pin_input.text()
            if self.secure_storage.verify_pin(pin):
                self.auth_screen.auth_success.emit(
                    self.secure_storage.load_config().get('owner_name', 'User')
                )
            else:
                self.auth_screen.pin_error.setText("Incorrect PIN")
                self.auth_screen.pin_input.clear()
        
        self.auth_screen.verify_pin = secure_verify_pin
        
        self.stack.addWidget(self.auth_screen)
        self.stack.setCurrentWidget(self.auth_screen)
        
        # Start authentication after brief delay
        QTimer.singleShot(500, self.auth_screen.start_authentication)
    
    def on_enrollment_complete(self, username):
        """Handle successful enrollment"""
        # Save embeddings to secure storage
        self.secure_storage.save_embeddings(self.face_recognizer.known_embeddings)
        
        # Save config with username
        config = self.secure_storage.load_config()
        config['owner_name'] = username
        self.secure_storage.save_config(config)
        
        # Create main interface
        self.create_main_interface()
        self.stack.setCurrentWidget(self.main_widget)
    
    def on_auth_success(self, username):
        """Handle successful authentication"""
        # Create main interface if not exists
        if not hasattr(self, 'main_widget'):
            self.create_main_interface()
        
        self.stack.setCurrentWidget(self.main_widget)
        
        # Add stack widget to main window
        if not hasattr(self, 'stack_added'):
            self.stack.addWidget(self.main_widget)
            self.stack_added = True
    
    def create_main_interface(self):
        """Create the main MAYA interface"""
        self.main_widget = QWidget()
        
        # Create main vertical layout to hold navbar and content
        main_container_layout = QVBoxLayout(self.main_widget)
        main_container_layout.setContentsMargins(15, 15, 15, 0)
        main_container_layout.setSpacing(15)
        
        # Add navbar at the top
        from frontend.components.navbar import NavBar
        self.navbar = NavBar()
        main_container_layout.addWidget(self.navbar)
        
        # Create horizontal layout for three panels
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #000000;")
        main_layout = QHBoxLayout(content_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create three main panels
        from frontend.components.left_panel import LeftPanel
        from frontend.components.center_panel import CenterPanel
        from frontend.components.right_panel import RightPanel
        from frontend.components.voice_listener import VoiceListener
        from frontend.components.voice_listener_api import VoiceListenerAPI
        
        self.left_panel = LeftPanel()
        self.center_panel = CenterPanel()
        self.right_panel = RightPanel()
        
        # Initialize both voice listeners
        self.voice_listener_local = VoiceListener(model_size="base", language="en")
        self.voice_listener_api = VoiceListenerAPI(language="en")
        self.current_language = "en"  # Default language
        self.model_mode = "local"  # Default to local model
        self.voice_listener = self.voice_listener_local  # Active listener
        
        # Load Whisper model in background (for local)
        model_thread = threading.Thread(target=self.voice_listener_local.load_model)
        model_thread.daemon = True
        model_thread.start()
        
        # Connect signals
        self.left_panel.project_selected.connect(self.on_project_selected)
        self.right_panel.message_sent.connect(self.on_message_sent)
        self.right_panel.language_changed.connect(self.on_language_changed_ui)
        self.right_panel.voice_button_clicked.connect(self.on_voice_button_clicked)
        self.right_panel.model_mode_changed.connect(self.on_model_mode_changed)
        
        # Connect navbar signals
        self.navbar.model_mode_changed.connect(self.on_model_mode_changed)
        self.navbar.language_changed.connect(self.on_language_changed_ui)
        
        # Connect voice listener signals for both modes
        self._connect_voice_signals(self.voice_listener_local)
        self._connect_voice_signals(self.voice_listener_api)
        
        # Set fixed widths for left and right panels (25% of typical screen width)
        # Assuming a standard 1920px width, 25% ≈ 480px, but using 400px for better fit
        self.left_panel.setFixedWidth(400)
        self.right_panel.setFixedWidth(400)
        
        # Add panels to layout - left and right are fixed width, center takes remaining space
        main_layout.addWidget(self.left_panel)
        main_layout.addWidget(self.center_panel, stretch=1)
        main_layout.addWidget(self.right_panel)
        
        # Add content widget to main container
        main_container_layout.addWidget(content_widget)
    
    def setup_theme(self):
        """Configure dark theme for the application"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(200, 210, 230))
        palette.setColor(QPalette.ColorRole.Base, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Text, QColor(200, 210, 230))
        palette.setColor(QPalette.ColorRole.Button, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(200, 210, 230))
        self.setPalette(palette)
    
    def _connect_voice_signals(self, listener):
        """Connect signals for a voice listener"""
        listener.transcription_ready.connect(self.on_transcription_ready)
        listener.listening_started.connect(self.on_listening_started)
        listener.listening_stopped.connect(self.on_listening_stopped)
        listener.error_occurred.connect(self.on_voice_error)
    
    def on_model_mode_changed(self, mode: str):
        """Handle model mode change (local/api)"""
        self.model_mode = mode
        
        if mode == "local":
            self.voice_listener = self.voice_listener_local
            self.right_panel.add_message("🖥️ Switched to Local Model (Whisper)", is_user=False)
        else:
            # Check for API key
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                self.right_panel.add_message(
                    "⚠️ OpenAI API key not found. Please set OPENAI_API_KEY environment variable.",
                    is_user=False
                )
                return
            self.voice_listener = self.voice_listener_api
            self.right_panel.add_message("☁️ Switched to API Model (OpenAI Whisper)", is_user=False)
        
        # Update language for new listener
        self.voice_listener.set_language(self.current_language)
        print(f"Model mode changed to: {mode}")
    
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
    import argparse
    
    parser = argparse.ArgumentParser(description='MAYA AI Assistant')
    parser.add_argument('--skip-auth', action='store_true', 
                       help='Skip face authentication (for development)')
    args = parser.parse_args()
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use Fusion style for better dark theme support
    
    # Create splash screen
    splash_pix = QPixmap(400, 300)
    splash_pix.fill(QColor(10, 10, 15))
    splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
    
    # Add MAYA text to splash
    from PyQt6.QtGui import QPainter
    painter = QPainter(splash_pix)
    painter.setPen(QColor(0, 212, 255))
    font = QFont("Arial", 48, QFont.Weight.Bold)
    painter.setFont(font)
    painter.drawText(splash_pix.rect(), Qt.AlignmentFlag.AlignCenter, "MAYA")
    painter.end()
    
    splash.setPixmap(splash_pix)
    splash.show()
    app.processEvents()
    
    # Initialize window
    window = MAYAMainWindow(skip_auth=args.skip_auth)
    
    # Close splash and show window
    splash.finish(window)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
