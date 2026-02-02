// MAYA Tauri App - JavaScript

class MayaApp {
    constructor() {
        this.isListening = false;
        this.isCameraOn = false;
        this.language = 'en';
        this.apiMode = 'local';
        this.mediaRecorder = null;
        this.cameraStream = null;
        
        this.init();
    }
    
    async init() {
        console.log('Initializing MAYA...');
        this.addMessage('system', 'MAYA Tauri App is ready!');
        this.setupEventListeners();
        await this.setupCamera();
        
        // Optimize video playback
        const waveformVideo = document.getElementById('waveformVideo');
        if (waveformVideo) {
            waveformVideo.playbackRate = 1.0;
        }
    }
    
    setupEventListeners() {
        console.log('Setting up event listeners...');
        
        // Language toggle
        const languageToggle = document.getElementById('languageToggle');
        if (languageToggle) {
            console.log('Language toggle found');
            languageToggle.addEventListener('click', () => {
                languageToggle.classList.toggle('active');
                this.language = languageToggle.classList.contains('active') ? 'bn' : 'en';
                console.log('Language:', this.language);
            });
        } else {
            console.error('Language toggle NOT found');
        }
        
        // API toggle
        const apiToggle = document.getElementById('apiToggle');
        if (apiToggle) {
            console.log('API toggle found');
            apiToggle.addEventListener('click', () => {
                apiToggle.classList.toggle('active');
                this.apiMode = apiToggle.classList.contains('active') ? 'api' : 'local';
                console.log('API Mode:', this.apiMode);
            });
        } else {
            console.error('API toggle NOT found');
        }
        
        // Camera button
        const cameraBtn = document.getElementById('cameraBtn');
        if (cameraBtn) {
            console.log('Camera button found');
            cameraBtn.addEventListener('click', () => {
                console.log('Camera button clicked');
                this.toggleCamera();
            });
        } else {
            console.error('Camera button NOT found');
        }
        
        // Microphone button
        const micBtn = document.getElementById('micBtn');
        if (micBtn) {
            console.log('Microphone button found');
            micBtn.addEventListener('click', () => {
                console.log('Microphone button clicked');
                this.toggleMicrophone();
            });
        } else {
            console.error('Microphone button NOT found');
        }
        
        // Power button
        const powerBtn = document.getElementById('powerBtn');
        if (powerBtn) {
            console.log('Power button found');
            powerBtn.addEventListener('click', () => {
                console.log('Power button clicked');
                if (confirm('Are you sure you want to exit MAYA?')) {
                    this.endSession();
                }
            });
        } else {
            console.error('Power button NOT found');
        }
        
        console.log('Event listeners setup complete');
    }
    
    async setupCamera() {
        try {
            this.cameraStream = await navigator.mediaDevices.getUserMedia({
                video: { 
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                }
            });
            console.log('Camera stream ready');
        } catch (error) {
            console.error('Camera setup failed:', error);
            this.addMessage('system', 'Camera access denied. Please grant permissions.');
        }
    }
    
    toggleCamera() {
        const cameraBtn = document.getElementById('cameraBtn');
        const cameraPreview = document.getElementById('cameraPreview');
        const cameraVideo = document.getElementById('cameraVideo');
        
        if (!cameraBtn || !cameraPreview || !cameraVideo) return;
        
        this.isCameraOn = !this.isCameraOn;
        
        if (this.isCameraOn) {
            cameraBtn.classList.add('active');
            cameraBtn.setAttribute('data-active', 'true');
            cameraPreview.classList.add('active');
            
            if (this.cameraStream) {
                cameraVideo.srcObject = this.cameraStream;
                cameraVideo.style.display = 'block';
                cameraVideo.play();
                this.addMessage('system', 'Camera turned on');
            }
        } else {
            cameraBtn.classList.remove('active');
            cameraBtn.setAttribute('data-active', 'false');
            cameraPreview.classList.remove('active');
            
            if (cameraVideo.srcObject) {
                cameraVideo.pause();
                cameraVideo.srcObject = null;
                cameraVideo.style.display = 'none';
            }
            this.addMessage('system', 'Camera turned off');
        }
    }
    
    async toggleMicrophone() {
        const micBtn = document.getElementById('micBtn');
        if (!micBtn) return;
        
        this.isListening = !this.isListening;
        
        if (this.isListening) {
            micBtn.classList.add('active');
            micBtn.setAttribute('data-active', 'true');
            await this.startListening();
        } else {
            micBtn.classList.remove('active');
            micBtn.setAttribute('data-active', 'false');
            this.stopListening();
        }
    }
    
    async startListening() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 16000
                }
            });
            
            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm'
            });
            
            let audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            
            this.mediaRecorder.onstop = async () => {
                if (audioChunks.length > 0) {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    console.log('Audio recorded:', audioBlob.size, 'bytes');
                    
                    // Simulate transcription (replace with actual API call)
                    this.addMessage('user', 'Voice input detected');
                    this.addMessage('ai', 'This is a demo response. Connect to backend for real transcription.');
                    
                    audioChunks = [];
                }
                
                // Continue listening if still active
                if (this.isListening) {
                    setTimeout(() => {
                        if (this.isListening && this.mediaRecorder) {
                            this.mediaRecorder.start();
                            setTimeout(() => {
                                if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
                                    this.mediaRecorder.stop();
                                }
                            }, 5000);
                        }
                    }, 100);
                }
            };
            
            this.mediaRecorder.start();
            this.addMessage('system', 'Listening... (5-second intervals)');
            
            // Stop after 5 seconds
            setTimeout(() => {
                if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
                    this.mediaRecorder.stop();
                }
            }, 5000);
            
        } catch (error) {
            console.error('Microphone access failed:', error);
            this.isListening = false;
            const micBtn = document.getElementById('micBtn');
            if (micBtn) {
                micBtn.classList.remove('active');
                micBtn.setAttribute('data-active', 'false');
            }
            this.addMessage('system', 'Microphone access denied. Please grant permissions.');
        }
    }
    
    stopListening() {
        if (this.mediaRecorder) {
            if (this.mediaRecorder.state === 'recording') {
                this.mediaRecorder.stop();
            }
            
            if (this.mediaRecorder.stream) {
                const tracks = this.mediaRecorder.stream.getTracks();
                tracks.forEach(track => track.stop());
            }
            
            this.mediaRecorder = null;
        }
        this.addMessage('system', 'Listening stopped');
    }
    
    addMessage(sender, text) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const timestamp = new Date().toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        if (sender === 'system') {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <p style="color: #4A9EAD; font-style: italic;">${text}</p>
                    <span class="message-time">${timestamp}</span>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <p>${text}</p>
                    <span class="message-time">${timestamp}</span>
                </div>
            `;
        }
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    async endSession() {
        console.log('Ending session...');
        this.addMessage('system', 'Shutting down MAYA...');
        
        // Stop camera
        if (this.cameraStream) {
            const tracks = this.cameraStream.getTracks();
            tracks.forEach(track => track.stop());
            this.cameraStream = null;
            console.log('Camera stopped');
        }
        
        // Stop microphone
        if (this.mediaRecorder) {
            this.stopListening();
            console.log('Microphone stopped');
        }
        
        // Add a brief delay for visual feedback
        await new Promise(resolve => setTimeout(resolve, 300));
        
        console.log('Closing application...');
        
        // Use Tauri's invoke to call the exit command
        try {
            if (window.__TAURI__) {
                const { invoke } = window.__TAURI__.core;
                await invoke('exit_app');
            } else {
                // Fallback for non-Tauri environment
                window.close();
            }
        } catch (error) {
            console.error('Error closing application:', error);
            // Force close as last resort
            window.close();
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.mayaApp = new MayaApp();
});
