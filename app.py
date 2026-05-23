import streamlit as st
import google.generativeai as genai

# 1. Configure your AI API key
NEW_API_KEY = "PASTE_YOUR_NEW_SECURE_KEY_HERE"
genai.configure(api_key=NEW_API_KEY)

# App layout setup
st.title("🎙️ AI Assistant Suite")
st.write("Record a live meeting or manually clean up rough notes.")

st.write("---")
st.header("Meeting Summarizer")
st.write("Click the icon below to record your meeting audio. Once stopped, the AI will transcribe, summarize, and highlight key action items.")

# Streamlit native mic recorder widget (speech-optimized at 16000Hz)
audio_file = st.audio_input("Record your meeting audio:", sample_rate=16000)

if audio_file is not None:
    # Safely extract audio data from the widget
    audio_bytes = audio_file.read()
    
    if st.button("Generate Meeting Summary & Highlights", type="primary"):
        with st.spinner("Processing meeting audio... This can take a moment depending on the length."):
            try:
                # Wrap the audio bytes into the specific dictionary structure Gemini requires for raw media upload
                audio_data = {
                    "mime_type": "audio/wav",
                    "data": audio_bytes
                }
                
                # Initialize Gemini (2.5-flash natively understands audio files!)
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                # Craft an executive instructions prompt
                meeting_prompt = (
                    "You are an expert executive assistant. Listen carefully to the attached audio. "
                    "Provide a comprehensive, professional summary of the meeting, followed by a separate, "
                    "clearly labeled section for 'Key Highlights & Action Items' with bullet points."
                )
                
                # Send both the raw audio data and text instructions to Gemini
                response = model.generate_content([meeting_prompt, audio_data])
                
                # Display Results
                st.success("Analysis Complete!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Could not process audio: {e}")

st.write("---")
st.header("Messy Note Cleaner")

user_input = st.text_area("Your messy notes:", placeholder="e.g., call john at 3, fix the login bug...")

if st.button("Clean My Notes"):
    if user_input.strip() == "":
        st.warning("Please type something first!")
    else:
        with st.spinner("AI is thinking..."):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                prompt = f"Take these messy notes and organize them into professional, action-oriented bullet points:\n\n{user_input}"
                response = model.generate_content(prompt)
                
                st.success("Here are your organized notes:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
