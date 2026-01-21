"""
Face Enrollment Screen
First-time setup for face authentication
"""

import cv2
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QProgressBar, QLineEdit
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap, QFont


class FaceEnrollmentScreen(QWidget):
    """Face enrollment screen for first-time setup"""
    
    enrollment_complete = pyqtSignal(str)  # Emits username on completion
    enrollment_cancelled = pyqtSignal()
    
    def __init__(self, face_recognizer=None):
        super().__init__()
        self.face_recognizer = face_recognizer
        self.camera = None
        self.timer = None
        self.captured_frames = []
        self.total_frames_needed = 5
        self.username = ""
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize enrollment UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(25)
        
        self.setStyleSheet("background-color: #0a0a0f;")
        
        # Title
        title = QLabel("Set Up Face Unlock")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #00d4ff;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("We'll capture your face from different angles for better recognition")
        subtitle.setFont(QFont("Arial", 13))
        subtitle.setStyleSheet("color: #9ca3af;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Username input (hidden initially)
        self.username_container = QWidget()
        username_layout = QVBoxLayout(self.username_container)
        username_layout.setSpacing(10)
        
        username_label = QLabel("Enter Your Name:")
        username_label.setFont(QFont("Arial", 12))
        username_label.setStyleSheet("color: #cbd5e1;")
        username_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("e.g., Afraz")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e293b;
                color: #cbd5e1;
                border: 2px solid #374151;
                padding: 12px 16px;
                border-radius: 8px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border-color: #00d4ff;
            }
        """)
        self.username_input.returnPressed.connect(self.start_capture)
        username_layout.addWidget(self.username_input)
        
        layout.addWidget(self.username_container)
        
        # Camera preview
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(640, 480)
        self.preview_label.setStyleSheet("""
            QLabel {
                background-color: #1e293b;
                border: 3px solid #374151;
                border-radius: 12px;
            }
        """)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.hide()
        layout.addWidget(self.preview_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Instructions
        self.instruction_label = QLabel("")
        self.instruction_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.instruction_label.setStyleSheet("color: #00d4ff;")
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instruction_label.hide()
        layout.addWidget(self.instruction_label)
        
        # Progress bar
        self.progress_container = QWidget()
        progress_layout = QVBoxLayout(self.progress_container)
        progress_layout.setSpacing(10)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.total_frames_needed)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1e293b;
                border: 2px solid #374151;
                border-radius: 8px;
                height: 30px;
                text-align: center;
                color: #cbd5e1;
                font-size: 13px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:1 #22c55e);
                border-radius: 6px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("0 / 5 captures")
        self.progress_label.setFont(QFont("Arial", 12))
        self.progress_label.setStyleSheet("color: #9ca3af;")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout.addWidget(self.progress_label)
        
        self.progress_container.hide()
        layout.addWidget(self.progress_container)
        
        layout.addSpacing(20)
        
        # Buttons
        self.button_container = QWidget()
        button_layout = QHBoxLayout(self.button_container)
        button_layout.setSpacing(15)
        
        self.start_btn = QPushButton("Start Enrollment")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                padding: 15px 40px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16a34a;
            }
            QPushButton:disabled {
                background-color: #374151;
                color: #6b7280;
            }
        """)
        self.start_btn.clicked.connect(self.start_capture)
        button_layout.addWidget(self.start_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #cbd5e1;
                border: 2px solid #374151;
                padding: 15px 40px;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #334155;
                border-color: #ef4444;
                color: #ef4444;
            }
        """)
        self.cancel_btn.clicked.connect(self.cancel_enrollment)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(self.button_container, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Capture button (hidden initially)
        self.capture_btn = QPushButton("📸 Capture")
        self.capture_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 18px 50px;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        self.capture_btn.clicked.connect(self.capture_frame)
        self.capture_btn.hide()
        layout.addWidget(self.capture_btn, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def start_capture(self):
        """Start the enrollment capture process"""
        username = self.username_input.text().strip()
        if not username:
            self.username_input.setFocus()
            return
        
        self.username = username
        
        # Hide username input, show camera
        self.username_container.hide()
        self.button_container.hide()
        self.preview_label.show()
        self.instruction_label.show()
        self.progress_container.show()
        self.capture_btn.show()
        
        self.instruction_label.setText("Position your face in the frame")
        
        # Start camera
        self.camera = cv2.VideoCapture(0)
        
        # Start preview timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_preview)
        self.timer.start(30)  # ~30 FPS
    
    def update_preview(self):
        """Update camera preview"""
        if self.camera is None:
            return
        
        ret, frame = self.camera.read()
        if not ret:
            return
        
        # Flip and convert
        frame = cv2.flip(frame, 1)
        
        # Draw face detection box if available
        if self.face_recognizer:
            face_box = self.face_recognizer.detect_face(frame)
            if face_box:
                x, y, w, h = face_box
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 212, 255), 3)
                cv2.putText(frame, "Face Detected", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 212, 255), 2)
        
        # Convert to QImage
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Display
        pixmap = QPixmap.fromImage(q_img).scaled(
            640, 480, 
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.preview_label.setPixmap(pixmap)
    
    def capture_frame(self):
        """Capture current frame for enrollment"""
        if self.camera is None:
            return
        
        ret, frame = self.camera.read()
        if not ret:
            return
        
        # Flip frame to match preview
        frame = cv2.flip(frame, 1)
        
        # Verify face is detected
        if self.face_recognizer:
            face_box = self.face_recognizer.detect_face(frame)
            if face_box is None:
                self.instruction_label.setText("⚠️ No face detected. Please try again.")
                return
        
        # Add frame to captured list
        self.captured_frames.append(frame)
        
        # Update progress
        count = len(self.captured_frames)
        self.progress_bar.setValue(count)
        self.progress_label.setText(f"{count} / {self.total_frames_needed} captures")
        
        # Update instruction based on count
        if count < self.total_frames_needed:
            instructions = [
                "Great! Now tilt your head slightly left",
                "Perfect! Now tilt your head slightly right", 
                "Excellent! Now look slightly up",
                "Almost there! Look straight ahead with a smile"
            ]
            if count - 1 < len(instructions):
                self.instruction_label.setText(instructions[count - 1])
        else:
            self.finish_enrollment()
    
    def finish_enrollment(self):
        """Complete the enrollment process"""
        self.stop_camera()
        
        self.instruction_label.setText("Processing your face data...")
        self.capture_btn.hide()
        
        # Enroll face with captured frames
        if self.face_recognizer:
            success = self.face_recognizer.enroll_face(self.username, self.captured_frames)
            
            if success:
                self.instruction_label.setText(f"✓ Face unlock ready for {self.username}!")
                self.instruction_label.setStyleSheet("color: #22c55e; font-size: 18px;")
                
                # Emit success after delay
                QTimer.singleShot(2000, lambda: self.enrollment_complete.emit(self.username))
            else:
                self.instruction_label.setText("❌ Enrollment failed. Please try again.")
                self.instruction_label.setStyleSheet("color: #ef4444; font-size: 16px;")
                
                # Show retry button
                QTimer.singleShot(2000, self.reset_enrollment)
    
    def reset_enrollment(self):
        """Reset enrollment to try again"""
        self.captured_frames = []
        self.progress_bar.setValue(0)
        self.progress_label.setText("0 / 5 captures")
        
        self.preview_label.hide()
        self.instruction_label.hide()
        self.progress_container.hide()
        self.capture_btn.hide()
        
        self.username_container.show()
        self.button_container.show()
        self.username_input.clear()
    
    def cancel_enrollment(self):
        """Cancel enrollment process"""
        self.stop_camera()
        self.enrollment_cancelled.emit()
    
    def stop_camera(self):
        """Stop camera and timer"""
        if self.timer:
            self.timer.stop()
        if self.camera:
            self.camera.release()
            self.camera = None
    
    def closeEvent(self, event):
        """Cleanup on close"""
        self.stop_camera()
        event.accept()
