"""
Camera Feed Widget - Figma Design
Simple camera preview matching the new UI design
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
import cv2


class CameraFeed(QWidget):
    """Minimal camera feed display matching Figma design"""
    
    def __init__(self):
        super().__init__()
        self.camera = None
        self.is_camera_on = False
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Video display label
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a1a, stop:1 #252525);
                border-radius: 8px;
                border: 1px solid #1E1E1E;
            }
        """)
        
        # Show camera icon placeholder
        self.show_placeholder()
        
        layout.addWidget(self.video_label)
    
    def show_placeholder(self):
        """Show camera icon placeholder"""
        self.video_label.setText("📷")
        self.video_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a1a, stop:1 #252525);
                border-radius: 8px;
                border: 1px solid #1E1E1E;
                color: #6B6B6B;
                font-size: 32px;
            }
        """)
    
    def toggle_camera(self):
        """Toggle camera on/off"""
        if self.is_camera_on and self.camera:
            # Turn OFF
            self.is_camera_on = False
            if hasattr(self, 'timer'):
                self.timer.stop()
            if self.camera:
                self.camera.release()
                self.camera = None
            self.show_placeholder()
            print("Camera OFF")
        else:
            # Turn ON
            self.is_camera_on = True
            self.init_camera()
            print("Camera ON")
    
    def init_camera(self):
        """Initialize camera capture"""
        if not self.is_camera_on:
            return
            
        try:
            self.camera = cv2.VideoCapture(0)
            
            # Give camera time to initialize
            import time
            time.sleep(0.3)
            
            if self.camera.isOpened():
                # Test read to verify camera access
                ret, frame = self.camera.read()
                if ret:
                    # Timer for updating frames (30 FPS)
                    self.timer = QTimer()
                    self.timer.timeout.connect(self.update_frame)
                    self.timer.start(33)  # ~30 FPS
                    print("Camera initialized successfully")
                else:
                    self.show_error("Camera access denied")
                    self.camera.release()
                    self.camera = None
                    self.is_camera_on = False
            else:
                self.show_error("Camera not available")
                self.is_camera_on = False
        except Exception as e:
            print(f"Camera error: {e}")
            self.show_error("Camera error")
            self.is_camera_on = False
    
    def show_error(self, message):
        """Show error message"""
        self.video_label.setText("⚠️")
        self.video_label.setStyleSheet("""
            QLabel {
                background: #1a1a1a;
                border-radius: 8px;
                border: 1px solid #1E1E1E;
                color: #ef4444;
                font-size: 24px;
            }
        """)
        print(f"Camera: {message}")
    
    def update_frame(self):
        """Update the video frame"""
        if self.camera and self.camera.isOpened() and self.is_camera_on:
            ret, frame = self.camera.read()
            if ret:
                # Convert frame to Qt format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)  # Mirror image
                
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                
                # Scale to fit label while maintaining aspect ratio
                scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
                    self.video_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                
                # Update stylesheet for active camera
                self.video_label.setStyleSheet("""
                    QLabel {
                        background: #000000;
                        border-radius: 8px;
                        border: 1px solid #4A9EAD;
                    }
                """)
                self.video_label.setPixmap(scaled_pixmap)
    
    def closeEvent(self, event):
        """Clean up camera on close"""
        if self.camera:
            self.camera.release()
        event.accept()
