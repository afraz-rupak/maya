# MAYA - AI Desktop Assistant 🤖

<div align="center">

![Tauri](https://img.shields.io/badge/Tauri-2.0-24C8D8?logo=tauri&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-1.93-orange?logo=rust&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Cross-Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Cross-Platform Native Desktop AI Assistant with Voice Recognition & Face Authentication**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Architecture](#architecture)

</div>

---

## 🎯 Overview

MAYA is a **cross-platform native desktop application** built with **Tauri v2** (Rust + HTML/CSS/JS frontend), featuring a modern three-panel interface for multi-modal AI interactions. It runs natively on **macOS, Windows, and Linux**, combining biometric face authentication, speech-to-text (Whisper), real-time camera/microphone access, and conversational AI in a sleek dark theme.

### Key Capabilities
- 🖥️ **Cross-Platform** - Native apps for macOS, Windows, and Linux from single codebase
- 🔐 **Face Authentication** - Secure biometric login with encrypted storage
- 🎤 **Voice Recognition** - OpenAI Whisper with English & Bangla support
- 🎥 **Camera Integration** - Live feed with WebRTC and privacy controls
- 💬 **Conversational UI** - Chat interface with message history
- 🎨 **Modern Design** - Dark theme (Figma-based) with smooth animations
- 🔊 **Visual Feedback** - Real-time waveform showing AI states
- 🚀 **Native Performance** - Fast startup, low memory footprint (~15MB binary)
- 📦 **Easy Distribution** - .dmg (macOS), .msi/.exe (Windows), .deb/.AppImage (Linux)

---

## ✨ Features

### 🔐 Face Authentication
- **Biometric Login**: Face recognition using SFace (lightweight FaceNet)
- **Secure Enrollment**: 5-step face capture from multiple angles
- **Encrypted Storage**: Face embeddings encrypted locally (AES-128)
- **Backup PIN**: 4-digit PIN fallback authentication
- **Privacy-first**: All processing local, no cloud uploads
- **Anti-spoofing**: Live face detection prevents photo attacks

### 🎤 Voice Recognition
- **Dual Mode Operation**:
  - **Local Speech-to-Text** using OpenAI Whisper (offline, privacy-first)
  - **API Mode** using OpenAI Cloud Whisper (faster, requires API key)
- **Multi-language Support**: English (`en`) and Bangla (`bn`)
- **5-second voice capture** with visual feedback
- **Toggle switching** via navbar for seamless mode changes

### 🎨 User Interface
- **Three-Panel Layout** (25% : 50% : 25%):
  - 🧭 **Left Panel**: Active features, camera preview with flip controls
  - 🌊 **Center Panel**: Animated waveform (listening/processing states), control bar
  - 💬 **Right Panel**: Conversation history with timestamps
- **Custom Navbar** with toggle switches for Language (EN/BN) and API mode (Local/Cloud)
- **Control Bar**: Camera toggle, Power/Exit, Microphone recording
- **Dark Theme**: #0D0D0D background, #4A9EAD accent, based on Figma design

### 📹 Camera & Microphone
- Live webcam preview with WebRTC MediaDevices API
- **Camera Toggle** - Enable/disable video feed
- **Microphone Recording** - 5-second audio capture intervals
- **Horizontal Flip** - Mirror camera view for natural interaction
- **SVG Icons** - Professional Flaticon-style controls

---

## 🚀 Installation

### Prerequisites
- **Rust** 1.93+ (installed automatically via rustup)
- **Node.js** 16+ (for Tauri CLI)
- **Python** 3.10+ (for face auth backend - optional)
- Webcam and microphone access

### Platform-Specific Requirements

#### macOS
```bash
xcode-select --install
```

#### Windows
- Install [Visual Studio C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Or install Visual Studio 2022 with "Desktop development with C++" workload

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file \
  libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev
```

#### Linux (Fedora)
```bash
sudo dnf install webkit2gtk4.1-devel openssl-devel curl wget file \
  libappindicator-gtk3-devel librsvg2-devel
```

#### Linux (Arch)
```bash
sudo pacman -S webkit2gtk-4.1 base-devel curl wget file openssl \
  appmenu-gtk-module gtk3 libappindicator-gtk3 librsvg libvips
```

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/afraz-rupak/maya.git
cd maya/tauri-app
```

2. **Install Rust** (if not already installed)
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

3. **Install dependencies**
```bash
npm install
```

4. **Run MAYA (Development)**
```bash
npm run dev
```

5. **Build Production App**
```bash
npm run build
```

This creates platform-specific installers:
- **macOS**: `src-tauri/target/release/bundle/macos/MAYA.app` + `.dmg` installer
- **Windows**: `src-tauri/target/release/bundle/msi/MAYA_2.0.0_x64.msi`
- **Linux**: `src-tauri/target/release/bundle/deb/maya_2.0.0_amd64.deb` + `.AppImage`

6. **Launch the App**
```bash
# Development (fast iteration, hot reload)
npm run dev

# Production (optimized, platform-specific)
# macOS:
./src-tauri/target/release/maya
# or: open src-tauri/target/release/bundle/macos/MAYA.app

# Windows:
.\src-tauri\target\release\maya.exe

# Linux:
./src-tauri/target/release/maya
```

---

## 📖 Usage

### Getting Started
1. Launch MAYA from Applications or run the binary
2. **Grant Permissions**: Allow camera and microphone access when prompted
3. The app will open with the three-panel interface

### Camera Controls
- Click the **camera icon** in the control bar to toggle video feed
- Camera feed appears in the left panel with horizontal flip
- Video is disabled by default for privacy

### Voice Recording
1. Click the **🎤 microphone icon** in the center control bar
2. Recording starts for 5-second intervals automatically
3. LED indicator shows recording status
4. Transcription will appear in the conversation panel (future integration)

### Language & API Switching
- **Language Toggle**: Click **EN** / **BN** switch in navbar
- **API Mode**: Click **Local** / **API** switch for Whisper mode
  - Local: Offline processing (privacy-first)
  - API: Cloud-based (faster, requires OpenAI API key)

### Exit the App
- Click the **power icon** in the center control bar
- Or use standard macOS quit (⌘Q)

### Visual States
Watch the center waveform video for UI feedback:
- 🟢 Animated waveform plays when app is active
- Smooth looping animation indicates ready state

---

## 📦 Project Structure

```
maya/
├── tauri-app/                     # 🚀 Active Tauri application
│   ├── src/                       # Frontend (HTML/CSS/JS)
│   │   ├── index.html            # Main UI structure
│   │   ├── styles.css            # Figma-based dark theme
│   │   ├── app.js                # Frontend logic (WebRTC, events)
│   │   └── assets/
│   │       ├── maya_logo.png     # App logo (110KB)
│   │       └── waveform.mp4      # Animated waveform (6.7MB)
│   │
│   ├── src-tauri/                 # Rust backend
│   │   ├── src/
│   │   │   └── main.rs           # Tauri commands (greet, exit_app)
│   │   ├── icons/                # App icons (multi-resolution)
│   │   │   ├── icon.icns         # macOS Dock icon (336KB)
│   │   │   ├── icon.png          # 1024x1024 RGBA
│   │   │   ├── 512x512.png
│   │   │   ├── 128x128.png
│   │   │   └── 32x32.png
│   │   ├── Cargo.toml            # Rust dependencies
│   │   ├── tauri.conf.json       # Tauri v2 configuration
│   │   ├── Info.plist            # macOS permissions
│   │   ├── entitlements.plist    # Camera/Mic entitlements
│   │   └── target/release/
│   │       ├── maya              # Production binary (15MB)
│   │       └── bundle/
│   │           ├── macos/MAYA.app         # App bundle
│   │           └── dmg/MAYA_2.0.0_aarch64.dmg  # Installer
│   │
│   ├── package.json              # Node dependencies
│   ├── setup.sh                  # Automated setup script
│   └── README.md                 # Tauri-specific docs
│
├── frontend/                      # 📁 Frontend assets
│   ├── assets/
│   │   ├── maya_logo.svg         # Vector logo (68KB)
│   │   ├── maya_logo.png         # Raster logo (110KB)
│   │   └── videos/
│   │       └── waveform_loop.mp4 # Source video
│   └── README.md
│
├── maya/                          # 🐍 Original PyQt6 app (legacy)
│   ├── __init__.py
│   └── main.py
│
├── scripts/                       # 🛠️ Setup scripts
│   ├── setup_pin.py              # PIN setup utility
│   └── test_installation.sh      # Dependency checker
│
├── LICENSE                        # MIT License
├── Makefile                       # Build automation
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🛠️ Technology Stack

### Tauri Application (Current)
| Component | Technology | Version | Platform |
|-----------|-----------|---------|----------|
| Framework | Tauri | 2.0 | macOS, Windows, Linux |
| Backend | Rust | 1.93.0 | Cross-platform |
| Frontend | HTML5/CSS3/JavaScript | ES6 | Cross-platform |
| Camera/Mic | WebRTC MediaDevices API | - | All platforms |
| Build System | Cargo + npm | - | Cross-platform |
| Video | HTML5 Video (MP4) | - | All platforms |
| Icons | .icns (macOS), .ico (Windows), .png (Linux) | - | Platform-specific |

### Platform Support
| Platform | Minimum Version | Installer Format | Binary Size |
|----------|----------------|------------------|-------------|
| macOS | 10.13+ (High Sierra) | .dmg, .app | ~15MB |
| Windows | Windows 7+ | .msi, .exe (NSIS) | ~15MB |
| Linux | Ubuntu 20.04+, Fedora 36+, Arch | .deb, .AppImage | ~15MB |

### Legacy PyQt6 Application
| Component | Technology | Version |
|-----------|-----------|---------|
| GUI Framework | PyQt6 | 6.10.2 |
| Face Recognition | OpenCV SFace | 4.13.0 |
| Speech Recognition | OpenAI Whisper | 20250625 |
| Computer Vision | OpenCV | 4.13.0 |

---

## 🏗️ Architecture

### Current: Tauri Native App (Cross-Platform)
```
┌─────────────────────────────────────────┐
│  Native Application                     │
│  (Windows/macOS/Linux)                  │
├─────────────────────────────────────────┤
│  Tauri WebView (HTML/CSS/JS)            │
│  ├─ index.html (3-panel layout)         │
│  ├─ styles.css (dark theme)             │
│  └─ app.js (event handlers, WebRTC)     │
├─────────────────────────────────────────┤
│  Rust Backend (Tauri Core)              │
│  ├─ greet() command                     │
│  └─ exit_app() command                  │
├─────────────────────────────────────────┤
│  Platform-Specific APIs                 │
│  ├─ Windows: Win32, WebView2            │
│  ├─ macOS: Cocoa, WKWebView              │
│  └─ Linux: GTK, WebKitGTK                │
└─────────────────────────────────────────┘
```

### Build Output (Platform-Specific)
| Platform | Artifacts |
|----------|-----------|
| **macOS** | `MAYA.app` (app bundle), `MAYA_2.0.0_aarch64.dmg` (installer) |
| **Windows** | `MAYA_2.0.0_x64.msi` (MSI installer), `MAYA_2.0.0_x64-setup.exe` (NSIS) |
| **Linux** | `maya_2.0.0_amd64.deb` (Debian), `maya_2.0.0_amd64.AppImage` (portable) |

- **Development**: `npm run dev` → Hot reload, fast iteration (all platforms)
- **Production**: `npm run build` → Optimized binary + platform installer

---

## 📅 Development Log

### **February 3, 2026** - Cross-Platform Support Added
- ✅ Configured Tauri for Windows and Linux builds
- ✅ Created Windows .ico icon (multi-resolution: 256, 128, 64, 48, 32, 16)
- ✅ Added platform-specific build targets (dmg, msi, nsis, deb, appimage)
- ✅ Configured Windows WebView2 installer settings
- ✅ Added Linux GTK and WebKit dependencies
- ✅ Updated README with cross-platform installation instructions
- ✅ Added platform-specific prerequisites for Ubuntu, Fedora, Arch, Windows
- ✅ Documented build output locations for all platforms
- ✅ Updated architecture diagram to show Windows/macOS/Linux support

### **February 2, 2026** - Tauri v2 Migration Complete (macOS)
- ✅ Migrated from PyQt6 to Tauri v2 for native macOS app
- ✅ Installed Rust 1.93.0 and Cargo toolchain
- ✅ Created Tauri project with React-like frontend structure
- ✅ Fixed Tauri v2 configuration schema and permissions
- ✅ Ported HTML/CSS/JS from web version (identical Figma design)
- ✅ Integrated waveform video (6.7MB MP4)
- ✅ Created custom app icons from logo (multi-resolution PNG + .icns)
- ✅ Fixed exit button with Rust `exit_app()` command
- ✅ Debugged microphone and button interactivity (z-index, pointer-events)
- ✅ Built production binary (15MB, optimized)
- ✅ Added GPU acceleration for video rendering
- ✅ Fixed camera orientation (horizontal flip, no rotation)
- ✅ Updated navbar with custom MAYA logo
- ✅ Created .app bundle with proper Dock icon integration
- ✅ Configured camera/microphone permissions (Info.plist, entitlements.plist)
- ✅ Generated .dmg installer for distribution
- ✅ Cleaned up project (removed web/, docs, build artifacts)

### **January 22, 2026** - Face Authentication System (PyQt6)
- ✅ Implemented biometric face authentication on app launch
- ✅ Created face enrollment screen with 5-step capture process
- ✅ Integrated OpenCV SFace (lightweight FaceNet) for recognition
- ✅ Added YuNet face detector (ONNX, ~20 FPS on CPU)
- ✅ Built secure storage with AES-128 encryption for embeddings
- ✅ Implemented PBKDF2-HMAC-SHA256 for PIN hashing

### **January 20, 2026** - UI Refinement & Voice Recognition (PyQt6)
- ✅ Created custom navbar with animated toggle switches
- ✅ Implemented OpenAI Whisper for speech-to-text
- ✅ Added English and Bangla language support
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

### Current (Tauri v2 App)
- [x] Native macOS application with Tauri v2
- [x] WebRTC camera and microphone access
- [x] Custom Dock icon and .app bundle
- [x] Three-panel dark theme UI (Figma-based)
- [x] Waveform animation with GPU acceleration
- [x] Language and API mode toggles
- [x] Production-ready binary and DMG installer

### Next Steps
- [ ] **Backend Integration**: Connect Python Whisper API to Tauri frontend
- [ ] **Face Authentication**: Port face recognition to Tauri/Rust
- [ ] **Voice Processing**: Implement actual speech-to-text with Whisper
- [ ] **AI Responses**: Add conversational AI (GPT/Claude integration)
- [ ] **Conversation History**: Persistent chat storage with SQLite
- [ ] **Settings Panel**: User preferences (theme, shortcuts, models)

### Future Features
- [ ] Wake word detection ("Hey MAYA")
- [ ] Continuous listening mode
- [ ] Voice activity detection (auto-stop recording)
- [ ] Text-to-speech (TTS) for AI responses
- [ ] Context-aware conversation memory
- [ ] Plugin system for custom AI models
- [ ] Multi-language support (Hindi, Urdu, Arabic)
- [ ] Screen capture and annotation tools
- [ ] Cross-platform support (Windows, Linux)
- [ ] Cloud sync for conversation history
- [ ] Code signing and notarization for distribution

### Legacy Features (PyQt6 Version)
- [x] Face authentication on launch
- [x] Encrypted face embeddings storage (AES-128)
- [x] Backup PIN system with PBKDF2
- [x] OpenCV SFace integration
- [x] YuNet face detector

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

## 🙏 Acknowledgments

- **Tauri Team** - For the amazing native app framework
- **OpenAI** - For Whisper speech recognition model
- **Figma Community** - UI design inspiration
- **Flaticon** - SVG icons for controls
- **Rust Community** - For excellent tooling and documentation

---

## 📧 Contact

**Afraz Rupak**
- GitHub: [@afraz-rupak](https://github.com/afraz-rupak)
- Repository: [github.com/afraz-rupak/maya](https://github.com/afraz-rupak/maya)

---

<div align="center">

**Made with ❤️ using Tauri, Rust, and modern web technologies**

</div>

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

