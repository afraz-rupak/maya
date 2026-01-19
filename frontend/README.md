# MAYA Frontend

Desktop AI assistant application with three-panel interface for computer vision and machine learning project integration.

## Architecture Overview

### Layout Structure
```
┌─────────────┬──────────────────────┬─────────────┐
│             │                      │             │
│   Left      │      Center          │    Right    │
│  Navigation │   AI Interaction     │ Conversation│
│  & Projects │   (Waveform)         │   History   │
│             │                      │             │
│             ├──────────────────────┤             │
│             │   Camera Feed        │             │
└─────────────┴──────────────────────┴─────────────┘
```

## Directory Structure

```
frontend/
├── assets/          # Images, icons, fonts
├── components/      # UI components
│   ├── left_panel.py       # Navigation & Projects
│   ├── center_panel.py     # Waveform visualization
│   ├── right_panel.py      # Conversation interface
│   ├── camera_feed.py      # Webcam display
│   └── waveform.py         # Audio visualization
├── styles/          # CSS/QSS styling
├── utils/           # Helper functions
└── main.py          # Application entry point
```

## Key Features

### Left Panel: Navigation & Projects
- MAYA logo/branding
- Scrollable ML/CV project list
- Add Project functionality
- Active/inactive project states

### Center Panel: AI Interaction
- Animated audio waveform (60fps)
- Real-time frequency visualization
- State indicators:
  - Listening
  - Processing
  - Speaking

### Right Panel: Conversation
- Chat history display
- User/AI message distinction
- Auto-scroll to latest

### Camera Feed
- Live webcam preview
- Minimize/expand options
- User self-view

## Technology Stack

- **Framework**: PyQt6 (cross-platform desktop)
- **Audio Visualization**: NumPy + FFT processing
- **Camera**: OpenCV
- **Animation**: PyQt6 QPropertyAnimation
- **Styling**: QSS (Qt Style Sheets)

## Getting Started

1. Install dependencies:
   ```bash
   pip install PyQt6 opencv-python numpy pyaudio
   ```

2. Run the application:
   ```bash
   python frontend/main.py
   ```

## Visual Hierarchy

1. Center waveform (primary interaction feedback)
2. Conversation panel (information exchange)
3. Camera feed (secondary awareness)
4. Project list (utility/navigation)
5. Logo (branding)
