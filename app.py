import streamlit as st
import google.generativeai as genai

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing Gemini API Key. Please configure it in your Streamlit Advanced Settings.")

st.title("AI Assistant Suite for DPSI")
st.write("Developed by Shashank Jangid")

tab1, tab2 = st.tabs(["🎙️ Meeting Summarizer", "✍️ Messy Note Cleaner"])

with tab1:
    st.header("Meeting Summarizer & Highlights")
    st.write("Record your live meeting or discussion. The AI will analyze the audio to generate a complete summary and extract critical action items.")
    
    audio_file = st.audio_input("Record meeting audio:", sample_rate=16000)
    
    if audio_file is not None:
        audio_bytes = audio_file.read()
        
        if st.button("Generate Meeting Summary", type="primary"):
            with st.spinner("Processing meeting audio... This might take a moment depending on length."):
                try:
                    audio_data = {
                        "mime_type": "audio/wav",
                        "data": audio_bytes
                    }
                    
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    
                    meeting_prompt = (
                        "You are an expert executive assistant. Listen carefully to the attached audio. "
                        "Provide a comprehensive, professional summary of the meeting, followed by a separate, "
                        "clearly labeled section for 'Key Highlights & Action Items' with clean bullet points."
                    )
                    
                    response = model.generate_content([meeting_prompt, audio_data])
                    
                    st.success("Analysis Complete!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Could not process audio content: {e}")

with tab2:
    st.header("Messy Note Cleaner")
    st.write("Paste your rough thoughts below, and the AI will organize them perfectly.")
    
    user_input = st.text_area("Your messy notes:", placeholder="e.g., call john at 3, fix the login bug, buy coffee...")
    
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
