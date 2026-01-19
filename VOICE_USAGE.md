# MAYA Voice Recognition Usage Guide

## Overview
MAYA now includes speech-to-text functionality powered by OpenAI Whisper with support for **English** and **Bangla** languages.

## Features
✅ **Local Speech Recognition** - Works offline using Whisper
✅ **Multi-language Support** - English and Bangla (বাংলা)
✅ **Real-time Visual Feedback** - Waveform shows listening state
✅ **Easy Language Switching** - Dropdown selector in chat panel

## How to Use

### 1. Start the Application
```bash
cd /Volumes/afraz_SSD/maya
source maya_env/bin/activate
python frontend/main.py
```

### 2. Change Language
- Use the **language dropdown** in the top-right of the conversation panel
- Options: "English" or "বাংলা (Bangla)"
- Language is saved for all voice inputs

### 3. Voice Input Methods

#### Method A: Voice Button (Recommended)
1. Click the **🎤 Voice** button in the conversation panel
2. Speak for 5 seconds
3. Wait for transcription to appear

#### Method B: Text Commands
Type one of these commands:
- `listen` or `voice` - Start voice listening
- `english` or `en` - Switch to English
- `bangla` or `বাংলা` or `bn` - Switch to Bangla

### 4. Visual Feedback
Watch the center panel waveform:
- **Ready** (Gray) - Idle, ready to listen
- **● Listening...** (Green) - Recording audio
- **⟳ Processing...** (Orange) - Transcribing speech
- **♪ Speaking...** (Blue) - AI responding

## Technical Details

### Whisper Model
- **Model Size**: Base (default)
- **Accuracy**: High for both English and Bangla
- **Loading Time**: ~5-10 seconds on first launch
- **Recording Duration**: 5 seconds per voice input

### Supported Languages
| Language | Code | Whisper Support |
|----------|------|----------------|
| English  | `en` | ✅ Native      |
| Bangla   | `bn` | ✅ Native      |

### Dependencies
```txt
openai-whisper>=20250625  # Speech recognition
sounddevice>=0.5.0        # Audio capture
torch>=2.9.0              # ML framework
PyQt6>=6.10.0             # GUI
```

## Troubleshooting

### "Model not loaded" Error
- Wait 5-10 seconds after app launch for Whisper model to load
- Check terminal for "Model loaded successfully!" message

### No Audio Captured
- **macOS**: Grant microphone permissions in System Settings > Privacy & Security > Microphone
- Check that your microphone is working in other apps
- Verify microphone isn't muted

### Poor Transcription
- Speak clearly and at normal volume
- Reduce background noise
- Ensure correct language is selected
- For better accuracy, upgrade to larger model:
  ```python
  # In frontend/main.py, line ~40
  self.voice_listener = VoiceListener(model_size="small", language="en")
  # Options: tiny, base, small, medium, large
  ```

### Bangla Not Recognized
- Ensure language is set to "বাংলা (Bangla)" in dropdown
- Whisper has excellent Bangla support, but may require clear pronunciation
- Try speaking common phrases first to test

## Customization

### Change Recording Duration
In `frontend/main.py`:
```python
def start_voice_listening(self, duration=10):  # Change to 10 seconds
    ...
```

### Change Whisper Model Size
In `frontend/main.py`:
```python
# Line ~40
self.voice_listener = VoiceListener(
    model_size="small",  # Options: tiny, base, small, medium, large
    language="en"
)
```

Model sizes:
- **tiny**: Fastest, lower accuracy (~1GB VRAM)
- **base**: Good balance (default) (~1GB VRAM)
- **small**: Better accuracy (~2GB VRAM)
- **medium**: High accuracy (~5GB VRAM)
- **large**: Best accuracy (~10GB VRAM)

## Tips for Best Results

1. **Wait for model load**: Don't use voice immediately after launch
2. **Speak naturally**: Normal pace and volume work best
3. **Reduce noise**: Close windows, turn off fans
4. **Test connection**: Try "Hello MAYA" or "আসসালামু আলাইকুম" first
5. **Right language**: Make sure dropdown matches your speech language

## Next Steps
- [ ] Add wake word detection ("Hey MAYA")
- [ ] Continuous listening mode
- [ ] Voice activity detection (automatic stop)
- [ ] Custom vocabulary support
- [ ] More languages (Hindi, Urdu, etc.)
