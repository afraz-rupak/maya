#!/bin/bash
# Test Face Authentication Installation
# This script verifies all components are correctly installed

echo "=========================================="
echo "  MAYA Face Authentication Test"
echo "=========================================="
echo ""

# Check Python version
echo "1. Checking Python version..."
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "   ✓ Python $PYTHON_VERSION"
echo ""

# Check virtual environment
echo "2. Checking virtual environment..."
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "   ✓ Virtual environment active: $VIRTUAL_ENV"
else
    echo "   ⚠ Virtual environment not active"
    echo "   Run: source maya_env/bin/activate"
fi
echo ""

# Check required packages
echo "3. Checking required packages..."

check_package() {
    if python -c "import $1" 2>/dev/null; then
        VERSION=$(python -c "import $1; print($1.__version__)" 2>/dev/null || echo "unknown")
        echo "   ✓ $1 ($VERSION)"
        return 0
    else
        echo "   ✗ $1 - NOT INSTALLED"
        return 1
    fi
}

MISSING=0

check_package "PyQt6" || ((MISSING++))
check_package "cv2" || ((MISSING++))
check_package "numpy" || ((MISSING++))
check_package "cryptography" || ((MISSING++))
check_package "torch" || ((MISSING++))
check_package "whisper" || ((MISSING++))
check_package "sounddevice" || ((MISSING++))

echo ""

if [ $MISSING -gt 0 ]; then
    echo "⚠ $MISSING package(s) missing. Run: pip install -r requirements.txt"
    echo ""
fi

# Check camera availability
echo "4. Checking camera..."
python -c "
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print('   ✓ Camera detected')
    cap.release()
else:
    print('   ✗ Camera not available')
" 2>/dev/null
echo ""

# Check face recognition models
echo "5. Checking face recognition models..."

if [ -f "frontend/models/face_detection_yunet_2023mar.onnx" ]; then
    echo "   ✓ YuNet detector"
else
    echo "   ⚠ YuNet detector will download on first run"
fi

if [ -f "frontend/models/face_recognition_sface_2021dec.onnx" ]; then
    echo "   ✓ SFace recognizer"
else
    echo "   ⚠ SFace recognizer will download on first run"
fi
echo ""

# Check secure storage
echo "6. Checking secure storage..."
if [ -d "$HOME/.maya/secure" ]; then
    echo "   ✓ Secure directory exists: $HOME/.maya/secure"
    
    if [ -f "$HOME/.maya/secure/embeddings.enc" ]; then
        echo "   ✓ Face embeddings enrolled"
        ENROLLED=1
    else
        echo "   ⚠ No face enrolled (first-time setup required)"
        ENROLLED=0
    fi
    
    if [ -f "$HOME/.maya/secure/pin.json" ]; then
        echo "   ✓ PIN configured"
    else
        echo "   ⚠ No PIN set (optional)"
    fi
else
    echo "   ⚠ Secure directory will be created on first run"
    ENROLLED=0
fi
echo ""

# Test face recognition engine
echo "7. Testing face recognition engine..."
python -c "
import sys
sys.path.insert(0, '.')
try:
    from frontend.components.face_recognizer import FaceRecognizer
    recognizer = FaceRecognizer()
    print('   ✓ Face recognizer initialized')
except Exception as e:
    print(f'   ✗ Error: {e}')
" 2>/dev/null
echo ""

# Test secure storage
echo "8. Testing secure storage..."
python -c "
import sys
sys.path.insert(0, '.')
try:
    from frontend.components.secure_storage import SecureStorage
    storage = SecureStorage()
    print('   ✓ Secure storage initialized')
except Exception as e:
    print(f'   ✗ Error: {e}')
" 2>/dev/null
echo ""

# Summary
echo "=========================================="
echo "  Test Summary"
echo "=========================================="

if [ $MISSING -eq 0 ]; then
    echo "✓ All dependencies installed"
else
    echo "⚠ Some dependencies missing"
fi

if [ $ENROLLED -eq 1 ]; then
    echo "✓ Face authentication ready"
    echo ""
    echo "Run: python -m maya.main"
else
    echo "⚠ Face enrollment required"
    echo ""
    echo "Run: python -m maya.main"
    echo "(You'll be guided through face enrollment)"
fi

echo ""
echo "=========================================="
echo ""

# Optional: Quick launch
read -p "Launch MAYA now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Launching MAYA..."
    python -m maya.main
fi
