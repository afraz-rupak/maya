# MAYA - Desktop AI Assistant 🤖

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-6.10-green?logo=qt&logoColor=white)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-orange?logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Multi-modal AI Desktop Assistant with Speech Recognition & Computer Vision**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Development Log](#development-log)

</div>

---

## 🎯 Overview

MAYA is a desktop AI assistant built with PyQt6, featuring a modern three-panel interface optimized for multi-modal interactions. It combines speech-to-text (Whisper), real-time camera feed, and conversational AI in a sleek dark blue theme.

### Key Capabilities
- 🎤 **Speech Recognition** - OpenAI Whisper with English & Bangla support
- 🎥 **Camera Integration** - Live feed with privacy controls (blur, on/off)
- 💬 **Conversational UI** - Chat interface with message history
- 🎨 **Modern Design** - Dark blue theme with smooth animations
- 🔊 **Visual Feedback** - Real-time waveform showing AI states

---

## ✨ Features

### Voice Recognition
- **Dual Mode Operation**:
  - **Local Speech-to-Text** using OpenAI Whisper (offline, privacy-first)
  - **API Mode** using OpenAI Cloud Whisper (faster, requires API key)
- **Multi-language Support**: English (`en`) and Bangla (`bn`)
- **5-second voice capture** with visual feedback
- **Toggle switching** via navbar for seamless mode changes

### User Interface
- **Three-Panel Layout** (25% : 50% : 25%):
  - 🧭 **Left Panel** (400px): Project navigation, logo, camera feed
  - 🌊 **Center Panel** (flexible): Animated waveform (listening/processing/speaking states)
  - 💬 **Right Panel** (400px): Conversation chat with language selector
- **Custom Navbar** with animated toggle switches for Language (EN/BN) and API mode (Local/Cloud)

### Camera Controls
- Live webcam preview with auto-hide control bar
- **Blur Toggle** - Gaussian blur for privacy (45×45 kernel)
- **Camera On/Off** - Disable camera when not in use
- **SVG Icons** - Professional Flaticon-style controls

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- macOS, Linux, or Windows
- Microphone access
- Webcam (optional)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/afraz-rupak/maya.git
cd maya
```

2. **Create virtual environment**
```bash
python -m venv maya_env
source maya_env/bin/activate  # On Windows: maya_env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run MAYA**
```bash
python -m maya.main
# or use the launch script
./run_maya.sh
```

---

## 📖 Usage

### Starting the Application
```bash
cd maya
source maya_env/bin/activate
python -m maya.main
```

### Voice Commands
1. Click the **🎤 Voice** button in the chat panel
2. Speak for 5 seconds
3. Transcription appears automatically

### Language Switching
- Use navbar toggle: Click **EN** / **BN** switch at top
- Or type commands: `english`, `bangla`, `en`, `bn`

### API Mode Switching
- Use navbar toggle: Click **OFF** (Local) / **ON** (API) switch
- Local mode: Offline Whisper, privacy-first
- API mode: Cloud Whisper, faster (requires `OPENAI_API_KEY`)

### Text Commands
- `listen` / `voice` - Start voice input
- `english` / `en` - Switch to English
- `bangla` / `বাংলা` / `bn` - Switch to Bangla

### Visual States
Watch the center waveform for AI status:
- 🟢 **Listening** - Recording audio
- 🟠 **Processing** - Transcribing/thinking
- 🔵 **Speaking** - AI responding
- ⚪ **Ready** - Idle state

---

## 📦 Project Structure

```
maya/
├── maya/                          # Main application module
│   ├── __init__.py
│   └── main.py                    # Application entry point (three panels + navbar)
│
├── frontend/                      # UI components
│   ├── components/
│   │   ├── navbar.py             # Custom toggle navbar (Language/API mode)
│   │   ├── left_panel.py         # Navigation & camera (400px fixed)
│   │   ├── center_panel.py       # Waveform display (flexible width)
│   │   ├── right_panel.py        # Chat interface (400px fixed)
│   │   ├── camera_feed.py        # Camera with controls
│   │   ├── waveform.py           # Video-based animation
│   │   ├── voice_listener.py     # Local Whisper (offline)
│   │   └── voice_listener_api.py # OpenAI API Whisper (cloud)
│   │
│   └── assets/
│       ├── maya_logo.png         # Transparent logo
│       └── videos/
│           └── waveform_loop.mp4 # Looping animation
│
├── requirements.txt               # Python dependencies
├── pyproject.toml                # Project metadata
├── run_maya.sh                   # Launch script
├── API_SETUP.md                  # OpenAI API configuration
├── VOICE_USAGE.md                # Voice recognition guide
├── LICENSE                       # MIT License
└── README.md                     # This file
```

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| GUI Framework | PyQt6 | 6.10.2 |
| Speech Recognition | OpenAI Whisper | 20250625 |
| Audio Capture | sounddevice | 0.5.3 |
| Computer Vision | OpenCV | 4.13.0 |
| ML Framework | PyTorch | 2.9.1 |
| Array Processing | NumPy | 2.4.0 |

---

## 📅 Development Log

### **January 20, 2026** - UI Refinement & Fixed Panel Widths
- ✅ Created custom navbar with animated toggle switches
- ✅ Implemented `pyqtProperty` for smooth animations (200ms cubic easing)
- ✅ Added Language toggle (EN/BN) and API mode toggle (Local/Cloud)
- ✅ Removed duplicate controls from right panel (model/language dropdowns)
- ✅ Set fixed panel widths: Left 400px, Right 400px, Center flexible
- ✅ Optimized layout ratios for better screen utilization
- ✅ Fixed navbar visibility and QPropertyAnimation errors
- ✅ Changed color scheme to pure black backgrounds (#000000)

### **January 20, 2026** - Voice Recognition Integration
- ✅ Implemented OpenAI Whisper for speech-to-text
- ✅ Added English and Bangla language support
- ✅ Created `voice_listener.py` component with threading
- ✅ Built `voice_listener_api.py` for cloud-based transcription
- ✅ Integrated voice button in chat panel
- ✅ Added dual-mode voice listener switching (local/API)
- ✅ Connected waveform visual feedback for listening states
- ✅ Moved `main.py` to `maya/` module folder
- ✅ Updated launch scripts and imports
- ✅ Created comprehensive voice usage documentation (`VOICE_USAGE.md`, `API_SETUP.md`)

### **January 19, 2026** - UI Refinement & Camera Controls
- ✅ Replaced animated waveform with looping video (`waveform_loop.mp4`)
- ✅ Updated logo with transparent background
- ✅ Changed color scheme to dark blue theme (#0a0f1e, #1e293b, #3b82f6)
- ✅ Added camera blur toggle functionality
- ✅ Implemented auto-hide control bar (300ms fade animation)
- ✅ Integrated Flaticon-style SVG icons for controls
- ✅ Added separate blur and camera on/off buttons
- ✅ Resolved PyQt6 SVG rendering (QtSvg module)

### **January 19, 2026** - Frontend Development
- ✅ Created three-panel desktop layout using PyQt6
- ✅ Built left panel with project navigation and camera feed
- ✅ Developed center panel with animated waveform visualization
- ✅ Implemented right panel chat interface with message bubbles
- ✅ Added signal connections between panels
- ✅ Applied dark theme with QPalette customization
- ✅ Created modular component structure

### **January 19, 2026** - Initial Setup
- ✅ Created virtual environment `maya_env`
- ✅ Installed Python 3.13 and basic libraries
- ✅ Set up project structure with Cookiecutter Data Science template
- ✅ Updated `pyproject.toml` for Python >=3.10 compatibility
- ✅ Initialized Git repository
- ✅ Created MIT LICENSE

### **January 20, 2026** - Project Cleanup
- ✅ Removed unused files (`remove_bg.py`, test videos, old logos)
- ✅ Deleted empty directories (data/, models/, notebooks/, etc.)
- ✅ Uninstalled unnecessary libraries (rembg, python-dotenv, ruff, etc.)
- ✅ Cleaned up 25+ unused dependencies
- ✅ Updated `requirements.txt` to essential packages only
- ✅ Removed ruff configuration from `pyproject.toml`
- ✅ Committed and pushed cleanup to GitHub

---

## 🔮 Roadmap

### Planned Features
- [ ] Wake word detection ("Hey MAYA")
- [ ] Continuous listening mode
- [ ] Voice activity detection (auto-stop recording)
- [ ] Text-to-speech (TTS) for AI responses
- [ ] Context-aware conversation memory
- [ ] Plugin system for custom AI models
- [ ] More language support (Hindi, Urdu, Arabic)
- [ ] Screen capture and annotation tools
- [ ] Project management features
- [ ] Export conversation history

### Backend Integration (TODO)
- [ ] Connect to LLM API (OpenAI, Anthropic, local models)
- [ ] Implement RAG (Retrieval-Augmented Generation)
- [ ] Add vector database for context storage
- [ ] Build custom AI agent workflows
- [ ] Integrate computer vision models for project list

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Afraz Ul Haque**
- GitHub: [@afraz-rupak](https://github.com/afraz-rupak)
- Repository: [maya](https://github.com/afraz-rupak/maya)

---

## 🙏 Acknowledgments

- OpenAI Whisper for state-of-the-art speech recognition
- PyQt6 for the powerful GUI framework
- Flaticon for icon design inspiration
- Cookiecutter Data Science for project template

---

<div align="center">

**Made with ❤️ for AI-powered productivity**

</div>

