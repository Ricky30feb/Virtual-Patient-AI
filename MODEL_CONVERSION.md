# Model Conversion Guide: Fine-tuned Model → GGUF for Ollama

This guide explains how to convert your fine-tuned virtual patient model to GGUF format for easy distribution via Ollama.

## 🔄 Conversion Process

### Option 1: From Hugging Face Model

If your model is saved in Hugging Face format:

```bash
# 1. Install llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

# 2. Convert to GGUF
python convert.py /path/to/your/fine-tuned-model --outdir ./models --outfile virtual_patient.gguf

# 3. Quantize for smaller size (optional but recommended)
./quantize ./models/virtual_patient.gguf ./models/virtual_patient.Q4_K_M.gguf Q4_K_M
```

### Option 2: From MLX Format (Apple Silicon)

If you used MLX for training:

```bash
# Install mlx-lm if not already installed
pip install mlx-lm

# Convert MLX to Hugging Face format first
python -m mlx_lm.convert --model /path/to/mlx/model --upload-repo your-username/virtual-patient-hf

# Then follow Option 1 steps above
```

### Option 3: Using Transformers Library

```python
# conversion_script.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load your fine-tuned model
model_path = "/path/to/your/fine-tuned-model"
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Save in a format compatible with llama.cpp
model.save_pretrained("./virtual_patient_for_conversion")
tokenizer.save_pretrained("./virtual_patient_for_conversion")

# Then use llama.cpp convert.py on this directory
```

## 📤 Distribution Setup

### Step 1: Prepare Files for Distribution

After conversion, you should have:
```
virtual_patient.Q4_K_M.gguf  # Your quantized model (~800MB-1.5GB)
Modelfile                    # Ollama configuration (already created)
```

### Step 2: Upload to Distribution Platform

#### Option A: GitHub Release
1. Create a new release in your GitHub repository
2. Upload `virtual_patient.Q4_K_M.gguf` as a release asset
3. Include `Modelfile` in the repository

#### Option B: Hugging Face Hub
```bash
# Install huggingface_hub
pip install huggingface_hub

# Upload to Hugging Face
huggingface-cli upload your-username/virtual-patient-ai ./virtual_patient.Q4_K_M.gguf
huggingface-cli upload your-username/virtual-patient-ai ./Modelfile
```

#### Option C: Google Drive / Dropbox
1. Upload `virtual_patient.Q4_K_M.gguf` to cloud storage
2. Get shareable download link
3. Update README with download instructions

## 🧪 Testing Your GGUF Model

Before distribution, test the converted model:

```bash
# Create the Ollama model
ollama create virtual-patient -f Modelfile

# Test with a sample prompt
ollama run virtual-patient "Persona: Depressed Patient elderly patients, Doctor's persona: Optimistic Doctor, Patient age: 75. **Doctor**: How are you feeling today? **Patient**:"

# Verify it responds as a patient, not a doctor
```

## 📝 Model Quality Checklist

- [ ] Model responds as patient, not doctor
- [ ] Responses match selected persona personality
- [ ] No meta-commentary (like "As a virtual patient...")
- [ ] Appropriate medical language for patient type
- [ ] Conversation flows naturally
- [ ] Model stops at appropriate points

## 💾 File Size Expectations

- **Original model**: 2-4GB (depending on base model)
- **Q4_K_M quantized**: 800MB - 1.5GB
- **Q8_0 quantized**: 1.5GB - 2.5GB (higher quality)
- **Q2_K quantized**: 400MB - 800MB (smaller, lower quality)

Choose quantization level based on your quality vs. size preferences.

## 🚨 Important Notes

1. **Backup Original**: Keep your original fine-tuned model safe
2. **Test Thoroughly**: Quantization can affect model quality
3. **License Compliance**: Ensure you comply with base model licenses
4. **Documentation**: Update README.md with new download instructions

## Next Steps

1. Convert your model using one of the methods above
2. Test the GGUF model with Ollama
3. Upload to your chosen distribution platform
4. Update the main README.md with download instructions
5. Test the complete user experience
