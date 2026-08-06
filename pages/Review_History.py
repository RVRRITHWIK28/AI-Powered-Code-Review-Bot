import streamlit as st
import sqlite3
import pandas as pd

st.title("📜 Review History")

conn = sqlite3.connect("reviews.db")

df = pd.read_sql(
    "SELECT * FROM reviews ORDER BY id DESC",
    conn
)

search = st.text_input(
    "Search Filename"
)

if search:

    filtered = df[
        df["filename"].str.contains(
            search,
            case=False
        )
    ]

    st.dataframe(filtered)

else:

    st.dataframe(df)