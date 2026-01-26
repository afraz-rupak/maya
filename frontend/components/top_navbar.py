"""
Top Navigation Bar for MAYA - Figma Design
Logo and toggle switches for Language and API mode
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from .custom_widgets import MayaLogo, ToggleSwitch, COLORS


class TopNavBar(QWidget):
    """Top bar with logo and toggles"""
    
    language_changed = pyqtSignal(str)  # "en" or "bn"
    model_mode_changed = pyqtSignal(str)  # "local" or "api"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(55)
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI components"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 8, 20, 8)
        
        # Logo
        logo = MayaLogo()
        layout.addWidget(logo)
        
        layout.addStretch()
        
        # Language toggle
        lang_lbl = QLabel("Language")
        lang_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        self.lang_toggle = ToggleSwitch(checked=True)
        self.lang_toggle.toggled.connect(self.on_language_toggled)
        
        layout.addWidget(lang_lbl)
        layout.addSpacing(6)
        layout.addWidget(self.lang_toggle)
        layout.addSpacing(16)
        
        # API toggle
        api_lbl = QLabel("API")
        api_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        self.api_toggle = ToggleSwitch(checked=False)  # Default to local
        self.api_toggle.toggled.connect(self.on_api_toggled)
        
        layout.addWidget(api_lbl)
        layout.addSpacing(6)
        layout.addWidget(self.api_toggle)
    
    def on_language_toggled(self, checked):
        """Handle language toggle"""
        language = "en" if checked else "bn"
        self.language_changed.emit(language)
    
    def on_api_toggled(self, checked):
        """Handle API mode toggle"""
        mode = "api" if checked else "local"
        self.model_mode_changed.emit(mode)
