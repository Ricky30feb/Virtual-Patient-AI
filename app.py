import streamlit as st
import json
import os
import requests
from typing import List, Dict
from tts_system import VirtualPatientTTS


class VirtualPatientApp:
    def __init__(self):
        self.tts_engine = VirtualPatientTTS()
        self.available_personas = self._load_available_personas()

    def _load_available_personas(self) -> List[str]:
        """Load available patient personas from the dataset"""
        personas = []
        if os.path.exists("data/train.jsonl"):
            try:
                with open("data/train.jsonl", "r", encoding="utf-8") as f:
                    for line in f:
                        data = json.loads(line)
                        if "Persona:" in data["input"]:
                            persona_line = data["input"].split("\n")[0]
                            persona = persona_line.replace("Persona:", "").strip()
                            if persona and persona not in personas:
                                personas.append(persona)
                        if len(personas) >= 50:
                            break
            except Exception as e:
                st.error(f"Error loading personas: {e}")

        if not personas:
            personas = [
                "65-year-old male with type 2 diabetes and hypertension, retired teacher",
                "28-year-old female nurse with anxiety and sleep issues",
                "45-year-old construction worker with lower back pain",
                "72-year-old female with mild cognitive impairment and arthritis",
                "35-year-old mother of two with postpartum depression",
                "19-year-old college student with eating disorder concerns",
                "58-year-old businessman with chest pain and high stress",
            ]
        return personas[:20]

    def query_ollama_model(self, prompt: str, model_name: str = "virtual-patient") -> str:
        """Query the Ollama model with a prompt"""
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "repeat_penalty": 1.2,
                        "num_ctx": 2048,
                        "stop": ["Doctor:", "Patient:", "**Doctor**:", "**Patient**:", "\nDoctor:", "\nPatient:"],
                        "num_predict": 150,
                    },
                },
                timeout=30,
            )
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response generated")
            return f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Make sure Ollama is running."
        except Exception as e:
            return f"Error querying model: {str(e)}"

    def clean_patient_response(self, response: str) -> str:
        """Clean and extract only the patient response"""
        if not response:
            return response
            
        lines = response.strip().split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if any(pattern in line.lower() for pattern in [
                'doctor:', 'patient:', 'dr.:', 'dr:', '**doctor**:', '**patient**:',
                'conversation:', 'response:', 'doctor says:', 'patient says:',
                'doctor replies:', 'patient replies:'
            ]):
                continue
            if line in ['**Patient**:', '**Doctor**:', 'Patient:', 'Doctor:', '*', '**', '---']:
                continue
            if line.startswith(('Dr.', 'Dr:', 'Doctor:', 'Patient:', '**')):
                continue
            cleaned_lines.append(line)
        
        cleaned_response = ' '.join(cleaned_lines)
        
        patterns_to_remove = [
            '**Patient**:', '**Doctor**:', 'Patient:', 'Doctor:', 'Dr.:', 'Dr:',
            'Patient responds:', 'Patient says:', 'The patient says:', 'Response:'
        ]
        
        for pattern in patterns_to_remove:
            cleaned_response = cleaned_response.replace(pattern, '')
        
        cleaned_response = ' '.join(cleaned_response.split())
        
        return cleaned_response.strip()

    def format_prompt(self, persona: str, history: List[Dict[str, str]], doctor_input: str) -> str:
        """Format conversation for prompt"""
        prompt = f"You are a virtual patient with this persona: {persona}\n\n"
        
        prompt += "Respond ONLY as the patient. Do not include any conversation history or speaker labels in your response.\n"
        prompt += "Keep your response brief, realistic, and in character.\n\n"
        
        recent_history = history[-3:] if len(history) > 3 else history
        if recent_history:
            prompt += "Recent conversation:\n"
            for turn in recent_history:
                speaker = "Doctor" if turn["role"] == "doctor" else "Patient"
                prompt += f"{speaker}: {turn['content']}\n"
        
        if doctor_input.strip():
            prompt += f"Doctor: {doctor_input}\n"
        
        prompt += "\nRespond as the patient (your response only, no labels):"
        return prompt

    def _inject_custom_css(self):
        """Inject custom CSS for professional styling"""
        st.markdown("""
        <style>
        .main-header {
            text-align: center;
            color: #1e3a8a;
            font-family: 'serif';
            margin-bottom: 1rem;
            font-size: 2rem;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
            font-style: italic;
        }

        .prompt-button {
            margin: 0.2rem;
            font-size: 0.9rem;
        }
        .stChatMessage {
            margin-bottom: 1rem;
        }
        .css-1d391kg {
            width: 0px;
        }
        /* Make chat input area more prominent */
        .stChatInput > div {
            border-radius: 25px;
            border: 2px solid #1e3a8a;
        }
        /* Hide Streamlit menu and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        header {visibility: hidden;}
        
        /* Status indicator */
        .status-indicator {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 500;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        .status-online {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status-offline {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
            width: 100%;
            margin-bottom: 0.5rem;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(30,58,138,0.3);
        }
        
        /* Clear button styling */
        .clear-button > button {
            background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        }
        
        .clear-button > button:hover {
            box-shadow: 0 4px 12px rgba(220,38,38,0.3);
        }
        </style>
        """, unsafe_allow_html=True)

    def _render_header(self):
        """Render the application header"""
        st.markdown("""
        <div class="app-header">
            <h1 class="app-title">🏥 Virtual Patient Simulator</h1>
            <p class="app-subtitle">Advanced AI-Powered Medical Training Platform</p>
        </div>
        """, unsafe_allow_html=True)

    def _render_control_panel(self):
        """Render the control panel"""
        with st.container():
            st.markdown('<div class="control-panel">', unsafe_allow_html=True)
            st.markdown('<div class="control-title">Patient Configuration</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                persona = st.selectbox(
                    "Select Patient Persona",
                    self.available_personas,
                    index=self.available_personas.index(st.session_state.current_persona)
                    if st.session_state.current_persona in self.available_personas
                    else 0,
                    key="persona_selector",
                    help="Choose the virtual patient you want to interact with"
                )
                
                if persona != st.session_state.current_persona:
                    st.session_state.current_persona = persona
                    st.session_state.conversation_history = []
                    st.rerun()
            
            with col2:
                if st.button("🔄 Reset Chat", help="Clear conversation history"):
                    st.session_state.conversation_history = []
                    st.rerun()
            
            with col3:
                tts_enabled = st.checkbox("🔊 TTS", value=True, help="Enable text-to-speech")
                st.session_state.tts_enabled = tts_enabled
            
            st.markdown('</div>', unsafe_allow_html=True)

    def _render_chat_interface(self):
        """Render the chat interface"""
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        if st.session_state.conversation_history:
            for i, turn in enumerate(st.session_state.conversation_history):
                if turn["role"] == "doctor":
                    with st.chat_message("user", avatar="👨‍⚕️"):
                        st.write(turn["content"])
                else:
                    with st.chat_message("assistant", avatar="🤒"):
                        st.write(turn["content"])
        else:
            st.info("💡 **Getting Started:** Select a patient persona above and start the conversation by typing your message below.")
            
            # Show current persona info
            if st.session_state.current_persona:
                st.markdown(f"""
                **Current Patient:** {st.session_state.current_persona}
                
                *This virtual patient will respond based on their medical history, symptoms, and personality traits.*
                """)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def _render_input_section(self):
        """Render the input section"""
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        
        doctor_input = st.chat_input(
            "💬 Type your message as the doctor...",
            key="doctor_input"
        )
        
        if doctor_input:
            self._process_doctor_input(doctor_input)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def _process_doctor_input(self, doctor_input: str):
        """Process doctor input and generate patient response"""
        with st.spinner("🤖 Generating patient response..."):
            prompt = self.format_prompt(
                st.session_state.current_persona,
                st.session_state.conversation_history,
                doctor_input,
            )
            
            raw_response = self.query_ollama_model(
                prompt, 
                "virtual-patient"
            )
            
            # Clean the response to extract only patient content
            patient_response = self.clean_patient_response(raw_response)

            if patient_response and not patient_response.startswith("Error"):
                # Add messages to history
                st.session_state.conversation_history.append(
                    {"role": "doctor", "content": doctor_input}
                )
                st.session_state.conversation_history.append(
                    {"role": "patient", "content": patient_response}
                )
                
                # Handle TTS if enabled
                if st.session_state.get('tts_enabled', True):
                    try:
                        self.tts_engine.speak_text(patient_response)
                    except Exception as e:
                        st.warning(f"⚠️ TTS error: {e}")
                
                st.rerun()
            else:
                st.error(f"❌ Failed to generate response: {raw_response}")

    def run_app(self):
        """Main Streamlit application with Napa Valley style UI"""
        st.set_page_config(
            page_title="Virtual Patient AI",
            page_icon="🏥",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

        if "conversation_history" not in st.session_state:
            st.session_state.conversation_history = []
        if "selected_persona" not in st.session_state:
            st.session_state.selected_persona = self.available_personas[0] if self.available_personas else ""
        if "tts_enabled" not in st.session_state:
            st.session_state.tts_enabled = False

        self._inject_custom_css()

        st.markdown('<h1 class="main-header">🏥 Virtual Patient AI</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Practice medical consultations with AI patients</p>', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.chat_message("user", avatar="👨‍⚕️").write(message["content"])
            else:
                st.chat_message("assistant", avatar="🤒").write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your message as the doctor..."):
            # Add user message to display immediately
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user", avatar="👨‍⚕️").write(prompt)
            
            # Add to conversation history
            st.session_state.conversation_history.append({"role": "doctor", "content": prompt})
            
            # Get response with thinking indicator
            with st.chat_message("assistant", avatar="🤒"):
                with st.spinner("Patient is thinking..."):
                    try:
                        prompt_formatted = self.format_prompt(
                            st.session_state.current_persona,
                            st.session_state.conversation_history[:-1],  # Don't include the current message
                            prompt,
                        )
                        
                        raw_response = self.query_ollama_model(
                            prompt_formatted, 
                            "virtual-patient"
                        )
                        
                        # Clean the response
                        patient_response = self.clean_patient_response(raw_response)
                        
                        if patient_response and not patient_response.startswith("Error"):
                            st.write(patient_response)
                            
                            # Save to session state
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": patient_response
                            })
                            st.session_state.conversation_history.append({
                                "role": "patient", 
                                "content": patient_response
                            })
                            
                            # Handle TTS
                            try:
                                self.tts_engine.speak_text(patient_response)
                            except Exception as e:
                                st.warning(f"⚠️ TTS error: {e}")
                            
                            # Keep only last 20 messages for memory efficiency
                            if len(st.session_state.conversation_history) > 20:
                                st.session_state.conversation_history = st.session_state.conversation_history[-20:]
                                st.session_state.messages = st.session_state.messages[-20:]
                        else:
                            error_msg = f"Failed to generate response: {raw_response}"
                            st.error(error_msg)
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        
                    except Exception as e:
                        error_msg = f"I encountered an error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})


def main():
    app = VirtualPatientApp()
    app.run_app()


if __name__ == "__main__":
    main()