# MAYA API Configuration

## Setting up OpenAI API Key

To use the API-based speech recognition, you need to set your OpenAI API key as an environment variable.

### Option 1: Temporary (Current Session)
```bash
export OPENAI_API_KEY='your-api-key-here'
python -m maya.main
```

### Option 2: Permanent (Add to shell profile)

**For zsh (macOS default):**
```bash
echo "export OPENAI_API_KEY='your-api-key-here'" >> ~/.zshrc
source ~/.zshrc
```

**For bash:**
```bash
echo "export OPENAI_API_KEY='your-api-key-here'" >> ~/.bashrc
source ~/.bashrc
```

### Option 3: Using .env file (Recommended for Development)

1. Create a `.env` file in the project root:
```bash
cd /Volumes/afraz_SSD/maya
touch .env
```

2. Add your API key:
```
OPENAI_API_KEY=your-api-key-here
```

3. Install python-dotenv:
```bash
pip install python-dotenv
```

4. The application will automatically load it.

## Getting an OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (you won't see it again!)
5. Set it as an environment variable

## Model Comparison

| Feature | 🖥️ Local Model | ☁️ API Model |
|---------|---------------|-------------|
| **Cost** | Free | ~$0.006/minute |
| **Privacy** | 100% Private | Data sent to OpenAI |
| **Speed** | Slower (CPU) | Fast (cloud) |
| **Accuracy** | Excellent | Excellent |
| **Internet** | Not required | Required |
| **Setup** | Model download (~140MB) | API key only |

## Usage

1. **Launch MAYA**
2. **Select Model Mode** in the conversation panel:
   - 🖥️ Local Model (default)
   - ☁️ API Model
3. **Click Voice Button** to start recording
4. **Speak** for 5 seconds
5. **Get transcription**

### Switching Between Modes

You can switch between local and API models at any time using the dropdown in the chat panel. The application will automatically use the selected model for all voice inputs.

## Troubleshooting

### "OpenAI API key not found"
- Make sure you've set the `OPENAI_API_KEY` environment variable
- Restart the application after setting the key
- Check the key is valid at https://platform.openai.com/api-keys

### "API transcription error"
- Check your internet connection
- Verify your API key is valid and has credits
- Check OpenAI service status: https://status.openai.com/

### Local model is slow
- Local model runs on CPU, which is slower than API
- Consider using API model for faster responses
- Or upgrade to a GPU-enabled machine for faster local processing

## Cost Considerations

**OpenAI Whisper API Pricing:**
- $0.006 per minute of audio
- Example: 100 voice commands (5 sec each) = 8.3 minutes = $0.05
- Very affordable for occasional use

**Recommendation:**
- Use **Local Model** for privacy-sensitive or frequent use
- Use **API Model** for faster responses and convenience
