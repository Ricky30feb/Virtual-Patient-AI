"""
Simplified Text-to-Speech Module for Virtual Patient System
"""

import pyttsx3
import threading
from typing import Optional


class VirtualPatientTTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._setup_voice()
        
    def _setup_voice(self):
        """Setup a single voice for all patients"""
        voices = self.engine.getProperty('voices')
        
        preferred_voice_index = None
        
        for i, voice in enumerate(voices):
            if 'en-IN.Rishi' in voice.id or 'Rishi' in voice.name:
                preferred_voice_index = i
                break
        
        if preferred_voice_index is None and voices:
            preferred_voice_index = 0
            
        if preferred_voice_index is not None:
            self.engine.setProperty('voice', voices[preferred_voice_index].id)
            print(f"TTS Voice: {voices[preferred_voice_index].name}")
        
        self.engine.setProperty('rate', 170)
        self.engine.setProperty('volume', 0.9)
    
    def speak_text(self, text: str, persona: Optional[str] = None, blocking: bool = False):
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            persona: Patient persona (ignored in simplified version)
            blocking: Whether to wait for speech to complete
        """
        if not text or not text.strip():
            return
            
        try:
            if blocking:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                thread = threading.Thread(target=self._speak_async, args=(text,))
                thread.daemon = True
                thread.start()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def _speak_async(self, text: str):
        """Speak text asynchronously"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Async TTS Error: {e}")
    
    def stop(self):
        """Stop current speech"""
        try:
            self.engine.stop()
        except Exception as e:
            print(f"TTS Stop Error: {e}")


VirtualPatientTTS.set_voice_for_persona = lambda self, persona: None
