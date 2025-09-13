#!/bin/bash
# Virtual Patient AI Model Download Script
# Downloads the pre-trained GGUF model from Google Drive

set -e

# Google Drive file ID (extracted from the sharing link)
DRIVE_FILE_ID="15vYfdAkdZySX0y-9V3dX17Doe4Z1x-az"
MODEL_FILE="virtual_patient.Q4_K_M.gguf"
MODEL_SIZE="2.3GB"

echo "🏥 Virtual Patient AI - Model Download"
echo "======================================"
echo "Downloading model: $MODEL_FILE ($MODEL_SIZE)"
echo "Source: Google Drive"
echo ""

# Check if model already exists
if [ -f "$MODEL_FILE" ]; then
    echo "✅ Model file already exists: $MODEL_FILE"
    echo "   Delete it first if you want to re-download"
    exit 0
fi

# Download using gdown (Google Drive downloader)
echo "📥 Downloading from Google Drive..."
echo "   File ID: $DRIVE_FILE_ID"
echo ""

# Check if gdown is available
if ! command -v gdown >/dev/null 2>&1; then
    echo "📦 Installing gdown for Google Drive downloads..."
    pip install gdown
fi

# Download the file
gdown "https://drive.google.com/uc?id=$DRIVE_FILE_ID" -O "$MODEL_FILE"

# Verify download
if [ -f "$MODEL_FILE" ]; then
    echo ""
    echo "✅ Download completed: $MODEL_FILE"
    echo "📊 File size: $(ls -lh "$MODEL_FILE" | awk '{print $5}')"
    echo ""
    echo "🚀 Next steps:"
    echo "1. Create Ollama model: ollama create virtual-patient -f Modelfile"
    echo "2. Test setup: python test_setup.py"
    echo "3. Run app: streamlit run app.py"
else
    echo "❌ Download failed"
    exit 1
fi
