import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("📊 Analytics Dashboard")

conn = sqlite3.connect("reviews.db")

df = pd.read_sql(
    "SELECT * FROM reviews",
    conn
)

if len(df) == 0:

    st.warning("No reviews available.")

else:

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Reviews",
        len(df)
    )

    col2.metric(
        "Average Score",
        round(df["score"].mean(), 2)
    )

    col3.metric(
        "Files Reviewed",
        df["filename"].nunique()
    )

    st.divider()

    score_chart = px.histogram(
        df,
        x="score",
        title="Score Distribution"
    )

    st.plotly_chart(
        score_chart,
        use_container_width=True
    )

    df["extension"] = (
        df["filename"]
        .str.split(".")
        .str[-1]
    )

    pie = px.pie(
        df,
        names="extension",
        title="File Types Reviewed"
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )