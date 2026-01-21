"""
Face Authentication Screen
Biometric face unlock for MAYA application launch
"""

import os
import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QRect, pyqtProperty
from PyQt6.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QFont, QPainterPath


class CircularCameraWidget(QWidget):
    """Circular camera preview with animated scanning ring"""
    
    def __init__(self, size=280):
        super().__init__()
        self.size = size
        self.setFixedSize(size, size)
        self.frame = None
        self.ring_opacity = 0.0
        self.ring_color = QColor(0, 212, 255, 200)  # Cyan
        self.state = "scanning"  # scanning, success, failure
        
    def set_frame(self, frame):
        """Update the camera frame"""
        self.frame = frame
        self.update()
    
    def set_state(self, state):
        """Set authentication state: scanning, success, failure"""
        self.state = state
        if state == "success":
            self.ring_color = QColor(34, 197, 94, 200)  # Green
        elif state == "failure":
            self.ring_color = QColor(239, 68, 68, 200)  # Red
        else:
            self.ring_color = QColor(0, 212, 255, 200)  # Cyan
        self.update()
    
    @pyqtProperty(float)
    def ringOpacity(self):
        return self.ring_opacity
    
    @ringOpacity.setter
    def ringOpacity(self, value):
        self.ring_opacity = value
        self.update()
    
    def paintEvent(self, event):
        """Custom paint for circular camera view"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw circular camera feed
        if self.frame is not None:
            # Convert frame to QImage
            height, width = self.frame.shape[:2]
            bytes_per_line = 3 * width
            q_img = QImage(self.frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            
            # Create circular clipping path
            path = QPainterPath()
            path.addEllipse(10, 10, self.size - 20, self.size - 20)
            painter.setClipPath(path)
            
            # Draw scaled frame
            scaled_pixmap = QPixmap.fromImage(q_img).scaled(
                self.size - 20, self.size - 20,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(10, 10, scaled_pixmap)
            painter.setClipping(False)
        else:
            # Draw placeholder circle
            painter.setBrush(QColor(15, 23, 41))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(10, 10, self.size - 20, self.size - 20)
        
        # Draw animated ring
        if self.ring_opacity > 0:
            pen = QPen(self.ring_color)
            pen.setWidth(4)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(8, 8, self.size - 16, self.size - 16)
        
        # Draw face detection indicator (if state is success/failure)
        if self.state == "success":
            # Green checkmark
            painter.setPen(QPen(QColor(34, 197, 94), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawLine(self.size // 2 - 30, self.size // 2, self.size // 2 - 10, self.size // 2 + 20)
            painter.drawLine(self.size // 2 - 10, self.size // 2 + 20, self.size // 2 + 30, self.size // 2 - 20)
        elif self.state == "failure":
            # Red X
            painter.setPen(QPen(QColor(239, 68, 68), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawLine(self.size // 2 - 25, self.size // 2 - 25, self.size // 2 + 25, self.size // 2 + 25)
            painter.drawLine(self.size // 2 + 25, self.size // 2 - 25, self.size // 2 - 25, self.size // 2 + 25)


class FaceAuthScreen(QWidget):
    """Face authentication screen for application launch"""
    
    auth_success = pyqtSignal(str)  # Emits username on success
    auth_failed = pyqtSignal()
    
    def __init__(self, face_recognizer=None):
        super().__init__()
        self.face_recognizer = face_recognizer
        self.camera = None
        self.timer = None
        self.consecutive_matches = 0
        self.failed_attempts = 0
        self.max_attempts = 5
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the authentication UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Set dark background
        self.setStyleSheet("background-color: #0a0a0f;")
        
        # Stacked widget for different screens
        self.stack = QStackedWidget()
        
        # Screen 1: Face Authentication
        self.auth_screen = self.create_auth_screen()
        self.stack.addWidget(self.auth_screen)
        
        # Screen 2: Access Denied
        self.denied_screen = self.create_denied_screen()
        self.stack.addWidget(self.denied_screen)
        
        # Screen 3: PIN Entry
        self.pin_screen = self.create_pin_screen()
        self.stack.addWidget(self.pin_screen)
        
        layout.addWidget(self.stack)
        
    def create_auth_screen(self):
        """Create the main face authentication screen"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        
        # MAYA Logo
        logo_label = QLabel("MAYA")
        logo_label.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        logo_label.setStyleSheet("color: #00d4ff; letter-spacing: 8px;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        
        # Subtitle
        subtitle = QLabel("AI Assistant")
        subtitle.setFont(QFont("Arial", 16))
        subtitle.setStyleSheet("color: #6b7280;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Circular camera preview
        self.camera_widget = CircularCameraWidget(size=280)
        camera_container = QWidget()
        camera_layout = QHBoxLayout(camera_container)
        camera_layout.addWidget(self.camera_widget)
        camera_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(camera_container)
        
        # Status label
        self.status_label = QLabel("Looking for Afraz...")
        self.status_label.setFont(QFont("Arial", 14))
        self.status_label.setStyleSheet("color: #cbd5e1;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Scanning dots animation
        dots_layout = QHBoxLayout()
        dots_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dots_layout.setSpacing(8)
        
        self.dots = []
        for i in range(3):
            dot = QLabel("●")
            dot.setFont(QFont("Arial", 12))
            dot.setStyleSheet("color: #00d4ff;")
            self.dots.append(dot)
            dots_layout.addWidget(dot)
        
        dots_container = QWidget()
        dots_container.setLayout(dots_layout)
        layout.addWidget(dots_container)
        
        layout.addSpacing(40)
        
        # Use PIN button
        self.use_pin_btn = QPushButton("Use PIN Instead")
        self.use_pin_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #6b7280;
                border: 1px solid #374151;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1e293b;
                border-color: #00d4ff;
                color: #00d4ff;
            }
        """)
        self.use_pin_btn.clicked.connect(self.show_pin_screen)
        layout.addWidget(self.use_pin_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Setup ring animation
        self.ring_animation = QPropertyAnimation(self.camera_widget, b"ringOpacity")
        self.ring_animation.setDuration(1500)
        self.ring_animation.setStartValue(0.3)
        self.ring_animation.setEndValue(1.0)
        self.ring_animation.setLoopCount(-1)  # Infinite loop
        
        # Setup dots animation timer
        self.dots_timer = QTimer()
        self.dots_timer.timeout.connect(self.animate_dots)
        self.dots_index = 0
        
        return widget
    
    def create_denied_screen(self):
        """Create access denied screen"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # X icon
        x_label = QLabel("✗")
        x_label.setFont(QFont("Arial", 72))
        x_label.setStyleSheet("color: #ef4444;")
        x_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(x_label)
        
        # Message
        message = QLabel("Face Not Recognized")
        message.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        message.setStyleSheet("color: #cbd5e1;")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message)
        
        subtitle = QLabel("Access Denied")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setStyleSheet("color: #6b7280;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        # Attempt counter
        self.attempt_label = QLabel("")
        self.attempt_label.setFont(QFont("Arial", 12))
        self.attempt_label.setStyleSheet("color: #f59e0b;")
        self.attempt_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.attempt_label)
        
        layout.addSpacing(20)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        retry_btn = QPushButton("Try Again")
        retry_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 12px 32px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        retry_btn.clicked.connect(self.retry_auth)
        btn_layout.addWidget(retry_btn)
        
        pin_btn = QPushButton("Use PIN")
        pin_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #cbd5e1;
                border: 1px solid #374151;
                padding: 12px 32px;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #334155;
                border-color: #00d4ff;
            }
        """)
        pin_btn.clicked.connect(self.show_pin_screen)
        btn_layout.addWidget(pin_btn)
        
        layout.addLayout(btn_layout)
        
        return widget
    
    def create_pin_screen(self):
        """Create PIN entry screen"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Enter PIN")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #cbd5e1;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # PIN input
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setPlaceholderText("Enter 4-digit PIN")
        self.pin_input.setMaxLength(4)
        self.pin_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e293b;
                color: #cbd5e1;
                border: 2px solid #374151;
                padding: 15px 20px;
                border-radius: 10px;
                font-size: 24px;
                letter-spacing: 10px;
                text-align: center;
            }
            QLineEdit:focus {
                border-color: #00d4ff;
            }
        """)
        self.pin_input.setFixedWidth(250)
        self.pin_input.returnPressed.connect(self.verify_pin)
        layout.addWidget(self.pin_input, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Error message
        self.pin_error = QLabel("")
        self.pin_error.setFont(QFont("Arial", 12))
        self.pin_error.setStyleSheet("color: #ef4444;")
        self.pin_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.pin_error)
        
        layout.addSpacing(20)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        submit_btn = QPushButton("Submit")
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                padding: 12px 32px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16a34a;
            }
        """)
        submit_btn.clicked.connect(self.verify_pin)
        btn_layout.addWidget(submit_btn)
        
        back_btn = QPushButton("Back to Face Scan")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #cbd5e1;
                border: 1px solid #374151;
                padding: 12px 32px;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #334155;
                border-color: #00d4ff;
            }
        """)
        back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.auth_screen))
        btn_layout.addWidget(back_btn)
        
        layout.addLayout(btn_layout)
        
        return widget
    
    def animate_dots(self):
        """Animate the scanning dots"""
        for i, dot in enumerate(self.dots):
            if i == self.dots_index:
                dot.setStyleSheet("color: #00d4ff; font-size: 16px;")
            else:
                dot.setStyleSheet("color: #374151; font-size: 12px;")
        
        self.dots_index = (self.dots_index + 1) % 3
    
    def start_authentication(self):
        """Start the face authentication process"""
        self.stack.setCurrentWidget(self.auth_screen)
        self.consecutive_matches = 0
        self.failed_attempts = 0
        self.camera_widget.set_state("scanning")
        self.status_label.setText("Looking for Afraz...")
        
        # Start camera
        self.camera = cv2.VideoCapture(0)
        
        # Start animations
        self.ring_animation.start()
        self.dots_timer.start(400)
        
        # Start frame capture timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_frame)
        self.timer.start(50)  # 20 FPS
    
    def process_frame(self):
        """Process camera frame for face recognition"""
        if self.camera is None:
            return
        
        ret, frame = self.camera.read()
        if not ret:
            return
        
        # Flip and convert frame
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Update camera widget
        self.camera_widget.set_frame(rgb_frame)
        
        # Perform face recognition
        if self.face_recognizer:
            result = self.face_recognizer.recognize(frame)
            
            if result["match"]:
                self.consecutive_matches += 1
                self.status_label.setText(f"Face detected... ({self.consecutive_matches}/3)")
                
                if self.consecutive_matches >= 3:
                    self.on_auth_success(result["name"])
            else:
                if self.consecutive_matches > 0:
                    self.consecutive_matches = 0
                    self.status_label.setText("Looking for Afraz...")
    
    def on_auth_success(self, username):
        """Handle successful authentication"""
        self.stop_camera()
        self.camera_widget.set_state("success")
        self.status_label.setText(f"Welcome back, {username}!")
        
        # Emit success signal after brief delay
        QTimer.singleShot(1500, lambda: self.auth_success.emit(username))
    
    def on_auth_failure(self):
        """Handle authentication failure"""
        self.stop_camera()
        self.failed_attempts += 1
        self.camera_widget.set_state("failure")
        
        if self.failed_attempts >= self.max_attempts:
            self.attempt_label.setText(f"Maximum attempts reached. Please try again later.")
            QTimer.singleShot(2000, lambda: self.auth_failed.emit())
        else:
            self.attempt_label.setText(f"Attempt {self.failed_attempts}/{self.max_attempts}")
            QTimer.singleShot(1500, lambda: self.stack.setCurrentWidget(self.denied_screen))
    
    def retry_auth(self):
        """Retry face authentication"""
        if self.failed_attempts >= self.max_attempts:
            QMessageBox.warning(self, "Locked", "Too many failed attempts. Please wait 5 minutes.")
            return
        
        self.start_authentication()
    
    def show_pin_screen(self):
        """Show PIN entry screen"""
        self.stop_camera()
        self.pin_input.clear()
        self.pin_error.setText("")
        self.stack.setCurrentWidget(self.pin_screen)
        self.pin_input.setFocus()
    
    def verify_pin(self):
        """Verify entered PIN"""
        pin = self.pin_input.text()
        
        if len(pin) != 4:
            self.pin_error.setText("PIN must be 4 digits")
            return
        
        # TODO: Verify against stored PIN
        # For now, accept "1234" as demo
        if pin == "1234":
            self.auth_success.emit("Afraz")
        else:
            self.pin_error.setText("Incorrect PIN")
            self.pin_input.clear()
    
    def stop_camera(self):
        """Stop camera and animations"""
        if self.timer:
            self.timer.stop()
        if self.camera:
            self.camera.release()
            self.camera = None
        
        self.ring_animation.stop()
        self.dots_timer.stop()
    
    def closeEvent(self, event):
        """Cleanup on close"""
        self.stop_camera()
        event.accept()
