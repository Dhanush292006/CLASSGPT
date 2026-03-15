

import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyDFN-L5LZ1uLJ5ohts3x5hn0uf9kZ2TrdE")

model = genai.GenerativeModel("gemini-pro")

st.title("Class AI")

prompt = st.chat_input("Ask something")

if prompt:
    response = model.generate_content(prompt)
    st.write(response.text)
