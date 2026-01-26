"""
Center Panel: AI Interaction Display - Figma Design
Features animated waveform visualization and rounded control bar
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from .custom_widgets import IconButton, COLORS


class CenterPanel(QFrame):
    """AI interaction panel with waveform and camera"""
    
    # Signals for button actions
    camera_toggled = pyqtSignal(bool)  # True = ON, False = OFF
    end_session = pyqtSignal()  # Signal to close application
    mic_toggled = pyqtSignal(bool)  # True = unmuted, False = muted
    
    def __init__(self):
        super().__init__()
        self.camera_on = False
        self.mic_muted = True
        self.setStyleSheet(f"""
            QFrame#centerPanel {{
                background-color: #000000;
                border-radius: 12px;
            }}
        """)
        self.setObjectName("centerPanel")
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(0)
        
        # Visualization area (waveform)
        from .waveform import WaveformWidget
        self.waveform = WaveformWidget()
        layout.addWidget(self.waveform, stretch=1)
        
        # Control bar at bottom
        controls = QHBoxLayout()
        controls.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Rounded control container
        btn_container = QFrame()
        btn_container.setFixedSize(140, 44)
        btn_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['card_bg']};
                border-radius: 22px;
            }}
        """)
        
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(14, 0, 14, 0)
        btn_layout.setSpacing(14)
        
        # Camera button
        self.camera_button = IconButton('camera_off', COLORS['icon_gray'], 18)
        self.camera_button.clicked.connect(self.toggle_camera)
        
        # Power button (red)
        self.power_button = IconButton('power', COLORS['button_red'], 18)
        self.power_button.clicked.connect(self.end_session_clicked)
        
        # Mic button
        self.mic_button = IconButton('mic_off', COLORS['icon_gray'], 18)
        self.mic_button.clicked.connect(self.toggle_mic)
        
        btn_layout.addWidget(self.camera_button)
        btn_layout.addWidget(self.power_button)
        btn_layout.addWidget(self.mic_button)
        
        controls.addWidget(btn_container)
        layout.addLayout(controls)
    
    def toggle_camera(self):
        """Toggle camera ON/OFF"""
        self.camera_on = not self.camera_on
        if self.camera_on:
            self.camera_button.setIconName('camera_on')
            self.camera_button.setIconColor(COLORS['accent_cyan'])
        else:
            self.camera_button.setIconName('camera_off')
            self.camera_button.setIconColor(COLORS['icon_gray'])
        self.camera_toggled.emit(self.camera_on)
    
    def toggle_mic(self):
        """Toggle microphone mute/unmute"""
        self.mic_muted = not self.mic_muted
        if self.mic_muted:
            self.mic_button.setIconName('mic_off')
            self.mic_button.setIconColor(COLORS['icon_gray'])
        else:
            self.mic_button.setIconName('mic_on')
            self.mic_button.setIconColor(COLORS['accent_cyan'])
        self.mic_toggled.emit(not self.mic_muted)
    
    def end_session_clicked(self):
        """Handle end session button click"""
        self.end_session.emit()
    
    def set_state(self, state: str):
        """
        Set the interaction state
        Args:
            state: 'idle', 'listening', 'processing', or 'speaking'
        """
        self.waveform.set_state(state)
    
    def get_camera(self):
        """Get camera widget reference (if needed)"""
        return None