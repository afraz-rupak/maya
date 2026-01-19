"""
Navigation Bar Component for MAYA
Features toggle switches for Model Mode (Local/API) and Language (English/Bangla)
"""

import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect, pyqtProperty
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QPixmap


class ToggleSwitch(QWidget):
    """Custom toggle switch widget"""
    
    toggled = pyqtSignal(bool)  # True = ON, False = OFF
    
    def __init__(self, left_text="OFF", right_text="ON", default_state=False):
        super().__init__()
        self.left_text = left_text
        self.right_text = right_text
        self.is_on = default_state
        
        # Colors - Rounded pill style
        self.track_color = QColor(50, 50, 60)  # Dark gray track
        self.thumb_color_off = QColor(150, 150, 160)  # Gray thumb when off
        self.thumb_color_on = QColor(100, 200, 255)  # Light blue thumb when on
        self.text_color = QColor(255, 255, 255)
        self.text_color_inactive = QColor(150, 150, 160)
        
        # Dimensions - compact design
        self.setFixedSize(140, 36)
        self.track_radius = 18
        self.thumb_radius = 14
        
        # Animation
        self._thumb_position = 110 if self.is_on else 26
        self.animation = QPropertyAnimation(self, b"thumbPosition")
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setDuration(200)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def paintEvent(self, event):
        """Custom paint for toggle switch"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw rounded pill track
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.track_color)
        painter.drawRoundedRect(0, 0, 140, 36, self.track_radius, self.track_radius)
        
        # Draw text labels
        font = QFont("Arial", 9, QFont.Weight.Bold)
        painter.setFont(font)
        
        # Left text (OFF)
        painter.setPen(QPen(self.text_color if not self.is_on else self.text_color_inactive))
        left_rect = QRect(10, 0, 50, 36)
        painter.drawText(left_rect, Qt.AlignmentFlag.AlignCenter, self.left_text)
        
        # Right text (ON)
        painter.setPen(QPen(self.text_color if self.is_on else self.text_color_inactive))
        right_rect = QRect(80, 0, 50, 36)
        painter.drawText(right_rect, Qt.AlignmentFlag.AlignCenter, self.right_text)
        
        # Draw thumb (circle)
        thumb_color = self.thumb_color_on if self.is_on else self.thumb_color_off
        painter.setBrush(thumb_color)
        painter.drawEllipse(
            int(self._thumb_position - self.thumb_radius),
            int(18 - self.thumb_radius),
            self.thumb_radius * 2,
            self.thumb_radius * 2
        )
    
    def mousePressEvent(self, event):
        """Handle click to toggle"""
        self.toggle()
    
    def toggle(self):
        """Toggle the switch state"""
        self.is_on = not self.is_on
        
        # Animate thumb movement
        start_pos = self._thumb_position
        end_pos = 110 if self.is_on else 26
        
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.start()
        
        self.toggled.emit(self.is_on)
    
    def set_state(self, is_on: bool):
        """Programmatically set state"""
        if self.is_on != is_on:
            self.toggle()
    
    def getThumbPosition(self):
        return self._thumb_position
    
    def setThumbPosition(self, pos):
        self._thumb_position = pos
        self.update()  # Force repaint
    
    # Qt Property - must match the name used in QPropertyAnimation
    thumbPosition = pyqtProperty(float, getThumbPosition, setThumbPosition)


class NavBar(QWidget):
    """Navigation bar with toggle switches"""
    
    model_mode_changed = pyqtSignal(str)  # 'local' or 'api'
    language_changed = pyqtSignal(str)  # 'en' or 'bn'
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI components"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(15)
        
        # MAYA Logo on the left
        logo_container = QWidget()
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(10)
        
        # Load logo image
        logo_label = QLabel()
        logo_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 'assets', 'maya_logo.png'
        )
        
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(
                50, 50, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            logo_label.setPixmap(scaled_pixmap)
        else:
            # Fallback circle logo
            logo_label.setFixedSize(40, 40)
            logo_label.setStyleSheet("""
                QLabel {
                    background-color: #3b82f6;
                    border-radius: 20px;
                    border: none;
                }
            """)
        
        logo_layout.addWidget(logo_label)
        layout.addWidget(logo_container)
        
        # Spacer to push toggles to the right
        layout.addStretch()
        
        # Language Toggle
        language_label = QLabel("Language")
        language_label.setFont(QFont("Arial", 10))
        language_label.setStyleSheet("color: #94a3b8; border: none;")
        layout.addWidget(language_label)
        
        self.language_toggle = ToggleSwitch(
            left_text="EN",
            right_text="BN",
            default_state=False
        )
        self.language_toggle.toggled.connect(self.on_language_toggled)
        layout.addWidget(self.language_toggle)
        
        # API Toggle
        api_label = QLabel("API")
        api_label.setFont(QFont("Arial", 10))
        api_label.setStyleSheet("color: #94a3b8; border: none; margin-left: 20px;")
        layout.addWidget(api_label)
        
        self.api_toggle = ToggleSwitch(
            left_text="OFF",
            right_text="ON",
            default_state=False
        )
        self.api_toggle.toggled.connect(self.on_api_toggled)
        layout.addWidget(self.api_toggle)
        
        # Set navbar background with rounded style
        self.setStyleSheet("""
            NavBar {
                background-color: #2d2d35;
                border-radius: 25px;
            }
        """)
        
        self.setFixedHeight(50)
        self.setMinimumWidth(400)
        
        # Add shadow effect
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 120))
        self.setGraphicsEffect(shadow)
    
    def on_api_toggled(self, is_on: bool):
        """Handle API toggle"""
        mode = "api" if is_on else "local"
        self.model_mode_changed.emit(mode)
    
    def on_language_toggled(self, is_bangla: bool):
        """Handle language toggle"""
        language = "bn" if is_bangla else "en"
        self.language_changed.emit(language)
