"""
Right Panel: Conversation History - Figma Design
Chat bubbles with avatars matching Figma design
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from .custom_widgets import COLORS


class ChatBubble(QWidget):
    """Chat message bubble with avatar"""
    def __init__(self, text="", is_user=False, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.text = text
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(8)
        
        # Avatar
        avatar = QLabel()
        avatar.setFixedSize(28, 28)
        avatar.setStyleSheet(f"""
            background-color: {COLORS['text_secondary'] if is_user else '#3A5A5F'};
            border-radius: 14px;
        """)
        
        # Message bubble
        bubble = QFrame()
        bubble.setFixedHeight(45)
        bubble.setMinimumWidth(80)
        bubble.setMaximumWidth(120)
        
        if is_user:
            bubble.setStyleSheet(f"""
                background-color: {COLORS['chat_user']};
                border-radius: 10px;
            """)
            layout.addWidget(bubble)
            layout.addStretch()
            layout.addWidget(avatar)
        else:
            bubble.setStyleSheet(f"""
                background-color: {COLORS['chat_ai']};
                border-radius: 10px;
            """)
            layout.addWidget(avatar)
            layout.addWidget(bubble)
            layout.addStretch()


class RightPanel(QFrame):
    """Conversation history panel"""
    
    message_sent = pyqtSignal(str)  # Signal when user sends a message
    language_changed = pyqtSignal(str)  # Signal when language is changed
    voice_button_clicked = pyqtSignal()  # Signal when voice button is clicked
    model_mode_changed = pyqtSignal(str)  # Signal when model mode is changed (local/api)
    
    def __init__(self):
        super().__init__()
        self.setFixedWidth(220)
        self.setStyleSheet(f"""
            QFrame#rightPanel {{
                background-color: #0a0a0a;
                border-radius: 12px;
            }}
        """)
        self.setObjectName("rightPanel")
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)
        
        # Header
        header = QLabel("Conversation History")
        header.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px;")
        layout.addWidget(header)
        
        # Chat messages
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        chat_layout.setContentsMargins(0, 8, 0, 0)
        chat_layout.setSpacing(6)
        
        # AI message
        chat_layout.addWidget(ChatBubble(is_user=False))
        
        # User message
        chat_layout.addWidget(ChatBubble(is_user=True))
        
        chat_layout.addStretch()
        layout.addWidget(chat_widget, stretch=1)
    
    def add_message(self, text: str, is_user: bool):
        """Add a message to the conversation"""
        # For now, just a placeholder
        # In full implementation, would add ChatBubble with text
        pass
    
    def send_message(self):
        """Handle send button click"""
        pass
    
    def on_language_changed(self, language_text: str):
        """Handle language selection change"""
        language_code = "en" if "English" in language_text else "bn"
        self.language_changed.emit(language_code)
    
    def on_model_mode_changed(self, mode_text: str):
        """Handle model mode change"""
        mode = "local" if "Local" in mode_text else "api"
        self.model_mode_changed.emit(mode)
    
    def on_voice_button_clicked(self):
        """Handle voice button click"""
        self.voice_button_clicked.emit()
