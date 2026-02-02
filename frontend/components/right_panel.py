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
        
        # Message bubble with text
        bubble = QFrame()
        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(10, 8, 10, 8)
        
        message_label = QLabel(text)
        message_label.setWordWrap(True)
        message_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 12px;
            background: transparent;
            border: none;
        """)
        bubble_layout.addWidget(message_label)
        
        if is_user:
            bubble.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['chat_user']};
                    border-radius: 10px;
                }}
            """)
            bubble.setMinimumWidth(80)
            bubble.setMaximumWidth(160)
            layout.addWidget(bubble)
            layout.addStretch()
            layout.addWidget(avatar)
        else:
            bubble.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['chat_ai']};
                    border-radius: 10px;
                }}
            """)
            bubble.setMinimumWidth(80)
            bubble.setMaximumWidth(160)
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
        self.setFixedWidth(280)
        self.setStyleSheet(f"""
            QFrame#rightPanel {{
                background-color: #000000;
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
        
        # Scrollable chat area
        from PyQt6.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #1a1a1a;
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #3a3a3a;
                border-radius: 3px;
            }
        """)
        
        # Chat messages container
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setContentsMargins(0, 8, 0, 0)
        self.chat_layout.setSpacing(8)
        self.chat_layout.addStretch()
        
        scroll.setWidget(self.chat_widget)
        layout.addWidget(scroll, stretch=1)
    
    def add_message(self, text: str, is_user: bool):
        """Add a message to the conversation"""
        # Remove the stretch if it exists
        if self.chat_layout.count() > 0:
            item = self.chat_layout.takeAt(self.chat_layout.count() - 1)
            # Don't call deleteLater on spacer items
        
        # Add new message bubble
        bubble = ChatBubble(text=text, is_user=is_user)
        self.chat_layout.addWidget(bubble)
        
        # Add stretch at the end
        self.chat_layout.addStretch()
    
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
