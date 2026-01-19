from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, 
    QTextEdit, QPushButton, QHBoxLayout, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class MessageWidget(QWidget):
    """Individual message bubble"""
    
    def __init__(self, text: str, is_user: bool):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        message_label = QLabel(text)
        message_label.setWordWrap(True)
        message_label.setMaximumWidth(300)
        message_label.setFont(QFont("Arial", 11))
        
        if is_user:
            # User message (right-aligned, blue)
            message_label.setStyleSheet("""
                QLabel {
                    background-color: #1e293b;
                    color: #e2e8f0;
                    padding: 12px;
                    border-radius: 12px;
                    border-bottom-right-radius: 4px;
                    border: 1px solid #334155;
                }
            """)
            layout.addStretch()
            layout.addWidget(message_label)
        else:
            # AI message (left-aligned, blue)
            message_label.setStyleSheet("""
                QLabel {
                    background-color: #3b82f6;
                    color: white;
                    padding: 12px;
                    border-radius: 12px;
                    border-bottom-left-radius: 4px;
                }
            """)
            layout.addWidget(message_label)
            layout.addStretch()


class RightPanel(QWidget):
    """Conversation history panel"""
    
    message_sent = pyqtSignal(str)  # Signal when user sends a message
    language_changed = pyqtSignal(str)  # Signal when language is changed
    voice_button_clicked = pyqtSignal()  # Signal when voice button is clicked
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(10)
        
        # Header with language selector
        header_layout = QHBoxLayout()
        
        header_label = QLabel("💬  Live Conversation Chat")
        header_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #94a3b8; border: none; padding: 5px;")
        header_layout.addWidget(header_label)
        
        header_layout.addStretch()
        
        # Language selector
        self.language_selector = QComboBox()
        self.language_selector.addItems(["English", "বাংলা (Bangla)"])
        self.language_selector.setStyleSheet("""
            QComboBox {
                background-color: #1e293b;
                color: #cbd5e1;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 5px 10px;
                min-width: 120px;
                font-size: 11px;
            }
            QComboBox:hover {
                border-color: #3b82f6;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #1e293b;
                color: #cbd5e1;
                selection-background-color: #3b82f6;
                border: 1px solid #334155;
            }
        """)
        self.language_selector.currentTextChanged.connect(self.on_language_changed)
        header_layout.addWidget(self.language_selector)
        
        layout.addLayout(header_layout)
        
        # Conversation scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #1e293b;
                border-radius: 8px;
                background-color: #0f1729;
            }
        """)
        
        # Messages container
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.messages_layout.setSpacing(8)
        
        self.scroll_area.setWidget(self.messages_widget)
        layout.addWidget(self.scroll_area, stretch=1)
        
        # Input area
        input_layout = QVBoxLayout()
        
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Type your message...")
        self.input_field.setMaximumHeight(80)
        self.input_field.setStyleSheet("""
            QTextEdit {
                background-color: #0f1729;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 10px;
                color: #cbd5e1;
                font-size: 12px;
            }
        """)
        input_layout.addWidget(self.input_field)
        
        # Send and Voice buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Voice button
        self.voice_button = QPushButton("🎤 Voice")
        self.voice_button.setStyleSheet("""
            QPushButton {
                background-color: #0ea5e9;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0284c7;
            }
            QPushButton:pressed {
                background-color: #0369a1;
            }
        """)
        self.voice_button.clicked.connect(self.on_voice_button_clicked)
        button_layout.addWidget(self.voice_button)
        
        send_button = QPushButton("Send")
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 10px 30px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        send_button.clicked.connect(self.send_message)
        button_layout.addWidget(send_button)
        
        input_layout.addLayout(button_layout)
        layout.addLayout(input_layout)
        
        # Add welcome message
        self.add_message("Initialized. I'm ready to handle your multi-modal conversions. What are we processing today?", is_user=False)
    
    def add_message(self, text: str, is_user: bool):
        """Add a message to the conversation"""
        message = MessageWidget(text, is_user)
        self.messages_layout.addWidget(message)
        
        # Auto-scroll to bottom
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )
    
    def send_message(self):
        """Handle send button click"""
        text = self.input_field.toPlainText().strip()
        if text:
            self.add_message(text, is_user=True)
            self.input_field.clear()
            self.message_sent.emit(text)
    
    def on_language_changed(self, language_text: str):
        """Handle language selection change"""
        language_code = "en" if "English" in language_text else "bn"
        self.language_changed.emit(language_code)
    
    def on_voice_button_clicked(self):
        """Handle voice button click"""
        self.voice_button_clicked.emit()
