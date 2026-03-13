import streamlit as st
import pandas as pd
import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.schema import Document
from langchain.chains import RetrievalQA


st.set_page_config(page_title="ChatGPT File Assistant")

st.title("🤖 ChatGPT File Assistant")

# API key
api_key = st.text_input("Enter OpenAI API Key", type="password")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

# Upload files
uploaded_files = st.file_uploader(
    "Upload CSV / PDF / TXT",
    type=["csv", "pdf", "txt"],
    accept_multiple_files=True
)

documents = []

if uploaded_files:

    for file in uploaded_files:

        if file.name.endswith(".csv"):

            df = pd.read_csv(file)
            documents.append(Document(page_content=df.to_string()))

        elif file.name.endswith(".txt"):

            text = file.read().decode()
            documents.append(Document(page_content=text))

        elif file.name.endswith(".pdf"):

            with open(file.name, "wb") as f:
                f.write(file.getbuffer())

            loader = PyPDFLoader(file.name)
            documents.extend(loader.load())


# Create vector DB
if documents and api_key:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(docs, embeddings)

    retriever = vectorstore.as_retriever()

    llm = ChatOpenAI(model="gpt-4o-mini")

    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)


# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Chat input
prompt = st.chat_input("Ask something...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    if documents:

        try:
            response = qa.run(prompt)
        except:
            response = llm.invoke(prompt).content

    else:
        response = llm.invoke(prompt).content


    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
