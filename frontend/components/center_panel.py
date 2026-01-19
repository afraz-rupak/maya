"""
Center Panel: AI Interaction Display
Features animated waveform visualization and camera feed
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt


class CenterPanel(QWidget):
    """AI interaction panel with waveform and camera"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Import and add waveform widget
        from .waveform import WaveformWidget
        self.waveform = WaveformWidget()
        layout.addWidget(self.waveform, stretch=1)
    
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