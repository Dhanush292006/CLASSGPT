import streamlit as st
import pandas as pd
import re

st.title("Student Dataset Search Engine")

df = pd.read_csv("GPT DATA COLLECTION(Sheet1).csv", encoding="latin1")

query = st.text_input("Search student dataset")

if query:

    # Extract number (for roll number search)
    numbers = re.findall(r'\d+', query)
    search_term = numbers[0] if numbers else query

    # Search across ALL columns
    mask = df.apply(
        lambda row: row.astype(str).str.lower().str.contains(search_term.lower()).any(),
        axis=1
    )

    result = df[mask]

    if result.empty:
        st.write("No matching students found")

    else:
        st.subheader("Matching Students")
        st.dataframe(result)
