"""
Camera Feed Widget
Displays live webcam feed with auto-hide control bar
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QHBoxLayout, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QImage, QPixmap, QIcon, QPainter, QColor
from PyQt6.QtSvg import QSvgRenderer
import cv2


class CameraFeed(QWidget):
    """Live camera feed display with auto-hide controls"""
    
    # SVG icon definitions (Flaticon style)
    ICON_EYE = '''<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z" fill="currentColor"/>
    </svg>'''
    
    ICON_EYE_CROSSED = '''<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 6.5c2.76 0 5 2.24 5 5 0 .51-.1 1-.24 1.46l3.06 3.06c1.39-1.23 2.49-2.77 3.18-4.53C21.27 7.11 17 4 12 4c-1.27 0-2.49.2-3.64.57l2.17 2.17c.47-.14.96-.24 1.47-.24zM2.71 3.16c-.39.39-.39 1.02 0 1.41l1.97 1.97C3.06 7.83 1.77 9.53 1 11.5 2.73 15.89 7 19 12 19c1.52 0 2.97-.3 4.31-.82l2.72 2.72c.39.39 1.02.39 1.41 0 .39-.39.39-1.02 0-1.41L4.13 3.16c-.39-.39-1.03-.39-1.42 0zM12 16.5c-2.76 0-5-2.24-5-5 0-.77.18-1.5.49-2.14l1.57 1.57c-.04.18-.06.37-.06.57 0 1.66 1.34 3 3 3 .2 0 .38-.02.57-.07l1.56 1.56c-.64.32-1.37.51-2.13.51z" fill="currentColor"/>
    </svg>'''
    
    ICON_VIDEO = '''<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z" fill="currentColor"/>
    </svg>'''
    
    ICON_SETTINGS = '''<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94L14.4 2.81c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z" fill="currentColor"/>
    </svg>'''
    
    def __init__(self):
        super().__init__()
        self.camera = None
        self.is_minimized = False
        self.is_blurred = False
        self.control_bar_visible = False
        self.setup_ui()
        self.init_camera()
    
    def setup_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 10)
        layout.setSpacing(0)
        
        # Header with controls
        header_layout = QHBoxLayout()
        
        title_label = QLabel("HD CAMERA HUB")
        title_label.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Minimize/Expand button
        self.toggle_button = QPushButton("−")
        self.toggle_button.setFixedSize(25, 25)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #cbd5e1;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #334155;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_view)
        header_layout.addWidget(self.toggle_button)
        
        layout.addLayout(header_layout)
        
        # Container for video and controls
        self.video_container = QWidget()
        video_container_layout = QVBoxLayout(self.video_container)
        video_container_layout.setContentsMargins(0, 5, 0, 0)
        video_container_layout.setSpacing(0)
        
        # Video display label (with mouse tracking)
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setMinimumHeight(150)
        self.video_label.setMaximumHeight(200)
        self.video_label.setMouseTracking(True)
        self.video_label.setStyleSheet("""
            QLabel {
                background-color: #0a0f1e;
                border: 2px solid #1e293b;
                border-radius: 8px;
            }
        """)
        video_container_layout.addWidget(self.video_label)
        
        # Control bar overlay (positioned at bottom of video)
        self.control_bar = QWidget(self.video_label)
        self.control_bar.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.75);
                border-radius: 0px 0px 6px 6px;
            }
        """)
        
        # Setup opacity effect for fade in/out
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.0)
        self.control_bar.setGraphicsEffect(self.opacity_effect)
        
        # Animation for control bar
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        self.setup_control_bar()
        
        # Enable mouse tracking for hover detection
        self.video_container.setMouseTracking(True)
        self.setMouseTracking(True)
        
        layout.addWidget(self.video_container)
        
        self.setFixedHeight(240)
    
    def setup_control_bar(self):
        """Setup the slim control bar with icon buttons"""
        control_layout = QHBoxLayout(self.control_bar)
        control_layout.setContentsMargins(8, 4, 8, 4)
        
        control_layout.addStretch()
        
        # Blur toggle button
        self.blur_button = QPushButton()
        self.blur_button.setFixedSize(32, 32)
        self.blur_button.setText("👁")
        self.blur_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(107, 114, 128, 0.4);
                color: #9ca3af;
                border: none;
                border-radius: 16px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(107, 114, 128, 0.6);
            }
        """)
        self.blur_button.clicked.connect(self.toggle_blur)
        control_layout.addWidget(self.blur_button)
        
        control_layout.addSpacing(16)
        
        # Camera toggle button
        self.camera_button = QPushButton()
        self.camera_button.setFixedSize(32, 32)
        self.camera_button.setText("📹")
        self.camera_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(34, 197, 94, 0.4);
                color: #22c55e;
                border: none;
                border-radius: 16px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(34, 197, 94, 0.6);
            }
        """)
        self.camera_button.clicked.connect(self.toggle_camera)
        control_layout.addWidget(self.camera_button)
        
        control_layout.addSpacing(16)
        
        # Settings button
        self.settings_button = QPushButton()
        self.settings_button.setFixedSize(32, 32)
        self.settings_button.setText("⚙")
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(107, 114, 128, 0.4);
                color: #9ca3af;
                border: none;
                border-radius: 16px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(107, 114, 128, 0.6);
            }
        """)
        control_layout.addWidget(self.settings_button)
        
        control_layout.addStretch()
        
        # Set initial icons
        self.update_button_icons()
    
    def create_icon(self, svg_code, color, size=20):
        """Create a colored icon from SVG code"""
        # Replace currentColor with actual color
        svg_colored = svg_code.replace('currentColor', color)
        
        # Create pixmap from SVG
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        renderer = QSvgRenderer(svg_colored.encode())
        renderer.render(painter)
        painter.end()
        
        return QIcon(pixmap)
    
    def update_button_icons(self):
        """Update button icons with current state"""
        # Blur button icon
        if self.is_blurred:
            icon = self.create_icon(self.ICON_EYE_CROSSED, '#00d4ff')
        else:
            icon = self.create_icon(self.ICON_EYE, '#9ca3af')
        self.blur_button.setIcon(icon)
        self.blur_button.setIconSize(QSize(20, 20))
        self.blur_button.setText("")
        
        # Camera button icon
        if self.camera and self.camera.isOpened():
            icon = self.create_icon(self.ICON_VIDEO, '#22c55e')
        else:
            icon = self.create_icon(self.ICON_VIDEO, '#ef4444')
        self.camera_button.setIcon(icon)
        self.camera_button.setIconSize(QSize(20, 20))
        self.camera_button.setText("")
        
        # Settings button icon
        icon = self.create_icon(self.ICON_SETTINGS, '#9ca3af')
        self.settings_button.setIcon(icon)
        self.settings_button.setIconSize(QSize(20, 20))
        self.settings_button.setText("")
    
    def resizeEvent(self, event):
        """Handle resize to position control bar"""
        super().resizeEvent(event)
        if hasattr(self, 'control_bar'):
            # Position slim control bar at bottom of video label
            video_height = self.video_label.height()
            control_bar_height = 40
            self.control_bar.setGeometry(
                0, 
                video_height - control_bar_height, 
                self.video_label.width(), 
                control_bar_height
            )
    
    def enterEvent(self, event):
        """Show control bar when mouse enters"""
        super().enterEvent(event)
        if not self.is_minimized:
            self.show_controls()
    
    def leaveEvent(self, event):
        """Hide control bar when mouse leaves"""
        super().leaveEvent(event)
        if not self.is_minimized:
            self.hide_controls()
    
    def show_controls(self):
        """Fade in control bar"""
        if not self.control_bar_visible:
            self.control_bar_visible = True
            self.fade_animation.stop()
            self.fade_animation.setStartValue(self.opacity_effect.opacity())
            self.fade_animation.setEndValue(1.0)
            self.fade_animation.start()
    
    def hide_controls(self):
        """Fade out control bar"""
        if self.control_bar_visible:
            self.control_bar_visible = False
            self.fade_animation.stop()
            self.fade_animation.setStartValue(self.opacity_effect.opacity())
            self.fade_animation.setEndValue(0.0)
            self.fade_animation.start()
    
    def init_camera(self):
        """Initialize camera capture"""
        try:
            self.camera = cv2.VideoCapture(0)
            
            # Give camera time to initialize
            import time
            time.sleep(0.5)
            
            if self.camera.isOpened():
                # Test read to verify camera access
                ret, frame = self.camera.read()
                if ret:
                    # Timer for updating frames (30 FPS)
                    self.timer = QTimer()
                    self.timer.timeout.connect(self.update_frame)
                    self.timer.start(33)  # ~30 FPS
                else:
                    self.show_placeholder("Camera permission required\nGrant access in System Settings")
                    self.camera.release()
                    self.camera = None
            else:
                self.show_placeholder("Camera not available\nCheck System Preferences > Privacy > Camera")
        except Exception as e:
            self.show_placeholder(f"Camera error\nPlease enable camera access")
    
    def update_frame(self):
        """Update the video frame"""
        if self.camera and self.camera.isOpened() and not self.is_minimized:
            ret, frame = self.camera.read()
            if ret:
                # Apply blur if enabled
                if self.is_blurred:
                    frame = cv2.GaussianBlur(frame, (45, 45), 20)
                
                # Convert frame to Qt format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)  # Mirror image
                
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                
                # Scale to fit label
                scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
                    self.video_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.video_label.setPixmap(scaled_pixmap)
    
    def toggle_blur(self):
        """Toggle blur effect"""
        self.is_blurred = not self.is_blurred
        
        if self.is_blurred:
            # Blur ON - cyan
            self.blur_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0, 212, 255, 0.4);
                    color: #00d4ff;
                    border: none;
                    border-radius: 16px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: rgba(0, 212, 255, 0.6);
                }
            """)
            icon = self.create_icon(self.ICON_EYE_CROSSED, '#00d4ff')
        else:
            # Blur OFF - gray
            self.blur_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(107, 114, 128, 0.4);
                    color: #9ca3af;
                    border: none;
                    border-radius: 16px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: rgba(107, 114, 128, 0.6);
                }
            """)
            icon = self.create_icon(self.ICON_EYE, '#9ca3af')
        
        self.blur_button.setIcon(icon)
        self.blur_button.setIconSize(QSize(20, 20))
    
    def toggle_camera(self):
        """Toggle camera on/off"""
        if self.camera and self.camera.isOpened():
            # Turn OFF
            self.timer.stop()
            self.camera.release()
            self.camera = None
            self.video_label.clear()
            self.show_placeholder("Camera OFF")
            self.is_blurred = False
            
            # Red button
            self.camera_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(239, 68, 68, 0.4);
                    color: #ef4444;
                    border: none;
                    border-radius: 16px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: rgba(239, 68, 68, 0.6);
                }
            """)
            icon = self.create_icon(self.ICON_VIDEO, '#ef4444')
        else:
            # Turn ON
            self.init_camera()
            
            if self.camera and self.camera.isOpened():
                # Green button
                self.camera_button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(34, 197, 94, 0.4);
                        color: #22c55e;
                        border: none;
                        border-radius: 16px;
                        font-size: 16px;
                    }
                    QPushButton:hover {
                        background-color: rgba(34, 197, 94, 0.6);
                    }
                """)
                icon = self.create_icon(self.ICON_VIDEO, '#22c55e')
        
        self.camera_button.setIcon(icon)
        self.camera_button.setIconSize(QSize(20, 20))
    
    def show_placeholder(self, message: str):
        """Show placeholder text when camera is unavailable"""
        self.video_label.setText(message)
        self.video_label.setStyleSheet("""
            QLabel {
                background-color: #0a0f1e;
                border: 2px solid #1e293b;
                border-radius: 8px;
                color: #64748b;
                font-size: 12px;
            }
        """)
    
    def toggle_view(self):
        """Toggle between minimized and expanded view"""
        self.is_minimized = not self.is_minimized
        
        if self.is_minimized:
            self.video_container.hide()
            self.toggle_button.setText("+")
            self.setFixedHeight(50)
        else:
            self.video_container.show()
            self.toggle_button.setText("−")
            self.setFixedHeight(240)
    
    def closeEvent(self, event):
        """Clean up camera on close"""
        if self.camera:
            self.camera.release()
        event.accept()
