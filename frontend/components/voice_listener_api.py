"""
Voice Listener Component for MAYA (API Version)
Handles speech-to-text using OpenAI Whisper API
Supports English and Bangla languages
"""
import os
import sounddevice as sd
import numpy as np
import queue
import threading
import tempfile
import wave
from PyQt6.QtCore import QObject, pyqtSignal
from openai import OpenAI


class VoiceListenerAPI(QObject):
    """Voice listener with OpenAI Whisper API for speech recognition"""
    
    # Signals
    transcription_ready = pyqtSignal(str)  # Emits transcribed text
    listening_started = pyqtSignal()
    listening_stopped = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self, api_key=None, language="en"):
        """
        Initialize voice listener with API
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env variable)
            language: Language code ('en' for English, 'bn' for Bangla)
        """
        super().__init__()
        self.language = language  # 'en' or 'bn'
        self.sample_rate = 16000
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.is_recording = False
        
        # Initialize OpenAI client
        try:
            self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
            print("OpenAI API client initialized successfully!")
        except Exception as e:
            self.error_occurred.emit(f"Failed to initialize OpenAI client: {str(e)}")
            self.client = None
    
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
        if self.client is None:
            self.error_occurred.emit("OpenAI API not initialized. Check your API key.")
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
                dtype=np.int16,  # API prefers int16
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
                audio = np.concatenate(audio_data, axis=0)
                
                # Transcribe in separate thread
                transcribe_thread = threading.Thread(
                    target=self._transcribe_audio_api, 
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
    
    def _transcribe_audio_api(self, audio):
        """Transcribe audio to text using OpenAI API (runs in separate thread)"""
        try:
            print("Transcribing audio with OpenAI API...")
            
            # Save audio to temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                temp_path = temp_audio.name
                
                # Write WAV file
                with wave.open(temp_path, 'wb') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(self.sample_rate)
                    wav_file.writeframes(audio.tobytes())
            
            # Call OpenAI API
            with open(temp_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=self.language if self.language != 'bn' else None  # API uses 'en', 'es', etc.
                )
            
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
            
            text = transcript.text.strip()
            print(f"Transcription: {text}")
            
            # Emit result
            self.transcription_ready.emit(text)
            
        except Exception as e:
            self.error_occurred.emit(f"API transcription error: {str(e)}")
            # Clean up temp file on error
            try:
                if 'temp_path' in locals():
                    os.unlink(temp_path)
            except:
                pass
    
    def stop_listening(self):
        """Stop recording"""
        self.is_recording = False
        self.is_listening = False
