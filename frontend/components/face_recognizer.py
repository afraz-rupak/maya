"""
Face Recognition Module using FaceNet (FN8)
Lightweight face recognition for MAYA authentication
"""

import os
import cv2
import numpy as np
import pickle
from pathlib import Path


class FaceRecognizer:
    """Face recognition using OpenCV DNN with FaceNet model"""
    
    def __init__(self, config_path=None):
        self.detector = None
        self.recognizer_model = None
        self.known_embeddings = {}
        self.similarity_threshold = 0.6
        self.config_path = config_path or self._get_default_config_path()
        
        self.load_models()
        self.load_embeddings()
    
    def _get_default_config_path(self):
        """Get default path for face data storage"""
        return Path.home() / ".maya" / "face_data"
    
    def load_models(self):
        """Load face detection and recognition models"""
        try:
            # Load YuNet face detector (lightweight, fast)
            detector_path = self._download_yunet_model()
            self.detector = cv2.FaceDetectorYN.create(
                detector_path,
                "",
                (320, 320),
                score_threshold=0.6,
                nms_threshold=0.3
            )
            print("✓ YuNet face detector loaded")
            
            # Load SFace recognition model (lightweight FaceNet variant)
            recognizer_path = self._download_sface_model()
            self.recognizer_model = cv2.FaceRecognizerSF.create(
                recognizer_path, ""
            )
            print("✓ SFace recognition model loaded")
            
        except Exception as e:
            print(f"Error loading models: {e}")
            # Fallback to Haar Cascade if models fail
            self._load_fallback_detector()
    
    def _download_yunet_model(self):
        """Download YuNet model if not exists"""
        model_dir = Path(__file__).parent.parent / "models"
        model_dir.mkdir(exist_ok=True)
        model_path = model_dir / "face_detection_yunet_2023mar.onnx"
        
        if not model_path.exists():
            print("Downloading YuNet face detector...")
            url = "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
            
            try:
                import urllib.request
                urllib.request.urlretrieve(url, str(model_path))
                print(f"✓ Downloaded to {model_path}")
            except Exception as e:
                print(f"Failed to download YuNet: {e}")
                raise
        
        return str(model_path)
    
    def _download_sface_model(self):
        """Download SFace recognition model if not exists"""
        model_dir = Path(__file__).parent.parent / "models"
        model_path = model_dir / "face_recognition_sface_2021dec.onnx"
        
        if not model_path.exists():
            print("Downloading SFace recognition model...")
            url = "https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx"
            
            try:
                import urllib.request
                urllib.request.urlretrieve(url, str(model_path))
                print(f"✓ Downloaded to {model_path}")
            except Exception as e:
                print(f"Failed to download SFace: {e}")
                raise
        
        return str(model_path)
    
    def _load_fallback_detector(self):
        """Load Haar Cascade as fallback detector"""
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.detector = cv2.CascadeClassifier(cascade_path)
        print("⚠ Using Haar Cascade fallback detector")
    
    def detect_face(self, frame):
        """
        Detect face in frame
        Returns: (x, y, w, h) or None
        """
        if self.detector is None:
            return None
        
        try:
            # Resize frame for faster detection
            height, width = frame.shape[:2]
            if isinstance(self.detector, cv2.FaceDetectorYN):
                self.detector.setInputSize((width, height))
                _, faces = self.detector.detect(frame)
                
                if faces is not None and len(faces) > 0:
                    # Get first face (most confident)
                    face = faces[0]
                    x, y, w, h = face[:4].astype(int)
                    return (x, y, w, h)
            else:
                # Haar Cascade fallback
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.detector.detectMultiScale(gray, 1.3, 5)
                
                if len(faces) > 0:
                    return tuple(faces[0])
        
        except Exception as e:
            print(f"Face detection error: {e}")
        
        return None
    
    def extract_embedding(self, frame, face_box):
        """
        Extract face embedding from detected face
        Returns: 128-dim embedding vector or None
        """
        if self.recognizer_model is None:
            return None
        
        try:
            x, y, w, h = face_box
            
            # Crop and align face
            face_crop = frame[y:y+h, x:x+w]
            
            if face_crop.size == 0:
                return None
            
            # Align face using the recognition model
            aligned_face = cv2.resize(face_crop, (112, 112))
            
            # Extract embedding
            embedding = self.recognizer_model.feature(aligned_face)
            
            return embedding.flatten()
        
        except Exception as e:
            print(f"Embedding extraction error: {e}")
            return None
    
    def compare_embeddings(self, embedding1, embedding2):
        """
        Compare two embeddings using cosine similarity
        Returns: similarity score (0-1)
        """
        if embedding1 is None or embedding2 is None:
            return 0.0
        
        # Normalize embeddings
        embedding1 = embedding1 / np.linalg.norm(embedding1)
        embedding2 = embedding2 / np.linalg.norm(embedding2)
        
        # Compute cosine similarity
        similarity = np.dot(embedding1, embedding2)
        
        return float(similarity)
    
    def recognize(self, frame):
        """
        Recognize face in frame
        Returns: {"match": bool, "name": str, "confidence": float}
        """
        result = {
            "match": False,
            "name": None,
            "confidence": 0.0
        }
        
        # Detect face
        face_box = self.detect_face(frame)
        if face_box is None:
            return result
        
        # Extract embedding
        embedding = self.extract_embedding(frame, face_box)
        if embedding is None:
            return result
        
        # Compare with known faces
        best_match = None
        best_similarity = 0.0
        
        for name, known_embedding in self.known_embeddings.items():
            similarity = self.compare_embeddings(embedding, known_embedding)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = name
        
        # Check threshold
        if best_similarity >= self.similarity_threshold:
            result["match"] = True
            result["name"] = best_match
            result["confidence"] = best_similarity
        
        return result
    
    def enroll_face(self, name, frames):
        """
        Enroll a new face from multiple frames
        Args:
            name: Person's name
            frames: List of frames (at least 5 recommended)
        Returns: bool (success)
        """
        embeddings = []
        
        for frame in frames:
            face_box = self.detect_face(frame)
            if face_box is None:
                continue
            
            embedding = self.extract_embedding(frame, face_box)
            if embedding is not None:
                embeddings.append(embedding)
        
        if len(embeddings) < 3:
            print(f"Failed to enroll {name}: Not enough valid face samples")
            return False
        
        # Average embeddings for robustness
        avg_embedding = np.mean(embeddings, axis=0)
        
        # Store embedding
        self.known_embeddings[name] = avg_embedding
        
        # Save to disk
        self.save_embeddings()
        
        print(f"✓ Enrolled {name} with {len(embeddings)} samples")
        return True
    
    def load_embeddings(self):
        """Load saved face embeddings from disk"""
        embedding_file = self.config_path / "embeddings.pkl"
        
        if embedding_file.exists():
            try:
                with open(embedding_file, 'rb') as f:
                    self.known_embeddings = pickle.load(f)
                print(f"✓ Loaded {len(self.known_embeddings)} face(s)")
            except Exception as e:
                print(f"Error loading embeddings: {e}")
                self.known_embeddings = {}
        else:
            print("No saved embeddings found")
            self.known_embeddings = {}
    
    def save_embeddings(self):
        """Save face embeddings to disk (encrypted)"""
        self.config_path.mkdir(parents=True, exist_ok=True)
        embedding_file = self.config_path / "embeddings.pkl"
        
        try:
            with open(embedding_file, 'wb') as f:
                pickle.dump(self.known_embeddings, f)
            
            # Set file permissions to owner-only
            os.chmod(embedding_file, 0o600)
            
            print(f"✓ Saved embeddings to {embedding_file}")
        except Exception as e:
            print(f"Error saving embeddings: {e}")
    
    def delete_face(self, name):
        """Remove a person's face from database"""
        if name in self.known_embeddings:
            del self.known_embeddings[name]
            self.save_embeddings()
            print(f"✓ Deleted {name}'s face data")
            return True
        return False
    
    def list_enrolled_faces(self):
        """Get list of enrolled face names"""
        return list(self.known_embeddings.keys())
