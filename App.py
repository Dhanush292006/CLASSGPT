import streamlit as st
import pandas as pd
import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.schema import Document
from langchain.chains import RetrievalQA

st.title("📂 LLM File Chatbot")

st.write("Upload CSV, PDF or TXT files and ask questions")

# API Key
api_key = st.text_input("Enter OpenAI API Key", type="password")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key


# File uploader
uploaded_files = st.file_uploader(
    "Upload files",
    type=["csv", "pdf", "txt"],
    accept_multiple_files=True
)


if uploaded_files and api_key:

    documents = []

    for file in uploaded_files:

        if file.name.endswith(".csv"):

            df = pd.read_csv(file)
            text = df.to_string()
            documents.append(Document(page_content=text))


        elif file.name.endswith(".txt"):

            with open(file.name, "wb") as f:
                f.write(file.getbuffer())

            loader = TextLoader(file.name)
            documents.extend(loader.load())


        elif file.name.endswith(".pdf"):

            with open(file.name, "wb") as f:
                f.write(file.getbuffer())

            loader = PyPDFLoader(file.name)
            documents.extend(loader.load())


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(docs, embeddings)

    retriever = vectorstore.as_retriever()

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )

    question = st.text_input("Ask a question")

    if question:

        try:

            answer = qa.run(question)

            st.success(answer)

        except:

            response = llm.invoke(question)

            st.success(response.content)
