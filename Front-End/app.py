import streamlit as st
import requests
import json
from streamlit_mic_recorder import mic_recorder

st.set_page_config(
    page_title="AI Social Media Content Generator",
    page_icon="📱",
    layout="centered"
)


BACKEND_URL = "http://backend-server:5000"

def handle_text_input(platform):
    user_input = st.text_area("Enter your idea:", height=150)
    if st.button("Generate Content")  and user_input :
        with st.spinner(f"Generating {platform} content..."):
            data = {
                "platform": platform.lower(),
                "text_input": user_input
            }

            response = requests.post(
                f"{BACKEND_URL}/generate_content",
                data=json.dumps(data),
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                result = response.json()
                if "generated_content" in result:
                    st.subheader(f"Generated {platform} Content:")
                    st.write(result["generated_content"])
            else:
                st.error("❌ Error generating content. Please try again.")

def handle_voice_input(platform):
    user_input = None
    st.write("🎤 **Record your voice below:**")

    audio_data = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop Recording")

    if audio_data and "bytes" in audio_data:
        audio_bytes = audio_data["bytes"]
        st.audio(audio_bytes, format="audio/wav") 

        if st.button("Transcribe Audio"):
            with st.spinner("Transcribing..."):
                files = {"audio_file": ("recording.wav", audio_bytes, "audio/wav")}
                response = requests.post(f"{BACKEND_URL}/speech_to_text", files=files)

                if response.status_code == 200:
                    result = response.json()
                    if "transcription" in result:
                        user_input = result["transcription"]
                        st.success("✅ Transcription complete!")
                        st.write(f"**Transcribed text:** {user_input}")
                        with st.spinner(f"Generating {platform} content..."):
                            data = {
                                "platform": platform.lower(),
                                "text_input": user_input
                            }

                            response = requests.post(
                                f"{BACKEND_URL}/generate_content",
                                data=json.dumps(data),
                                headers={"Content-Type": "application/json"}
                            )

                            if response.status_code == 200:
                                result = response.json()
                                if "generated_content" in result:
                                    st.subheader(f"Generated {platform} Content:")
                                    st.write(result["generated_content"])
                            else:
                                st.error("❌ Error generating content. Please try again.")
                else:
                    st.error(f"❌ Error transcribing audio. Please try again. Status Code: {response.status_code}")

def main():
    st.title("AI Social Media Content Generator")
    st.write("Transform your ideas into platform-optimized social media content")
    
    platform = st.radio(
        "Select target platform:",
        ["Facebook", "Twitter", "LinkedIn"],
        horizontal=True
    )

    input_method = st.radio(
        "How would you like to input your idea?",
        ["Text", "Voice Recording"]
    )
    
    
    if input_method == "Text":
        handle_text_input(platform)
    elif input_method == "Voice Recording":
        handle_voice_input(platform)

if __name__ == "__main__":
    main()
