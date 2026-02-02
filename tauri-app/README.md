# MAYA Tauri Desktop App

A modern desktop application for MAYA AI Assistant built with Tauri v2, combining web technologies with native performance.

## 🚀 Features

- **Native Desktop App**: Runs as a native application on macOS, Windows, and Linux
- **Lightweight**: Much smaller than Electron (~3MB vs 100MB+)
- **Fast**: Rust backend provides native performance
- **Secure**: Tauri's security model protects against common vulnerabilities
- **Same Beautiful UI**: Identical Figma design as web and PyQt6 versions
- **Python Backend**: Integrated FastAPI backend with Whisper AI
- **WebRTC**: Browser APIs for camera and microphone access
- **Cross-Platform**: Single codebase for all platforms

## 📋 Prerequisites

1. **Rust** (latest stable)
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

2. **Node.js** (v16 or later)
   ```bash
   brew install node  # macOS
   ```

3. **Python 3.8+** with MAYA dependencies
   ```bash
   cd /path/to/maya
   source maya_env/bin/activate
   pip install fastapi uvicorn websockets soundfile openai-whisper
   ```

4. **System Dependencies** (macOS)
   ```bash
   xcode-select --install
   ```

## 🛠️ Installation

### 1. Install Tauri CLI

```bash
cd tauri-app
npm install
```

### 2. Install Rust Dependencies

```bash
cd src-tauri
cargo fetch
```

## 🏃 Running in Development

```bash
cd tauri-app
npm run dev
```

This will:
- Start the Python FastAPI backend automatically
- Launch the Tauri development window
- Enable hot-reload for frontend changes

## 📦 Building for Production

### Build for your platform:

```bash
cd tauri-app
npm run build
```

The built application will be in `src-tauri/target/release/bundle/`:
- **macOS**: `.app` and `.dmg` files
- **Windows**: `.exe` and `.msi` installers
- **Linux**: `.deb`, `.AppImage` files

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│     Tauri Native Window (Rust)      │
│  ┌───────────────────────────────┐  │
│  │   WebView (HTML/CSS/JS)       │  │
│  │   - Same UI as web version    │  │
│  │   - WebRTC camera/mic         │  │
│  │   - Tauri invoke() calls      │  │
│  └───────────────────────────────┘  │
│              │                       │
│      Tauri Commands (Rust)          │
│              │                       │
└──────────────┼───────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Python Backend      │
    │  - FastAPI server    │
    │  - Whisper AI        │
    │  - Voice processing  │
    └──────────────────────┘
```

## 🔧 Project Structure

```
tauri-app/
├── src/                    # Frontend (HTML/CSS/JS)
│   ├── index.html         # Main UI
│   ├── styles.css         # Figma design styles
│   └── app.js             # Tauri-integrated JavaScript
├── src-tauri/             # Rust backend
│   ├── src/
│   │   └── main.rs        # Tauri commands & Python integration
│   ├── Cargo.toml         # Rust dependencies
│   ├── tauri.conf.json    # Tauri configuration
│   └── capabilities/
│       └── default.json   # App permissions
└── package.json           # Node.js config
```

## 🎯 Tauri Commands

The Rust backend provides these commands callable from JavaScript:

- `start_python_backend()` - Launches the FastAPI server
- `stop_python_backend()` - Stops the Python backend
- `transcribe_audio(audioData)` - Sends audio to Whisper for transcription
- `send_message(message)` - Sends message to AI backend

### Usage in JavaScript:

```javascript
const { invoke } = window.__TAURI__.core;

// Start backend
await invoke('start_python_backend');

// Transcribe audio
const text = await invoke('transcribe_audio', { audioData: [...] });

// Send message
const response = await invoke('send_message', { message: "Hello" });
```

## 🔐 Permissions

Camera and microphone permissions are requested at runtime using the browser's WebRTC API. The app uses the same permission model as web browsers.

## ⚡ Performance

- **Bundle Size**: ~3-5 MB (vs Electron's 100+ MB)
- **Memory**: ~50-100 MB RAM (vs Electron's 200+ MB)
- **Startup**: Instant (<1 second)
- **CPU**: Native Rust performance

## 🆚 Comparison with Other Versions

| Feature | PyQt6 | Web (FastAPI) | Tauri |
|---------|-------|---------------|-------|
| Platform | Desktop only | Browser | Desktop (all OS) |
| Size | ~200 MB | N/A | ~5 MB |
| Distribution | Python required | Server required | Standalone .app/.exe |
| Performance | Native | Browser | Native |
| Installation | pip install | None | One-click install |
| Offline | ✅ | ❌ | ✅ |
| Auto-update | ❌ | ✅ | ✅ (with plugin) |

## 🐛 Troubleshooting

### Python backend doesn't start

Check that Python is in your PATH:
```bash
which python3
```

Edit `src-tauri/src/main.rs` and update the Python command path if needed.

### Rust compilation errors

Update Rust to the latest version:
```bash
rustup update stable
```

### WebRTC not working

Grant camera/microphone permissions in System Preferences (macOS) or Settings (Windows/Linux).

## 📝 Development Tips

1. **Hot Reload**: Changes to HTML/CSS/JS reload automatically in dev mode
2. **Rust Changes**: Require rebuilding (`cargo build`)
3. **Python Backend**: Must be restarted manually if you change `web/server.py`
4. **Debug Console**: Open DevTools with `Cmd+Option+I` (macOS) in dev mode

## 🚢 Deployment

### macOS Code Signing

```bash
# Sign the app
codesign --deep --force --verify --verbose --sign "Developer ID" Maya.app

# Notarize for distribution
xcrun notarytool submit Maya.dmg --keychain-profile "AC_PASSWORD"
```

### Windows Signing

Use `signtool.exe` with your code signing certificate.

## 🔮 Future Enhancements

- [ ] Auto-update support with `tauri-plugin-updater`
- [ ] System tray icon with `tauri-plugin-tray`
- [ ] Native notifications
- [ ] Keyboard shortcuts
- [ ] Multiple window support
- [ ] Custom window decorations

## 📄 License

Same as main MAYA project

## 🙏 Credits

- Tauri Team for the amazing framework
- MAYA project for the Python backend and AI models
