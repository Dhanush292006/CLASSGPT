import streamlit as st
import pandas as pd
import openai
from pypdf import PdfReader

st.set_page_config(page_title="AI Chat Assistant", layout="wide")

st.title("🤖 ChatGPT File Assistant")

# API KEY
api_key = st.text_input("Enter OpenAI API Key", type="password")

if api_key:
    openai.api_key = api_key

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar upload
st.sidebar.title("Upload Files")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV / TXT / PDF",
    type=["csv", "txt", "pdf"]
)

file_text = ""

# Read uploaded file
if uploaded_file:

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)
        file_text = df.to_string()

        st.sidebar.write("Dataset Preview")
        st.sidebar.dataframe(df.head())


    elif uploaded_file.name.endswith(".txt"):

        file_text = uploaded_file.read().decode()


    elif uploaded_file.name.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            file_text += page.extract_text()


# Display chat history
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Chat input
prompt = st.chat_input("Ask anything...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    if file_text != "":

        system_prompt = f"""
        Answer the question using this file data if possible.

        File Data:
        {file_text}
        """

    else:

        system_prompt = "You are a helpful AI assistant."

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response["choices"][0]["message"]["content"]

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
