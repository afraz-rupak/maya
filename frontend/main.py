"""
MAYA - Desktop AI Assistant Application
Main entry point for the three-panel interface
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor


class MAYAMainWindow(QMainWindow):
    """Main application window with three-panel layout"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MAYA - AI Assistant")
        self.setMinimumSize(1200, 800)
        
        # Set dark theme
        self.setup_theme()
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create three main panels
        from components.left_panel import LeftPanel
        from components.center_panel import CenterPanel
        from components.right_panel import RightPanel
        
        self.left_panel = LeftPanel()
        self.center_panel = CenterPanel()
        self.right_panel = RightPanel()
        
        # Connect signals
        self.left_panel.project_selected.connect(self.on_project_selected)
        self.right_panel.message_sent.connect(self.on_message_sent)
        
        # Add panels to layout with stretch factors
        main_layout.addWidget(self.left_panel, stretch=2)
        main_layout.addWidget(self.center_panel, stretch=3)
        main_layout.addWidget(self.right_panel, stretch=2)
    
    def setup_theme(self):
        """Configure dark theme for the application"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(10, 15, 30))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(200, 210, 230))
        palette.setColor(QPalette.ColorRole.Base, QColor(15, 20, 35))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(20, 25, 40))
        palette.setColor(QPalette.ColorRole.Text, QColor(200, 210, 230))
        palette.setColor(QPalette.ColorRole.Button, QColor(25, 35, 60))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(200, 210, 230))
        self.setPalette(palette)
    
    def on_project_selected(self, project_name: str):
        """Handle project selection from left panel"""
        print(f"Project selected: {project_name}")
        self.right_panel.add_message(f"Switched to project: {project_name}", is_user=False)
    
    def on_message_sent(self, message: str):
        """Handle message sent from right panel"""
        print(f"User message: {message}")
        
        # Simulate AI processing
        self.center_panel.set_state('processing')
        
        # TODO: Integrate with actual AI backend
        # For now, simulate a response
        import threading
        def simulate_response():
            import time
            time.sleep(1)
            self.center_panel.set_state('speaking')
            time.sleep(2)
            
            # Add AI response
            response = f"I received your message: '{message}'. This is a placeholder response."
            self.right_panel.add_message(response, is_user=False)
            
            self.center_panel.set_state('idle')
        
        thread = threading.Thread(target=simulate_response)
        thread.start()


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use Fusion style for better dark theme support
    
    window = MAYAMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
