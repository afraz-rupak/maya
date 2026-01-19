"""
Waveform Visualization Widget
Video-based audio visualization responding to speech input/output
"""

import os
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap, QFont, QColor
import cv2


class WaveformWidget(QWidget):
    """Audio waveform visualization using looping video"""
    
    IDLE = 'idle'
    LISTENING = 'listening'
    PROCESSING = 'processing'
    SPEAKING = 'speaking'
    
    def __init__(self):
        super().__init__()
        self.state = self.IDLE
        self.video_capture = None
        self.current_frame = 0
        self.total_frames = 0
        
        self.setup_ui()
        self.init_video()
        
        self.setMinimumHeight(300)
    
    def setup_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Video display label
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("background-color: #000000;")
        layout.addWidget(self.video_label, stretch=1)
        
        # State indicator overlay
        self.state_label = QLabel("Ready")
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.state_label.setStyleSheet("""
            QLabel {
                color: #64748b;
                font-size: 16px;
                font-weight: bold;
                padding: 20px;
                background-color: transparent;
            }
        """)
        layout.addWidget(self.state_label)
        layout.setStretch(0, 1)
        layout.setStretch(1, 0)
    
    def init_video(self):
        """Initialize video capture"""
        video_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 'assets', 'videos', 'waveform_loop.mp4'
        )
        
        if os.path.exists(video_path):
            self.video_capture = cv2.VideoCapture(video_path)
            self.total_frames = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Timer for video playback (30 FPS)
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(33)  # ~30 FPS
        else:
            self.video_label.setText("Video not found\nPlace maya.mp4 in assets/videos/")
            self.video_label.setStyleSheet("""
                QLabel {
                    background-color: #0a0f1e;
                    color: #64748b;
                    font-size: 14px;
                }
            """)
    
    def update_frame(self):
        """Update video frame"""
        if self.video_capture and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            
            if ret:
                # Convert frame to Qt format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                
                # Scale to fit label while maintaining aspect ratio
                scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
                    self.video_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.video_label.setPixmap(scaled_pixmap)
                
                self.current_frame += 1
            else:
                # Loop video
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.current_frame = 0
    
    def set_state(self, state: str):
        """Update the waveform state"""
        self.state = state
        
        # Update state indicator
        state_text = {
            self.IDLE: "Ready",
            self.LISTENING: "● Listening...",
            self.PROCESSING: "⟳ Processing...",
            self.SPEAKING: "♪ Speaking..."
        }
        
        state_colors = {
            self.IDLE: "#64748b",
            self.LISTENING: "#10b981",
            self.PROCESSING: "#f59e0b",
            self.SPEAKING: "#3b82f6"
        }
        
        text = state_text.get(state, "Ready")
        color = state_colors.get(state, "#646470")
        
        self.state_label.setText(text)
        self.state_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 14px;
                font-weight: bold;
                padding: 20px;
                background-color: transparent;
            }}
        """)
    
    def closeEvent(self, event):
        """Clean up video on close"""
        if self.video_capture:
            self.video_capture.release()
        event.accept()
