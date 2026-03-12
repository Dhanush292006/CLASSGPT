import streamlit as st
import pandas as pd
import re

st.title("Student Dataset Search Engine")

# Load dataset
df = pd.read_csv("clean_student_dataset.csv(1)")

# Search box
query = st.text_input("Search student dataset")

if query:

    query = query.lower()

    # Extract numbers (for roll number search)
    numbers = re.findall(r'\d+', query)

    if numbers:
        roll = numbers[0]
        result = df[df["Student ID"].astype(str).str.contains(roll)]

    else:
        # Search across all columns
        mask = df.apply(
            lambda row: row.astype(str).str.lower().str.contains(query).any(),
            axis=1
        )
        result = df[mask]

    if result.empty:
        st.write("No matching students found")
    else:
        st.write("Matching Students")
        st.dataframe(result)
