import streamlit as st
import google.generativeai as genai

# Page title
st.title("AI Chatbot")

# Configure Gemini API
genai.configure(api_key="AIzaSyDFN-L5LZ1uLJ5ohts3x5hn0uf9kZ2TrdE")

model = genai.GenerativeModel("gemini-pro")

# Chat input
prompt = st.chat_input("Ask something...")

if prompt:
    st.write("You:", prompt)

    response = model.generate_content(prompt)

    st.write("AI:", response.text)
