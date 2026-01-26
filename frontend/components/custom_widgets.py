"""
Custom UI Widgets for MAYA - Figma Design
Includes MayaLogo, ToggleSwitch, and IconButton with SVG support
"""

import os
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QByteArray, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QPixmap
from PyQt6.QtSvg import QSvgRenderer


# ============== Color Palette (from Figma) ==============
COLORS = {
    'background': '#0D0D0D',
    'panel_bg': '#141414',
    'panel_border': '#1E1E1E',
    'card_bg': '#1E1E1E',
    'card_hover': '#252525',
    'text_primary': '#FFFFFF',
    'text_secondary': '#6B6B6B',
    'accent_cyan': '#4A9EAD',
    'accent_cyan_dark': '#2A4A50',
    'chat_user': '#1E3A3F',
    'chat_ai': '#2A3A3D',
    'button_red': '#E63946',
    'icon_gray': '#6B6B6B',
}


# ============== SVG Icons ==============
ICONS = {
    'camera_off': '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="6" width="14" height="11" rx="2" stroke="{color}" stroke-width="1.5" fill="none"/>
        <path d="M16 9L20 7V17L16 15" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="2" y1="19" x2="20" y2="5" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
    </svg>''',
    
    'camera_on': '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="6" width="14" height="11" rx="2" stroke="{color}" stroke-width="1.5" fill="none"/>
        <path d="M16 9L20 7V17L16 15" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
    </svg>''',
    
    'power': '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 3V11" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
        <path d="M18.36 6.64A9 9 0 1 1 5.64 6.64" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
    </svg>''',
    
    'mic_off': '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="9" y="2" width="6" height="11" rx="3" stroke="{color}" stroke-width="1.5" fill="none"/>
        <path d="M5 10V11C5 14.866 8.13401 18 12 18C15.866 18 19 14.866 19 11V10" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="12" y1="18" x2="12" y2="22" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="3" y1="21" x2="21" y2="3" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
    </svg>''',
    
    'mic_on': '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="9" y="2" width="6" height="11" rx="3" stroke="{color}" stroke-width="1.5" fill="none"/>
        <path d="M5 10V11C5 14.866 8.13401 18 12 18C15.866 18 19 14.866 19 11V10" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="12" y1="18" x2="12" y2="22" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
    </svg>''',
    
    'settings': '''<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="3" stroke="{color}" stroke-width="1.5" fill="none"/>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" stroke="{color}" stroke-width="1.5" fill="none"/>
    </svg>''',
}


class MayaLogo(QLabel):
    """Custom MAYA logo from SVG file"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 35)
        
        # Load the logo SVG
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'maya_logo.svg')
        
        # Use QSvgRenderer for better quality
        self.renderer = QSvgRenderer(logo_path)
        
        # Create pixmap to render the SVG
        pixmap = QPixmap(50, 35)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.renderer.render(painter)
        painter.end()
        
        self.setPixmap(pixmap)
        self.setScaledContents(True)


class ToggleSwitch(QWidget):
    """Custom toggle switch matching Figma design"""
    toggled = pyqtSignal(bool)
    
    def __init__(self, checked=True, parent=None):
        super().__init__(parent)
        self._checked = checked
        self.setFixedSize(40, 20)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def isChecked(self):
        return self._checked
    
    def setChecked(self, checked):
        self._checked = checked
        self.update()
    
    def mousePressEvent(self, event):
        self._checked = not self._checked
        self.toggled.emit(self._checked)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background track
        track_color = QColor(COLORS['accent_cyan']) if self._checked else QColor(COLORS['card_bg'])
        painter.setBrush(QBrush(track_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, 40, 20, 10, 10)
        
        # Circle knob
        painter.setBrush(QBrush(QColor('#FFFFFF')))
        knob_x = 22 if self._checked else 2
        painter.drawEllipse(knob_x, 2, 16, 16)


class IconButton(QPushButton):
    """Button with SVG icon"""
    def __init__(self, icon_name, color=None, size=20, parent=None):
        super().__init__(parent)
        self.icon_name = icon_name
        self.icon_color = color or COLORS['icon_gray']
        self.icon_size = size
        self.setFixedSize(36, 36)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 18px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.08);
            }
        """)
    
    def setIconName(self, icon_name):
        """Change the icon dynamically"""
        self.icon_name = icon_name
        self.update()
    
    def setIconColor(self, color):
        """Change the icon color dynamically"""
        self.icon_color = color
        self.update()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self.icon_name in ICONS:
            svg_data = ICONS[self.icon_name].format(color=self.icon_color)
            renderer = QSvgRenderer(QByteArray(svg_data.encode()))
            
            # Center the icon
            x = (self.width() - self.icon_size) // 2
            y = (self.height() - self.icon_size) // 2
            renderer.render(painter, QRectF(x, y, self.icon_size, self.icon_size))
