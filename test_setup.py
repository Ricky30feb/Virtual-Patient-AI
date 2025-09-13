#!/usr/bin/env python3
"""
Test script for Virtual Patient AI setup
Verifies that all components are working correctly
"""

import sys
import subprocess
import requests
import json

def test_python_dependencies():
    """Test if required Python packages are installed"""
    print("🔍 Testing Python dependencies...")
    
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit not installed")
        return False
    
    try:
        import requests
        print(f"✅ Requests {requests.__version__}")
    except ImportError:
        print("❌ Requests not installed")
        return False
        
    try:
        import pyttsx3
        print("✅ pyttsx3 available")
    except ImportError:
        print("❌ pyttsx3 not installed")
        return False
        
    return True

def test_ollama_connection():
    """Test connection to Ollama service"""
    print("\n🔍 Testing Ollama connection...")
    
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=5)
        if response.status_code == 200:
            version_info = response.json()
            print(f"✅ Ollama connected - Version: {version_info.get('version', 'Unknown')}")
            return True
        else:
            print(f"❌ Ollama connection failed - Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama not accessible: {e}")
        print("   Make sure Ollama is running: ollama serve")
        return False

def test_virtual_patient_model():
    """Test if virtual patient model is available"""
    print("\n🔍 Testing virtual patient model...")
    
    try:
        # List models
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            models = result.stdout
            if "virtual-patient" in models:
                print("✅ virtual-patient model found")
                return True
            else:
                print("❌ virtual-patient model not found")
                print("   Available models:")
                for line in models.split('\n')[1:]:
                    if line.strip():
                        print(f"   - {line.split()[0]}")
                print("\n   To create the model:")
                print("   1. Download virtual_patient.Q4_K_M.gguf")
                print("   2. Run: ollama create virtual-patient -f Modelfile")
                return False
        else:
            print(f"❌ Failed to list models: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Ollama command timed out")
        return False
    except FileNotFoundError:
        print("❌ Ollama command not found - is Ollama installed?")
        return False

def test_model_response():
    """Test model response quality"""
    print("\n🔍 Testing model response...")
    
    test_prompt = """Persona: Optimistic Patient elderly patients, Doctor's persona: Optimistic Doctor, Patient age: 75
**Doctor**: Good morning! How are you feeling today?
**Patient**:"""
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "virtual-patient",
                "prompt": test_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 100
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            patient_response = result.get("response", "").strip()
            
            if patient_response:
                print("✅ Model responded successfully")
                print(f"   Response: {patient_response[:100]}...")
                
                # Check if response seems appropriate
                if any(word in patient_response.lower() for word in ["good", "fine", "well", "feeling", "morning", "doctor"]):
                    print("✅ Response seems contextually appropriate")
                    return True
                else:
                    print("⚠️  Response may not be contextually appropriate")
                    return True
            else:
                print("❌ Model returned empty response")
                return False
        else:
            print(f"❌ Model request failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_tts_system():
    """Test TTS system"""
    print("\n🔍 Testing TTS system...")
    
    try:
        from tts_system import VirtualPatientTTS
        
        tts = VirtualPatientTTS()
        print("✅ TTS system initialized successfully")
        
        # Test speak function (without actually playing audio)
        tts.speak_text("Test message", blocking=False)
        print("✅ TTS speak function working")
        
        return True
        
    except Exception as e:
        print(f"❌ TTS system failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Virtual Patient AI Setup Test")
    print("=" * 40)
    
    tests = [
        ("Python Dependencies", test_python_dependencies),
        ("Ollama Connection", test_ollama_connection),
        ("Virtual Patient Model", test_virtual_patient_model),
        ("Model Response", test_model_response),
        ("TTS System", test_tts_system)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 40)
    print("📊 Test Results Summary:")
    
    passed = 0
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 All tests passed! Your Virtual Patient AI is ready to use.")
        print("   Start the app: streamlit run app.py")
    else:
        print(f"\n⚠️  {len(tests) - passed} test(s) failed. Please check the setup.")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
