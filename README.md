# Virtual Patient AI System

An AI-powered virtual patient simulation system for medical training, featuring personality-based patient personas with Indian text-to-speech capabilities and an interactive Streamlit interface.

## 🎯 Features

- **Personality-Based Patients**: 9+ unique patient personas (Depressed, Optimistic, Self-Diagnosing, etc.)
- **Ollama Integration**: Uses fine-tuned virtual-patient-llama32-1b-patientonly model
- **Indian TTS Voice**: Single optimized Rishi (English-India) voice for all personas
- **Interactive UI**: Clean Streamlit web interface for real-time medical conversations
- **Medical Training**: Realistic patient dialogues based on 1,433 training examples
- **Context Retention**: Maintains conversation history for natural interactions

## 📋 System Requirements

- **Python**: 3.8+ (Tested with 3.13)
- **Memory**: 4GB+ RAM recommended
- **Platform**: macOS/Linux/Windows
- **Ollama**: Required for AI model inference
- **TTS**: System text-to-speech engine (pyttsx3)

## 🚀 Complete Setup Guide

### 1. Prerequisites

#### Install Ollama
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows - Download from https://ollama.ai
```

#### Start Ollama Service
```bash
# Start Ollama server
ollama serve
```

### 2. Install Virtual Patient Model

#### Method 1: Download Pre-built GGUF Model (Recommended - Easy Setup)

**Step A: Download the GGUF model file**
```bash
# Option 1: From GitHub Releases (when available)
wget https://github.com/[your-username]/virtual-patient-ai/releases/download/v1.0/virtual_patient.Q4_K_M.gguf

# Option 2: From Hugging Face (when available)  
huggingface-cli download [your-username]/virtual-patient-ai virtual_patient.Q4_K_M.gguf

# Option 3: From Google Drive (when available)
# Download manually from provided link
```

**Step B: Create the Ollama model**
```bash
# Navigate to project directory
cd "Virtual Patient AI"

# Create model from GGUF + Modelfile
ollama create virtual-patient -f Modelfile

# Verify model was created
ollama list | grep virtual-patient
```

#### Method 2: Use Base Model + Modelfile (Fallback Option)
```bash
# Pull base model and create virtual patient model
ollama pull llama3.2:1b
ollama create virtual-patient-basic -f Modelfile

# Note: This uses the base model, not the fine-tuned version
# Quality will be lower than the GGUF version
```

### 3. Project Setup

```bash
# Navigate to project directory
cd "Virtual Patient AI"

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 4. Run the Application

```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Start the Streamlit app
streamlit run app.py
```

### 5. Verify Setup (Optional)

```bash
# Run setup verification test
python test_setup.py

# If all tests pass, you're ready to go!
# If tests fail, check the specific error messages
```

### 6. Access the Application

Open your browser to `http://localhost:8501` to start interacting with virtual patients!

## 📦 For Model Creators: Distributing Your Fine-tuned Model

If you've fine-tuned your own virtual patient model and want to share it:

### Step 1: Convert to GGUF Format
```bash
# See MODEL_CONVERSION.md for detailed instructions
# This converts your fine-tuned model to GGUF format for easy distribution
```

### Step 2: Upload Files
Upload these files to your distribution platform:
- `virtual_patient.Q4_K_M.gguf` (~1GB) - Your quantized model
- `Modelfile` - Ollama configuration (already included)

### Step 3: Update README
Update the download links in Step 2 of the setup guide with your actual URLs.

### Popular Distribution Options:
- **GitHub Releases**: Free, easy to use
- **Hugging Face Hub**: Built for ML models  
- **Google Drive**: Simple sharing
- **Direct hosting**: Your own server

## 📦 Dependencies

The system requires these Python packages (auto-installed via requirements.txt):

```txt
streamlit>=1.32.0      # Web interface
requests>=2.31.0       # HTTP requests to Ollama
pyttsx3>=2.90          # Text-to-speech engine
```

## 📁 Project Structure

```
Virtual Patient AI/
├── data/
│   └── train.jsonl           # Training data with patient personas (940K)
├── app.py                    # Main Streamlit application (20K)
├── tts_system.py            # Simplified TTS system (4K)
├── Modelfile                # Ollama model configuration for GGUF model
├── MODEL_CONVERSION.md      # Guide for converting fine-tuned model to GGUF
├── requirements.txt         # Python dependencies
└── README.md               # Setup documentation

# Additional files you'll create:
├── virtual_patient.Q4_K_M.gguf  # Your fine-tuned model in GGUF format (~1GB)
```

## 🎭 Available Patient Personas

The system loads personalities from training data:

- **Depressed Patient** (elderly patients)
- **Optimistic Patient** (elderly patients)  
- **Overly Trusting Patient** (elderly patients)
- **Self-Diagnosing Patient** (young adults)
- **Silent Patient** (middle-aged)
- **Forgetful Patient** (young adults)
- **Guilty Patient** (elderly patients)
- **Relieved Patient** (elderly patients)
- **Reluctant Patient** (elderly patients)

Each persona includes age groups, diversity factors, and doctor interaction styles.

## 🗣️ Text-to-Speech

**Optimized Single Voice System:**
- **Voice**: Rishi (English-India, Male)
- **Speech Rate**: 170 WPM
- **Volume**: 90%
- **Usage**: All patient personas use the same optimized voice for consistency

## 🎬 Usage Guide

1. **Start the Application**
   ```bash
   streamlit run app.py
   ```

2. **Select a Patient Persona**
   - Choose from dropdown menu (loads from training data)
   - Each persona has unique personality traits and medical context

3. **Begin Medical Conversation**
   - Type your message as a doctor
   - Patient responds based on selected persona
   - TTS speaks the patient's response aloud

4. **Continue Dialogue**
   - System maintains conversation context
   - Build realistic medical training scenarios
   - Practice different patient interaction types

## 🔧 Configuration

### Model Configuration
- **Model**: `virtual-patient-llama32-1b-patientonly`
- **Size**: 2.5GB
- **Context**: 2048 tokens
- **Temperature**: 0.7 (balanced creativity/consistency)

### TTS Configuration
Edit `tts_system.py` to modify:
- Speech rate: `self.engine.setProperty('rate', 170)`
- Volume: `self.engine.setProperty('volume', 0.9)`
- Voice selection preferences

## 🔧 Troubleshooting

### Common Issues

**1. Ollama not found or connection failed**
```bash
# Make sure Ollama is installed and running
ollama serve

# Check if service is running
curl http://localhost:11434/api/version
```

**2. Virtual patient model missing**
```bash
# List available models
ollama list

# Method 1: Create from GGUF (recommended)
# First download virtual_patient.Q4_K_M.gguf to project directory, then:
ollama create virtual-patient -f Modelfile

# Method 2: Create from base model (fallback)
ollama pull llama3.2:1b
ollama create virtual-patient-basic -f Modelfile

# Test the model
ollama run virtual-patient "Persona: Optimistic Patient elderly patients. **Doctor**: How are you feeling today? **Patient**:"
```
```bash
# List available models
ollama list

# Pull the required model if missing
ollama pull virtual-patient-llama32-1b-patientonly
```

**3. TTS not working**
- **macOS**: Ensure System Preferences > Security > Microphone access is enabled
- **Linux**: Install espeak: `sudo apt-get install espeak espeak-data`
- **Windows**: Windows Speech Platform should be available by default
- Check audio output settings and volume

**4. Streamlit won't start**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

**5. No personas loading**
- Verify `data/train.jsonl` exists and is readable
- Check file permissions
- Fallback personas will load if data file is missing

### Performance Tips

- **Model Loading**: First response may be slow as model initializes
- **Memory Usage**: 2.5GB model + ~1GB Python overhead
- **Response Time**: Typically 2-3 seconds per response
- **TTS Latency**: ~1-2 seconds for speech synthesis

### Development Mode

For debugging and development:
```bash
# Run with verbose logging
streamlit run app.py --logger.level=debug

# Check Ollama model details
ollama show virtual-patient-llama32-1b-patientonly
```

## 🏥 Medical Training Applications

### Use Cases
- **Communication Skills**: Practice patient interaction techniques
- **Persona Handling**: Learn to work with different personality types
- **Cultural Sensitivity**: Experience Indian healthcare communication patterns
- **Diagnostic Practice**: Gather patient information through conversation
- **Scenario Building**: Create complex multi-turn medical dialogues

### Educational Benefits
- **Safe Environment**: Practice without real patient impact
- **Reproducible Scenarios**: Consistent persona behaviors for training
- **Immediate Feedback**: Real-time conversation practice
- **Diverse Patient Types**: Experience range of patient personalities
- **Accessibility**: Available 24/7 for continuous learning

## 📊 Training Data Details

### Dataset Composition
- **Total Conversations**: 1,433 medical dialogues
- **Patient Personas**: 9+ unique personality types
- **Age Groups**: Young adults, middle-aged, elderly patients
- **Medical Contexts**: Various conditions and interaction scenarios
- **Doctor Personas**: Different doctor communication styles
- **Diversity Factors**: Socioeconomic, cultural, and demographic variations

### Data Format
```json
{
  "input": "Persona: Depressed Patient elderly patients, Doctor's persona: Direct and Blunt Doctor, Patient age: 75...",
  "output": "Good afternoon, Doctor Mehta. I've been feeling quite unwell lately..."
}
```

## 🛠️ Advanced Configuration

### Custom Model Creation

The `Modelfile` allows you to customize the virtual patient model:

1. **Modify System Prompt** (lines 10-20):
   ```modelfile
   SYSTEM """You are a virtual patient...
   [Customize patient behavior instructions here]
   """
   ```

2. **Adjust Model Parameters**:
   ```modelfile
   PARAMETER temperature 0.7      # Creativity (0.1-1.0)
   PARAMETER top_p 0.9           # Nucleus sampling  
   PARAMETER repeat_penalty 1.2  # Avoid repetition
   PARAMETER num_ctx 2048        # Context window
   ```

3. **Update Stop Sequences**:
   ```modelfile
   PARAMETER stop "Doctor:"      # Prevents model from speaking as doctor
   PARAMETER stop "**Doctor**:"  # Add more stop sequences as needed
   ```

4. **Recreate Model with Changes**:
   ```bash
   # Remove existing model
   ollama rm virtual-patient-llama32-1b-patientonly
   
   # Create new model with updated Modelfile
   ollama create virtual-patient-llama32-1b-patientonly -f Modelfile
   ```

### Using Different Base Models

To use a different base model, edit the first line of `Modelfile`:
```modelfile
FROM llama3.2:1b          # Current (fast, smaller)
# FROM llama3.2:3b        # Better quality, larger
# FROM gemma2:2b          # Alternative model
```

### Custom Model Usage

To use a different Ollama model in the app:
1. Edit `app.py` line ~45:
   ```python
   model_name: str = "your-custom-model-name"
   ```

### Model Testing

Test your model directly with Ollama:
```bash
# Interactive testing
ollama run virtual-patient-llama32-1b-patientonly

# Single prompt testing
ollama run virtual-patient-llama32-1b-patientonly "Persona: Depressed Patient elderly patients. **Doctor**: What brings you in today? **Patient**:"
```

### TTS Customization

Modify voice settings in `tts_system.py`:
```python
# Speech rate (words per minute)
self.engine.setProperty('rate', 170)

# Volume (0.0 to 1.0)  
self.engine.setProperty('volume', 0.9)

# Voice selection (comment/uncomment as needed)
if 'en-IN.Rishi' in voice.id or 'Rishi' in voice.name:
    preferred_voice_index = i
    break
```

### Adding New Personas

To add custom patient personas:
1. Edit the fallback personas in `app.py` (lines ~35-42)
2. Or add entries to `data/train.jsonl` with format:
   ```json
   {"input": "Persona: [Your Custom Persona]...", "output": "Patient response..."}
   ```


### Development Setup
```bash
# Clone repository
git clone [repository-url]
cd "Virtual Patient AI"

# Create development environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
streamlit run app.py --server.headless false
```

### Code Structure
- `app.py`: Main Streamlit application and UI logic
- `tts_system.py`: Text-to-speech functionality
- `data/train.jsonl`: Training conversations and persona definitions

### Testing
```bash
# Test TTS system
python3 -c "from tts_system import VirtualPatientTTS; tts = VirtualPatientTTS(); tts.speak_text('Test message')"

# Test model connection
python3 -c "import requests; print(requests.get('http://localhost:11434/api/version').json())"
```

### Improvements
- Add different voices for different personas.

## 🎁 GGUF Distribution Method

**For users receiving a pre-trained GGUF model file:**

⚠️ **Note**: The model file `virtual_patient.Q4_K_M.gguf` (2.3GB) is not included in this repository due to GitHub file size limits. 

### Option 1: Download Pre-trained Model
1. **Download the model file** from the releases section or your preferred distribution method
2. **Place it in the project directory** as `virtual_patient.Q4_K_M.gguf`
3. **Create the Ollama model:**
   ```bash
   ollama create virtual-patient -f Modelfile
   ```

### Option 2: Train Your Own Model
Follow the original training instructions in the documentation to create your own fine-tuned model.

### Verification
4. **Verify the model:**
   ```bash
   ollama list
   # Should show: virtual-patient:latest
   ```
5. **Run setup test:**
   ```bash
   python test_setup.py
   # Should pass all 5 tests
   ```

✅ **Model Conversion Complete**: The original fine-tuned model has been successfully extracted to GGUF format for easy distribution without requiring the original training process.

---

🎯 **Ready to Use**: Your Virtual Patient AI system is now fully operational with GGUF distribution support!
