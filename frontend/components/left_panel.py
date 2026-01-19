"""
Left Panel: Navigation & Projects
Displays MAYA logo and ML/CV project list
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QScrollArea, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap


class LeftPanel(QWidget):
    """Navigation and project management panel"""
    
    project_selected = pyqtSignal(str)  # Signal when project is selected
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(15)
        
        # MAYA Logo/Branding
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Load logo image
        logo_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 'assets', 'maya_logo.png'
        )
        
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            # Scale logo to fit nicely
            scaled_pixmap = pixmap.scaled(
                150, 80, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            logo_label.setPixmap(scaled_pixmap)
        else:
            # Fallback to text if image not found
            logo_label.setText("MAYA")
            logo_font = QFont("Arial", 24, QFont.Weight.Bold)
            logo_label.setFont(logo_font)
        
        logo_label.setStyleSheet("""
            QLabel {
                padding: 20px;
                border: none;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(59, 130, 246, 0.15),
                    stop:1 rgba(99, 102, 241, 0.15));
                border-radius: 10px;
            }
        """)
        layout.addWidget(logo_label)
        
        # Projects Section Header
        projects_header = QLabel("ACTIVE MODULES")
        projects_header.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        projects_header.setStyleSheet("color: #6b7280; border: none; padding: 5px; letter-spacing: 1px;")
        layout.addWidget(projects_header)
        
        # Projects List
        self.projects_list = QListWidget()
        self.projects_list.setStyleSheet("""
            QListWidget {
                background-color: #0f1729;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 5px;
                color: #cbd5e1;
            }
            QListWidget::item {
                padding: 12px;
                border-radius: 6px;
                margin: 2px 0;
            }
            QListWidget::item:hover {
                background-color: #1e293b;
            }
            QListWidget::item:selected {
                background-color: #3b82f6;
                color: #ffffff;
                font-weight: bold;
            }
        """)
        self.projects_list.itemClicked.connect(self.on_project_clicked)
        layout.addWidget(self.projects_list, stretch=1)
        
        # Add Project Button
        add_button = QPushButton("+ Add Project")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #cbd5e1;
                border: 1px solid #334155;
                padding: 12px;
                border-radius: 8px;
                font-weight: normal;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #334155;
                border-color: #3b82f6;
            }
            QPushButton:pressed {
                background-color: #0f172a;
            }
        """)
        add_button.clicked.connect(self.add_project)
        layout.addWidget(add_button)
        
        # Add camera feed at the bottom
        from .camera_feed import CameraFeed
        self.camera = CameraFeed()
        layout.addWidget(self.camera)
        
        # Add sample projects
        self.add_sample_projects()
    
    def add_sample_projects(self):
        """Add sample projects for demonstration"""
        projects = [
            "😊 Emotion Detection",
            "🧍 Pose Estimation",
            "⚠️ Anomaly Detection",
            "💬 NLP Sentiment",
        ]
        for project in projects:
            self.projects_list.addItem(project)
    
    def on_project_clicked(self, item: QListWidgetItem):
        """Handle project selection"""
        self.project_selected.emit(item.text())
    
    def add_project(self):
        """Handle add project button click"""
        # TODO: Implement project creation dialog
        print("Add new project")
