import streamlit as st
import pandas as pd
import re

# Page title
st.title("Student Dataset Search Engine")

# Load dataset
df = pd.read_csv("clean_student_dataset (1).csv")

# Search box
query = st.text_input("Search student dataset")

if query:

    q = query.lower()

    # Case 1: Students with no internship experience
    if "internship" in q and ("no" in q or "none" in q):

        result = df[
            df["Internship Experience"]
            .astype(str)
            .str.lower()
            .isin(["none", "no", "nil", "nan", ""])
        ]

    else:

        # Detect roll number
        numbers = re.findall(r'\d+', q)

        if numbers:
            roll = numbers[0]
            result = df[df["Student ID"].astype(str).str.contains(roll)]

        else:
            # General keyword search
            mask = df.apply(
                lambda row: row.astype(str).str.lower().str.contains(q).any(),
                axis=1
            )
            result = df[mask]

    # Show results
    if result.empty:
        st.warning("No matching students found")
    else:
        st.success(f"{len(result)} student(s) found")
        st.dataframe(result, use_container_width=True)
