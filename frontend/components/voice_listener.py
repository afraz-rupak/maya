"""
Voice Listener Component for MAYA
Handles speech-to-text using OpenAI Whisper
Supports English and Bangla languages
"""
import whisper
import sounddevice as sd
import numpy as np
import queue
import threading
from PyQt6.QtCore import QObject, pyqtSignal


class VoiceListener(QObject):
    """Voice listener with OpenAI Whisper for speech recognition"""
    
    # Signals
    transcription_ready = pyqtSignal(str)  # Emits transcribed text
    listening_started = pyqtSignal()
    listening_stopped = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self, model_size="base", language="en"):
        """
        Initialize voice listener
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            language: Language code ('en' for English, 'bn' for Bangla)
        """
        super().__init__()
        self.model_size = model_size
        self.language = language  # 'en' or 'bn'
        self.model = None
        self.sample_rate = 16000
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.is_recording = False
        self.stream = None
        
    def load_model(self):
        """Load Whisper model (call this in a separate thread)"""
        try:
            print(f"Loading Whisper {self.model_size} model...")
            self.model = whisper.load_model(self.model_size)
            print("Model loaded successfully!")
        except Exception as e:
            self.error_occurred.emit(f"Failed to load model: {str(e)}")
    
    def set_language(self, language_code):
        """
        Change language
        
        Args:
            language_code: 'en' for English, 'bn' for Bangla
        """
        self.language = language_code
    
    def audio_callback(self, indata, frames, time, status):
        """Callback for audio stream"""
        if status:
            print(f"Audio status: {status}")
        if self.is_recording:
            self.audio_queue.put(indata.copy())
    
    def start_listening(self, duration=5):
        """
        Start recording audio for specified duration
        
        Args:
            duration: Recording duration in seconds
        """
        if self.model is None:
            self.error_occurred.emit("Model not loaded. Please wait...")
            return
        
        self.is_listening = True
        self.is_recording = True
        self.listening_started.emit()
        
        # Start recording in a separate thread
        thread = threading.Thread(target=self._record_audio, args=(duration,))
        thread.daemon = True
        thread.start()
    
    def _record_audio(self, duration):
        """Record audio (runs in separate thread)"""
        audio_data = []
        
        try:
            # Clear queue
            while not self.audio_queue.empty():
                self.audio_queue.get()
            
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.float32,
                callback=self.audio_callback
            ):
                print(f"Recording for {duration} seconds...")
                # Calculate number of chunks based on blocksize
                chunks = int(self.sample_rate * duration / 1024)
                
                for _ in range(chunks):
                    if not self.is_recording:
                        break
                    try:
                        data = self.audio_queue.get(timeout=1)
                        audio_data.append(data)
                    except queue.Empty:
                        continue
            
            self.is_recording = False
            self.listening_stopped.emit()
            
            if audio_data:
                # Combine audio chunks
                audio = np.concatenate(audio_data, axis=0).flatten()
                
                # Transcribe in separate thread
                transcribe_thread = threading.Thread(
                    target=self._transcribe_audio, 
                    args=(audio,)
                )
                transcribe_thread.daemon = True
                transcribe_thread.start()
            else:
                self.error_occurred.emit("No audio recorded")
                
        except Exception as e:
            self.is_recording = False
            self.listening_stopped.emit()
            self.error_occurred.emit(f"Recording error: {str(e)}")
    
    def _transcribe_audio(self, audio):
        """Transcribe audio to text (runs in separate thread)"""
        try:
            print("Transcribing audio...")
            
            # Set language for transcription
            result = self.model.transcribe(
                audio, 
                language=self.language,
                fp16=False
            )
            
            text = result["text"].strip()
            print(f"Transcription: {text}")
            
            # Emit result
            self.transcription_ready.emit(text)
            
        except Exception as e:
            self.error_occurred.emit(f"Transcription error: {str(e)}")
    
    def stop_listening(self):
        """Stop recording"""
        self.is_recording = False
        self.is_listening = False
