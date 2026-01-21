# MAYA Face Authentication - System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        MAYA APPLICATION LAUNCH                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │  Check Embeddings Exist?  │
                    └───────────┬───────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
                ▼ NO                            ▼ YES
    ┌───────────────────┐           ┌────────────────────┐
    │ ENROLLMENT SCREEN │           │   AUTH SCREEN      │
    └───────────────────┘           └────────────────────┘
                │                               │
                │                               │
    ┌───────────▼───────────┐       ┌───────────▼──────────┐
    │  1. Enter Name        │       │  1. Start Camera     │
    │  2. Capture 5 Images  │       │  2. Detect Face      │
    │  3. Extract Embeddings│       │  3. Extract Embedding│
    │  4. Encrypt & Save    │       │  4. Compare Similarity│
    │  5. Set PIN (optional)│       │  5. Check Threshold  │
    └───────────┬───────────┘       └───────────┬──────────┘
                │                               │
                │                               │
                └───────────┬───────────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │  3 Consecutive        │
                │  Matches (>0.6)?      │
                └───────┬───────────────┘
                        │
            ┌───────────┴───────────┐
            │                       │
            ▼ YES                   ▼ NO
    ┌───────────────┐       ┌──────────────┐
    │ SUCCESS       │       │ FAILURE      │
    │ Green ✓       │       │ Red ✗        │
    └───────┬───────┘       └──────┬───────┘
            │                       │
            │                       ▼
            │               ┌───────────────┐
            │               │ Access Denied │
            │               │ - Retry       │
            │               │ - Use PIN     │
            │               └──────┬────────┘
            │                       │
            │                       ▼
            │               ┌───────────────┐
            │               │ PIN Entry     │
            │               │ PBKDF2 Verify │
            │               └──────┬────────┘
            │                       │
            └───────────────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   MAIN MAYA UI        │
                │                       │
                │  ┌─────────────────┐  │
                │  │ Left Panel      │  │
                │  │ - Projects      │  │
                │  │ - Camera Feed   │  │
                │  └─────────────────┘  │
                │                       │
                │  ┌─────────────────┐  │
                │  │ Center Panel    │  │
                │  │ - Waveform      │  │
                │  │ - AI States     │  │
                │  └─────────────────┘  │
                │                       │
                │  ┌─────────────────┐  │
                │  │ Right Panel     │  │
                │  │ - Chat          │  │
                │  │ - Voice Input   │  │
                │  └─────────────────┘  │
                └───────────────────────┘
```

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FACE RECOGNITION PIPELINE                 │
└─────────────────────────────────────────────────────────────┘

    Camera Frame (BGR)
         │
         ▼
    ┌─────────────────┐
    │   cv2.flip()    │  Flip horizontally
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │   YuNet         │  Face Detection
    │   Detector      │  (320x320 ONNX)
    └────────┬────────┘
             │
             ▼ (x, y, w, h)
    ┌─────────────────┐
    │   Crop Face     │  Extract face region
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │   cv2.resize()  │  Resize to 112x112
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │   SFace Model   │  Face Recognition
    │   (FaceNet-128) │  (ONNX)
    └────────┬────────┘
             │
             ▼ 128-dim vector
    ┌─────────────────┐
    │   Normalize     │  L2 normalization
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Cosine Similarity│  Compare with stored
    │ = dot(v1, v2)   │  embedding
    └────────┬────────┘
             │
             ▼ similarity score
    ┌─────────────────┐
    │ Threshold Check │  > 0.6 ?
    │ (configurable)  │
    └────────┬────────┘
             │
             ▼
        MATCH / NO MATCH
```

---

## Secure Storage Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    SECURE DATA STORAGE                        │
└──────────────────────────────────────────────────────────────┘

    ~/.maya/secure/
         │
         ├── .key (600)
         │    └─> Fernet Encryption Key (AES-128)
         │
         ├── embeddings.enc (600)
         │    │
         │    └─> {name: embedding} dict
         │         │
         │         ▼
         │    pickle.dumps()
         │         │
         │         ▼
         │    Fernet.encrypt()
         │         │
         │         ▼
         │    Encrypted bytes
         │
         ├── pin.json (600)
         │    │
         │    └─> {
         │          "salt": hex(random_bytes(32)),
         │          "hash": hex(pbkdf2_hmac(
         │                     'sha256',
         │                     pin,
         │                     salt,
         │                     100000
         │                  ))
         │        }
         │
         └── config.json (600)
              │
              └─> {
                    "enabled": true,
                    "similarity_threshold": 0.6,
                    "consecutive_matches_required": 3,
                    "timeout_seconds": 30,
                    "max_attempts": 5,
                    "owner_name": "Afraz"
                  }
```

---

## Authentication State Machine

```
┌─────────────────────────────────────────────────────────┐
│               AUTHENTICATION STATES                      │
└─────────────────────────────────────────────────────────┘

    START
      │
      ▼
   ┌──────────┐
   │  IDLE    │──────────────────┐
   └────┬─────┘                  │
        │                        │
        │ start_authentication() │
        ▼                        │
   ┌──────────┐                  │
   │ SCANNING │                  │ timeout
   └────┬─────┘                  │ (30s)
        │                        │
        │ face detected          │
        ▼                        │
   ┌──────────┐                  │
   │ MATCHING │                  │
   └────┬─────┘                  │
        │                        │
        ├─ match_count < 3 ──────┤
        │                        │
        ├─ match_count >= 3      │
        │    (SUCCESS)            │
        ▼                        │
   ┌──────────┐                  │
   │ SUCCESS  │                  │
   │ (✓)      │                  │
   └────┬─────┘                  │
        │                        │
        │ 1.5s delay             │
        ▼                        │
   ┌──────────┐                  │
   │ GRANTED  │                  │
   └──────────┘                  │
                                 │
   ┌──────────┐                  │
   │ FAILURE  │◄─────────────────┘
   │ (✗)      │
   └────┬─────┘
        │
        ├─ attempts < 5
        │    (RETRY)
        │
        └─ attempts >= 5
             (LOCKED - 5 min)
```

---

## Component Interaction Diagram

```
┌────────────────────────────────────────────────────────────┐
│                  MAYA APPLICATION                          │
└────────────────────────────────────────────────────────────┘
        │
        ├── MAYAMainWindow (QMainWindow)
        │       │
        │       ├── QStackedWidget
        │       │    │
        │       │    ├─► FaceEnrollmentScreen
        │       │    │       │
        │       │    │       ├── Camera (cv2.VideoCapture)
        │       │    │       ├── Preview (640x480)
        │       │    │       └── Signal: enrollment_complete
        │       │    │
        │       │    ├─► FaceAuthScreen
        │       │    │       │
        │       │    │       ├── CircularCameraWidget
        │       │    │       │      └── QPropertyAnimation
        │       │    │       │
        │       │    │       ├── Auth Screen (scanning)
        │       │    │       ├── Denied Screen (retry/PIN)
        │       │    │       ├── PIN Screen (4-digit)
        │       │    │       │
        │       │    │       └── Signals:
        │       │    │              - auth_success
        │       │    │              - auth_failed
        │       │    │
        │       │    └─► MainInterface
        │       │            │
        │       │            ├── NavBar
        │       │            ├── LeftPanel
        │       │            ├── CenterPanel
        │       │            └── RightPanel
        │       │
        │       ├── FaceRecognizer
        │       │       │
        │       │       ├── YuNet Detector
        │       │       │      └── detect_face()
        │       │       │
        │       │       ├── SFace Model
        │       │       │      └── extract_embedding()
        │       │       │
        │       │       ├── compare_embeddings()
        │       │       └── recognize()
        │       │
        │       └── SecureStorage
        │               │
        │               ├── save_embeddings()
        │               ├── load_embeddings()
        │               ├── save_pin()
        │               ├── verify_pin()
        │               └── Fernet encryption
        │
        └── Signals & Slots
                │
                ├── enrollment_complete → on_enrollment_complete()
                ├── auth_success → on_auth_success()
                └── auth_failed → close()
```

---

## Security Model

```
┌──────────────────────────────────────────────────────────┐
│                   SECURITY LAYERS                         │
└──────────────────────────────────────────────────────────┘

Layer 1: Physical Security
    └─> Camera required for authentication
    └─> Live detection (not photos)

Layer 2: Data Encryption
    └─> Face embeddings encrypted with Fernet (AES-128)
    └─> Unique key per installation
    └─> Key stored with 600 permissions

Layer 3: PIN Security
    └─> PBKDF2-HMAC-SHA256 (100K iterations)
    └─> Unique salt per PIN
    └─> Never stored plaintext

Layer 4: Access Control
    └─> File permissions: chmod 600
    └─> Owner-only access
    └─> No network transmission

Layer 5: Rate Limiting
    └─> Max 5 failed attempts
    └─> 5-minute lockout
    └─> Timeout after 30 seconds

Layer 6: Anti-spoofing
    └─> Live face detection
    └─> Consecutive match requirement (3)
    └─> No raw images stored
```

---

## Performance Profile

```
┌──────────────────────────────────────────────────────────┐
│                  PERFORMANCE METRICS                      │
└──────────────────────────────────────────────────────────┘

Enrollment Process:
    ┌─────────────────────────────┐
    │ Step 1: Initialize camera   │  ~0.5s
    │ Step 2: Detect face         │  ~0.05s per frame
    │ Step 3: Capture 5 images    │  ~30-45s (user time)
    │ Step 4: Extract embeddings  │  ~0.2s per image
    │ Step 5: Encrypt & save      │  ~0.1s
    └─────────────────────────────┘
    Total: ~31-46 seconds

Authentication Process:
    ┌─────────────────────────────┐
    │ Step 1: Initialize camera   │  ~0.5s
    │ Step 2: Process frames (20) │  ~0.05s per frame
    │ Step 3: 3 consecutive match │  ~2-3s (typical)
    │ Step 4: Animation & transit │  ~1.5s
    └─────────────────────────────┘
    Total: ~4-5 seconds

Model Loading (one-time):
    ┌─────────────────────────────┐
    │ YuNet download              │  ~2-3s (264 KB)
    │ SFace download              │  ~30-40s (35 MB)
    │ Model initialization        │  ~0.5s
    └─────────────────────────────┘
    Total: ~33-44 seconds (first run only)

Memory Usage:
    ┌─────────────────────────────┐
    │ Base app                    │  ~150 MB
    │ YuNet detector              │  ~10 MB
    │ SFace model                 │  ~40 MB
    │ Camera frames               │  ~5 MB
    └─────────────────────────────┘
    Peak: ~205 MB
```

---

*Architecture documentation for MAYA Face Authentication System*
