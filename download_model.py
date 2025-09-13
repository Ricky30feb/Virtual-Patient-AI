#!/usr/bin/env python3
"""
Virtual Patient AI Model Downloader
Downloads the pre-trained GGUF model from Google Drive
"""

import os
import sys
import subprocess

def install_gdown():
    """Install gdown if not available"""
    try:
        import gdown
        return True
    except ImportError:
        print("📦 Installing gdown for Google Drive downloads...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"])
            import gdown
            return True
        except Exception as e:
            print(f"❌ Failed to install gdown: {e}")
            return False

def download_model():
    """Download the model file from Google Drive"""
    
    # Configuration
    DRIVE_FILE_ID = "15vYfdAkdZySX0y-9V3dX17Doe4Z1x-az"
    MODEL_FILE = "virtual_patient.Q4_K_M.gguf"
    MODEL_SIZE = "2.3GB"
    
    print("🏥 Virtual Patient AI - Model Download")
    print("=" * 40)
    print(f"Model: {MODEL_FILE} ({MODEL_SIZE})")
    print("Source: Google Drive")
    print()
    
    # Check if already exists
    if os.path.exists(MODEL_FILE):
        print(f"✅ Model file already exists: {MODEL_FILE}")
        print("   Delete it first if you want to re-download")
        return True
    
    # Install gdown if needed
    if not install_gdown():
        return False
    
    try:
        import gdown
        
        print("📥 Downloading from Google Drive...")
        print(f"   File ID: {DRIVE_FILE_ID}")
        print()
        
        # Download the file
        url = f"https://drive.google.com/uc?id={DRIVE_FILE_ID}"
        gdown.download(url, MODEL_FILE, quiet=False)
        
        # Verify download
        if os.path.exists(MODEL_FILE):
            file_size = os.path.getsize(MODEL_FILE)
            print()
            print(f"✅ Download completed: {MODEL_FILE}")
            print(f"📊 File size: {file_size / (1024**3):.1f}GB")
            return True
        else:
            print("❌ Download failed - file not found")
            return False
            
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def main():
    """Main download function"""
    print("🚀 Starting model download...")
    print()
    
    if download_model():
        print()
        print("🎉 Model download successful!")
        print()
        print("🚀 Next steps:")
        print("1. Create Ollama model: ollama create virtual-patient -f Modelfile")
        print("2. Test setup: python test_setup.py")
        print("3. Run app: streamlit run app.py")
        return True
    else:
        print()
        print("❌ Model download failed")
        print()
        print("💡 Alternative:")
        print("   1. Visit: https://drive.google.com/file/d/15vYfdAkdZySX0y-9V3dX17Doe4Z1x-az/view?usp=sharing")
        print("   2. Click 'Download' to save virtual_patient.Q4_K_M.gguf")
        print("   3. Place the file in this directory")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
