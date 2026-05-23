import streamlit as st
import google.generativeai as genai

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Missing Gemini API Key. Please configure it in your Streamlit Advanced Settings.")

st.title("AI Messy Note Cleaner for DPSI")
st.write("Paste your rough thoughts below, and the AI will organize them perfectly, by Shashank Jangid")

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
