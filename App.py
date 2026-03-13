import streamlit as st
import pandas as pd
import openai

st.set_page_config(page_title="ChatGPT Clone", layout="wide")

st.title("🤖 AI Chat Assistant")

# API Key
api_key = st.text_input("Enter OpenAI API Key", type="password")

if api_key:
    openai.api_key = api_key

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar file upload
st.sidebar.title("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

data = None

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.sidebar.write("Dataset Preview")
    st.sidebar.dataframe(data.head())

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask anything...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # If CSV uploaded → answer from dataset
    if data is not None:

        dataset_text = data.to_string()

        system_prompt = f"""
        You are a data assistant.
        Answer the question using this dataset if possible.

        Dataset:
        {dataset_text}
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

    reply = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
