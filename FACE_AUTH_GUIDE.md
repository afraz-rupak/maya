# Face Authentication Setup Guide

## Overview

MAYA features biometric face authentication that securely verifies your identity when launching the application. This guide covers setup, usage, and troubleshooting.

---

## 🎯 Features

- **Secure Biometric Login**: Face recognition using OpenCV SFace model
- **Encrypted Storage**: Face embeddings stored encrypted on your device
- **Backup PIN**: Fallback authentication method
- **First-time Enrollment**: Easy 5-step face capture process
- **Anti-spoofing**: Live face detection prevents photo attacks
- **Privacy-first**: All data stored locally, never uploaded

---

## 🚀 First-time Setup

### 1. Launch MAYA

```bash
python -m maya.main
```

On first launch, you'll see the **Face Enrollment Screen**.

### 2. Enter Your Name

- Type your name (e.g., "Afraz")
- Click **Start Enrollment**

### 3. Capture Your Face

You'll be prompted to capture 5 images:

1. **Front view** - Look straight at camera
2. **Left tilt** - Tilt head slightly left
3. **Right tilt** - Tilt head slightly right  
4. **Looking up** - Tilt head slightly up
5. **Smile** - Front view with smile

**Tips:**
- Ensure good lighting
- Position face inside the blue detection box
- Wait for "Face Detected" confirmation before capturing
- Keep 1-2 feet distance from camera

### 4. Set Backup PIN

After face enrollment, you'll be prompted to set a 4-digit backup PIN.

```bash
# Or set PIN manually:
python scripts/setup_pin.py
```

### 5. Done!

Your face authentication is now active. Next time you launch MAYA, it will automatically recognize you.

---

## 🔐 Daily Usage

### Normal Login

1. Launch MAYA
2. Position your face in the circular preview
3. Wait for recognition (3 consecutive matches required)
4. Welcome message appears
5. Main interface loads

**Success indicators:**
- Green checkmark animation
- "Welcome back, [Your Name]!"

### Using PIN Backup

If face recognition fails or you prefer PIN:

1. Click **"Use PIN Instead"** button
2. Enter your 4-digit PIN
3. Press Enter or click **Submit**

---

## ⚙️ Configuration

### Face Authentication Settings

Edit configuration:
```bash
~/.maya/secure/config.json
```

```json
{
  "enabled": true,
  "similarity_threshold": 0.6,
  "consecutive_matches_required": 3,
  "timeout_seconds": 30,
  "max_attempts": 5,
  "fallback_to_pin": true,
  "owner_name": "Afraz"
}
```

**Parameters:**

- `similarity_threshold` (0.0-1.0): Face match confidence (default: 0.6)
- `consecutive_matches_required`: Matches needed for authentication (default: 3)
- `timeout_seconds`: Auto-timeout for face scan (default: 30)
- `max_attempts`: Max failed attempts before lockout (default: 5)
- `fallback_to_pin`: Allow PIN backup (default: true)

### Skip Authentication (Development)

```bash
python -m maya.main --skip-auth
```

---

## 🔧 Managing Your Data

### Change PIN

```bash
python scripts/setup_pin.py
```

### Remove PIN

```bash
python scripts/setup_pin.py remove
```

### Re-enroll Face

Delete existing face data and restart MAYA:

```bash
rm ~/.maya/secure/embeddings.enc
python -m maya.main
```

### Delete All Auth Data

```bash
rm -rf ~/.maya/secure/
```

**Warning:** This removes all face and PIN data. You'll need to re-enroll.

---

## 📂 Data Storage

All authentication data is stored locally:

```
~/.maya/secure/
├── .key                    # Encryption key (600 permissions)
├── embeddings.enc          # Encrypted face embeddings
├── pin.json               # Hashed PIN with salt
└── config.json            # Authentication settings
```

**Security:**
- Face embeddings encrypted with Fernet (AES-128)
- PIN hashed with PBKDF2-HMAC-SHA256 (100,000 iterations)
- Files have owner-only permissions (chmod 600)
- No raw images stored

---

## 🐛 Troubleshooting

### Face Not Detected

**Symptoms:** Blue detection box doesn't appear

**Solutions:**
- Improve lighting (front-facing light recommended)
- Adjust camera angle
- Move closer/farther from camera (1-2 feet optimal)
- Clean camera lens
- Check camera permissions

### Face Not Recognized

**Symptoms:** Red X animation, "Face Not Recognized"

**Solutions:**
- Ensure good lighting (same as enrollment)
- Look straight at camera
- Remove glasses/hat if not worn during enrollment
- Try different distance
- Re-enroll if consistently failing

### Camera Not Working

**Error:** "Camera could not be initialized"

**Solutions:**

1. Check camera permissions:
   ```bash
   # macOS - System Preferences > Security & Privacy > Camera
   ```

2. Close other apps using camera (Zoom, FaceTime, etc.)

3. Test camera:
   ```bash
   python -c "import cv2; print(cv2.VideoCapture(0).read())"
   ```

4. Restart MAYA

### PIN Not Accepting

**Error:** "Incorrect PIN"

**Solutions:**
- Verify you entered correct 4-digit PIN
- Reset PIN using `python scripts/setup_pin.py`
- If forgotten, delete `~/.maya/secure/pin.json` and use face auth

### Models Not Downloading

**Error:** "Failed to download YuNet" or "Failed to download SFace"

**Solutions:**

1. Check internet connection
2. Manual download:
   ```bash
   mkdir -p frontend/models
   cd frontend/models
   
   # YuNet detector
   wget https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx
   
   # SFace recognizer
   wget https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx
   ```

### Locked Out (Max Attempts)

**Message:** "Maximum attempts reached. Please wait 5 minutes."

**Solutions:**
- Wait 5 minutes for automatic unlock
- Use PIN backup (if enabled)
- Restart MAYA to reset counter (development only)

---

## 🔬 Technical Details

### Face Detection
- **Model**: YuNet (ONNX)
- **Speed**: ~20 FPS on CPU
- **Accuracy**: 95%+ on WIDER FACE dataset

### Face Recognition
- **Model**: SFace (lightweight FaceNet variant)
- **Embedding**: 128-dimensional vector
- **Comparison**: Cosine similarity
- **Threshold**: 0.6 (adjustable)

### Enrollment Process
1. Capture 5 frames from different angles
2. Detect face in each frame (YuNet)
3. Extract 128-dim embeddings (SFace)
4. Average embeddings for robustness
5. Encrypt and store locally

### Authentication Process
1. Capture live frames at 20 FPS
2. Detect face (YuNet)
3. Extract embedding (SFace)
4. Compare with stored embedding (cosine similarity)
5. Require 3 consecutive matches > 0.6 threshold
6. Grant access on success

---

## 🛡️ Security Considerations

### What's Stored
- ✅ 128-dimensional face embedding (encrypted)
- ✅ Hashed PIN with unique salt
- ✅ Configuration settings
- ❌ **NO raw face images**
- ❌ **NO passwords or sensitive data**

### Encryption
- **Face Embeddings**: AES-128 via Fernet
- **PIN**: PBKDF2-HMAC-SHA256 with 100K iterations
- **Key Storage**: Local `.key` file with 600 permissions

### Attack Resistance
- **Photo Attack**: Live detection prevents printed photos
- **Video Attack**: (Optional) Anti-spoofing detects screens
- **Brute Force**: PIN lockout after 5 attempts
- **Data Theft**: Embeddings useless without encryption key

### Privacy
- All processing happens **locally on your device**
- No cloud upload or API calls
- No telemetry or tracking
- Open source code for auditing

---

## ❓ FAQ

**Q: Can someone unlock MAYA with my photo?**  
A: No, basic live detection is built-in. For higher security, enable `anti_spoofing` in config.

**Q: What if I change my appearance?**  
A: Minor changes (haircut, beard) are fine. Major changes (glasses, significant weight) may require re-enrollment.

**Q: Is my face data safe?**  
A: Yes, embeddings are encrypted and never leave your device. Even if stolen, they're useless without the encryption key.

**Q: Can I have multiple users?**  
A: Currently, MAYA supports one registered face. Multi-user support is planned for future releases.

**Q: Does this work offline?**  
A: Yes, completely offline. All models and data are local.

**Q: Can I disable face authentication?**  
A: Yes, use `--skip-auth` flag or set `"enabled": false` in config.

---

## 📞 Support

If you encounter issues:

1. Check this troubleshooting guide
2. Review logs: `~/.maya/logs/`
3. Open GitHub issue: [maya/issues](https://github.com/afraz-rupak/maya/issues)
4. Email: [your-email]

---

## 🔮 Roadmap

- [ ] Multi-user support
- [ ] Advanced anti-spoofing (liveness detection)
- [ ] Face recognition improvements (age/appearance changes)
- [ ] Biometric settings UI
- [ ] Two-factor authentication
- [ ] Face unlock for specific projects/files

---

*Last updated: January 22, 2026*
