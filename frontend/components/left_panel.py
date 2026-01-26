"""
Left Panel: Active Features & Live Camera
Figma design with feature cards and camera preview
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from .custom_widgets import COLORS


class FeatureCard(QFrame):
    """Active Features list item"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(28)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['card_bg']};
                border-radius: 6px;
            }}
        """)


class LeftPanel(QFrame):
    """Active Features panel with camera feed"""
    
    project_selected = pyqtSignal(str)  # Signal when project is selected
    
    def __init__(self):
        super().__init__()
        self.setFixedWidth(210)
        self.setStyleSheet(f"""
            QFrame#leftPanel {{
                background-color: #0a0a0a;
                border-radius: 12px;
            }}
        """)
        self.setObjectName("leftPanel")
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)
        
        # === Active Features ===
        features_widget = QWidget()
        features_layout = QVBoxLayout(features_widget)
        features_layout.setContentsMargins(0, 0, 0, 0)
        features_layout.setSpacing(8)
        
        # Header
        header = QHBoxLayout()
        header.setSpacing(0)
        
        title = QLabel("Active Features")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px; font-weight: 500;")
        
        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(20, 20)
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {COLORS['text_secondary']};
                border: none;
                font-size: 13px;
            }}
            QPushButton:hover {{ color: {COLORS['text_primary']}; }}
        """)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(settings_btn)
        features_layout.addLayout(header)
        
        # Feature buttons
        face_verification_btn = QPushButton("Face Verification")
        face_verification_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        face_verification_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['card_bg']};
                color: {COLORS['text_primary']};
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 11px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {COLORS['card_hover']};
            }}
        """)
        features_layout.addWidget(face_verification_btn)
        
        speech_recognition_btn = QPushButton("Speech Recognition")
        speech_recognition_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        speech_recognition_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['card_bg']};
                color: {COLORS['text_primary']};
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 11px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {COLORS['card_hover']};
            }}
        """)
        features_layout.addWidget(speech_recognition_btn)
        
        features_layout.addStretch()
        layout.addWidget(features_widget, stretch=1)
        
        # === Live Camera ===
        camera_widget = QWidget()
        camera_layout = QVBoxLayout(camera_widget)
        camera_layout.setContentsMargins(0, 0, 0, 0)
        camera_layout.setSpacing(6)
        
        cam_label = QLabel("Live Camera")
        cam_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px;")
        camera_layout.addWidget(cam_label)
        
        # Add actual camera feed widget
        from .camera_feed import CameraFeed
        self.camera = CameraFeed()
        self.camera.setFixedHeight(95)
        camera_layout.addWidget(self.camera)
        layout.addWidget(camera_widget)
