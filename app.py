import streamlit as st
import google.generativeai as genai

# 1. Securely fetch the API key from Streamlit's hidden cloud secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Missing Gemini API Key. Please configure it in your Streamlit Advanced Settings.")

# 2. Set up the web app interface
st.title("✍️ AI Messy Note Cleaner")
st.write("Paste your rough thoughts below, and the AI will organize them perfectly.")

# 3. Create user input box
user_input = st.text_area("Your messy notes:", placeholder="e.g., call john at 3, fix the login bug, buy coffee...")

# 4. Create a trigger button
if st.button("Clean My Notes"):
    if user_input.strip() == "":
        st.warning("Please type something first!")
    else:
        with st.spinner("AI is thinking..."):
            try:
                # 5. Using current stable production model
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                prompt = f"Take these messy notes and organize them into professional, action-oriented bullet points:\n\n{user_input}"
                response = model.generate_content(prompt)
                
                # 6. Display the result on the screen
                st.success("Here are your organized notes:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")