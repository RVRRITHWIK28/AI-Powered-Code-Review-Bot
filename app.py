import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import pandas as pd

from review_engine import review_code
from database import (
    init_db,
    save_review,
    get_dashboard_stats,
    get_recent_reviews,
    get_all_reviews,
    get_language_stats,
    get_score_distribution,
    get_daily_reviews,
    delete_review
)
from utils import extract_score, detect_language
from report_generator import generate_pdf

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="AI-Powered Code Review Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# DATABASE
# -------------------------------------------------------

init_db()

# -------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------

defaults = {
    "page": "Home",
    "review_result": None,
    "code_score": 0,
    "uploaded_code": "",
    "file_name": "",
    "language": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------------------------------------------
# LOAD DASHBOARD STATS
# -------------------------------------------------------

stats = get_dashboard_stats()

total_reviews = stats["total_reviews"]
avg_score = stats["avg_score"]
languages = stats["languages"]
production_ready = stats["production_ready"]

# -------------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------------

st.markdown("""
<style>

/* -------------------------------------------------- */
/* Background */
/* -------------------------------------------------- */

.stApp{
background:#0F172A;
}

/* -------------------------------------------------- */
/* Main */
/* -------------------------------------------------- */

.main .block-container{
padding-top:1.8rem;
padding-left:2rem;
padding-right:2rem;
}

/* -------------------------------------------------- */
/* Sidebar */
/* -------------------------------------------------- */

section[data-testid="stSidebar"]{
background:#111827;
border-right:1px solid rgba(255,255,255,.08);
width:260px !important;
}

[data-testid="stSidebarNav"]{
display:none;
}

/* -------------------------------------------------- */
/* Buttons */
/* -------------------------------------------------- */

.stButton>button{
width:100%;
height:46px;
border-radius:12px;
border:none;
background:#1E293B;
color:white;
font-weight:600;
font-size:15px;
transition:.25s;
}

.stButton>button:hover{
background:#2563EB;
transform:translateX(4px);
}

/* -------------------------------------------------- */
/* Upload */
/* -------------------------------------------------- */

[data-testid="stFileUploader"]{

border:2px dashed #3B82F6;
border-radius:18px;
padding:18px;
background:#172033;

}

/* -------------------------------------------------- */
/* KPI CARD */
/* -------------------------------------------------- */

.metric-card{

background:linear-gradient(145deg,#1E293B,#111827);

padding:22px;

border-radius:18px;

text-align:center;

box-shadow:0 10px 30px rgba(0,0,0,.25);

transition:.30s;

}

.metric-card:hover{

transform:translateY(-6px);

box-shadow:0 14px 35px rgba(37,99,235,.35);

}

.metric-value{

font-size:38px;

font-weight:700;

color:#60A5FA;

}

.metric-title{

color:#CBD5E1;

font-size:16px;

margin-bottom:12px;

}

/* -------------------------------------------------- */
/* HERO */
/* -------------------------------------------------- */

.hero{

padding:35px;

border-radius:22px;

background:linear-gradient(135deg,#2563EB,#7C3AED);

color:white;

margin-bottom:30px;

box-shadow:0 12px 30px rgba(0,0,0,.35);

}

.hero h1{

font-size:44px;

font-weight:800;

margin-bottom:10px;

}

.hero p{

font-size:18px;

color:#E2E8F0;

}

/* -------------------------------------------------- */
/* FILE CARD */
/* -------------------------------------------------- */

.file-card{

background:#1E293B;

padding:18px;

border-radius:15px;

border:1px solid rgba(255,255,255,.08);

}

/* -------------------------------------------------- */

hr{

border:none;

height:1px;

background:#263244;

margin-top:15px;

margin-bottom:15px;

}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

with st.sidebar:

    st.markdown("""
    <h2 style="
    text-align:center;
    color:white;
    font-size:30px;
    font-weight:700;
    ">
    🤖 AI Review Bot
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🏠 Home"):
        st.session_state.page = "Home"

    if st.button("📊 Analytics"):
        st.session_state.page = "Analytics"

    if st.button("📜 Review History"):
        st.session_state.page = "Review History"

    st.markdown("---")

    st.markdown("""
    <div style="color:#CBD5E1">

    ### 🚀 Features

    1. AI Code Review

    2. Bug Detection

    3. Performance Analysis

    4. Security Scan

    5. Best Practices

    6. PDF Report

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.caption("Powered by Google Gemini")
    st.caption("Version 2.0")

# -------------------------------------------------------
# HOME PAGE
# -------------------------------------------------------

if st.session_state.page == "Home":

    st.markdown("""
    <div style="
    padding:22px 30px;
    border-radius:18px;
    background:linear-gradient(135deg,#2563EB,#7C3AED);
    color:white;
    margin-bottom:25px;
    box-shadow:0px 8px 25px rgba(0,0,0,0.35);
    ">

    <h1 style="
    margin:0;
    font-size:40px;
    font-weight:800;
    ">
    🤖 AI-Powered Code Review Bot
    </h1>

    <p style="
    margin-top:12px;
    font-size:18px;
    color:#E2E8F0;
    ">
    Analyze Python, Java, SQL, JavaScript, C and C++ source code using Google's Gemini AI.
    </p>

    <p style="
    margin-top:18px;
    font-size:17px;
    line-height:1.8;
    ">

    ✅ Detect Bugs &nbsp;&nbsp;&nbsp;
    🛡 Security Issues &nbsp;&nbsp;&nbsp;
    ⚡ Performance Optimization &nbsp;&nbsp;&nbsp;
    ⭐ Best Practices

    </p>

    </div>
    """, unsafe_allow_html=True)

    # ==========================================================
    # Upload Section
    # ==========================================================

    st.markdown("""
    <h2 style="color:white;">
    📂 Upload Your Source Code
    </h2>

    <p style="color:#94A3B8;font-size:16px;">
    Upload a supported source code file and let Gemini AI perform
    a professional code review.
    </p>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "",
        type=["py", "java", "sql", "js", "cpp", "c"],
        help="Supported: Python, Java, SQL, JavaScript, C, C++"
    )

    if uploaded_file:

        try:

            code = uploaded_file.read().decode("utf-8")

            language = detect_language(uploaded_file.name)

            st.session_state.uploaded_code = code
            st.session_state.file_name = uploaded_file.name
            st.session_state.language = language

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="file-card">

            <h3 style="color:white;margin-bottom:15px;">
            📄 File Information
            </h3>

            <b>Filename :</b> {uploaded_file.name}<br><br>

            <b>Language :</b> {language}<br><br>

            <b>Size :</b> {uploaded_file.size/1024:.2f} KB<br><br>

            <b>Lines :</b> {len(code.splitlines())}

            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <h3 style="color:white;">
            💻 Source Code Preview
            </h3>
            """, unsafe_allow_html=True)

            st.code(
                code,
                language=language.lower(),
                line_numbers=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button(
                "🚀 Analyze with Gemini AI",
                use_container_width=True
            ):

                progress = st.progress(0)

                status = st.empty()

                for i in range(100):

                    progress.progress(i + 1)

                    if i < 25:
                        status.info("📄 Reading source code...")

                    elif i < 50:
                        status.info("🔍 Detecting issues...")

                    elif i < 75:
                        status.info("🧠 Gemini AI is analyzing...")

                    else:
                        status.info("📊 Preparing review report...")

                    import time
                    time.sleep(0.01)

                with st.spinner("Generating AI Review..."):

                    review = review_code(code)

                    if "quota exceeded" in review.lower() or "resource_exhausted" in review.lower():

                        st.error(review)

                        st.stop()

                    score = extract_score(review)

                    save_review(
                        uploaded_file.name,
                        language,
                        score,
                        review
                    )

                    st.session_state.review_result = review
                    st.session_state.code_score = score

                progress.empty()

                status.success("✅ Review Completed Successfully!")

        except Exception as e:

            st.error(f"Error: {e}")
    # ==========================================================
    # REVIEW RESULTS
    # ==========================================================

    if st.session_state.review_result:

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <h2 style="color:white;">
        📊 Review Summary
        </h2>
        """, unsafe_allow_html=True)

        score = st.session_state.code_score

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "⭐ Code Score",
                f"{score}/100"
            )

        with col2:

            if score >= 80:
                st.success("🚀 Production Ready")

            elif score >= 60:
                st.warning("⚠ Needs Improvements")

            else:
                st.error("❌ Major Issues")

        with col3:
            st.metric(
                "💻 Language",
                st.session_state.language
            )

        with col4:
            st.metric(
                "📄 Lines of Code",
                len(st.session_state.uploaded_code.splitlines())
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("📈 Code Quality")

        st.progress(score / 100)

        if score >= 90:
            st.success("Excellent code quality.")

        elif score >= 75:
            st.info("Good implementation with minor improvements.")

        elif score >= 60:
            st.warning("Moderate quality. Improvements recommended.")

        else:
            st.error("Poor code quality. Significant improvements required.")

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander(
            "📋 AI Review Report",
            expanded=True
        ):
            st.markdown(st.session_state.review_result)

        st.markdown("<br>", unsafe_allow_html=True)

        try:

            pdf_file = generate_pdf(
                st.session_state.review_result
            )

            with open(pdf_file, "rb") as pdf:

                st.download_button(

                    label="📄 Download PDF Report",

                    data=pdf,

                    file_name="AI_Code_Review_Report.pdf",

                    mime="application/pdf",

                    use_container_width=True

                )

        except Exception as e:

            st.warning(
                f"Unable to generate PDF: {e}"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        ---
        <center>

        <span style="color:#94A3B8;">

        🤖 AI-Powered Code Review Bot

        <br>

        Powered by Google Gemini AI • Streamlit • SQLite

        </span>

        </center>
        """, unsafe_allow_html=True)


    # ==========================================================
    # ANALYTICS PAGE
    # ==========================================================

elif st.session_state.page == "Analytics":

        st.markdown("""
        <div class="hero">
            <h1>📊 Analytics Dashboard</h1>
            <p>
                View insights and trends from all AI-powered code reviews.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # -----------------------------------------
        # Dashboard Statistics
        # -----------------------------------------

        stats = get_dashboard_stats()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "📄 Total Reviews",
                stats["total_reviews"]
            )

        with col2:
            st.metric(
                "⭐ Average Score",
                f'{stats["avg_score"]}/100'
            )

        with col3:
            st.metric(
                "🌍 Languages",
                stats["languages"]
            )

        with col4:
            st.metric(
                "🚀 Production Ready",
                stats["production_ready"]
            )

        st.markdown("---")

        # -----------------------------------------
        # Daily Review Trend
        # -----------------------------------------

        st.subheader("📈 Daily Review Trend")

        daily_reviews = get_daily_reviews()

        if daily_reviews:

            df_daily = pd.DataFrame(
                daily_reviews,
                columns=[
                    "Date",
                    "Reviews"
                ]
            )

            fig = px.line(
                df_daily,
                x="Date",
                y="Reviews",
                markers=True,
                title="Reviews Submitted Per Day"
            )

            fig.update_layout(
                template="plotly_dark",
                height=450,
                xaxis_title="Date",
                yaxis_title="Reviews"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No review data available yet.")

        st.markdown("---")

        # -----------------------------------------
        # Reviews by Language
        # -----------------------------------------

        st.subheader("🌍 Reviews by Programming Language")

        language_stats = get_language_stats()

        if language_stats:

            df_language = pd.DataFrame(
                language_stats,
                columns=[
                    "Language",
                    "Reviews"
                ]
            )

            pie_chart = px.pie(
                df_language,
                names="Language",
                values="Reviews",
                hole=0.45,
                title="Programming Language Distribution"
            )

            pie_chart.update_layout(
                template="plotly_dark",
                height=500
            )

            st.plotly_chart(
                pie_chart,
                use_container_width=True
            )

        else:

            st.info("Language statistics not available.")

        # -----------------------------------------
        # Score Distribution
        # -----------------------------------------

        st.markdown("---")

        st.subheader("📊 Code Score Distribution")

        score_data = get_score_distribution()

        if score_data:

            df_score = pd.DataFrame(
                score_data,
                columns=[
                    "Score Range",
                    "Reviews"
                ]
            )

            bar_chart = px.bar(
                df_score,
                x="Score Range",
                y="Reviews",
                text="Reviews",
                title="Distribution of Review Scores"
            )

            bar_chart.update_layout(
                template="plotly_dark",
                height=450,
                xaxis_title="Score Range",
                yaxis_title="Number of Reviews"
            )

            bar_chart.update_traces(
                textposition="outside"
            )

            st.plotly_chart(
                bar_chart,
                use_container_width=True
            )

        else:

            st.info("No score distribution available.")

        # -----------------------------------------
        # Recent Reviews
        # -----------------------------------------

        st.markdown("---")

        st.subheader("📋 Recent Reviews")

        recent_reviews = get_recent_reviews()

        if recent_reviews:

            df_recent = pd.DataFrame(
                recent_reviews,
                columns=[
                    "Filename",
                    "Language",
                    "Score",
                    "Reviewed At"
                ]
            )

            st.dataframe(
                df_recent,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No reviews available.")

        # -----------------------------------------
        # Dashboard Summary
        # -----------------------------------------

        st.markdown("---")

        avg = stats["avg_score"]

        if avg >= 90:

            st.success(
                "🏆 Excellent overall code quality across reviewed projects."
            )

        elif avg >= 75:

            st.info(
                "👍 Overall code quality is good. Minor improvements are recommended."
            )

        elif avg >= 60:

            st.warning(
                "⚠ Code quality is average. More optimization and best practices are recommended."
            )

        else:

            st.error(
                "🚨 Most reviewed projects require significant improvements."
            )

        # -----------------------------------------
        # Footer
        # -----------------------------------------

        st.markdown("""
        <br><br>

        <center>

        <span style="color:#94A3B8;">

        📊 Analytics generated from SQLite review database

        <br>

        Powered by Plotly • Streamlit • Gemini AI

        </span>

        </center>
        """, unsafe_allow_html=True)



# ==========================================================
# REVIEW HISTORY PAGE
# ==========================================================

elif st.session_state.page == "Review History":

    st.markdown("""
    <div class="hero">
        <h1>📜 Review History</h1>
        <p>Browse, search, and manage all AI-generated code reviews.</p>
    </div>
    """, unsafe_allow_html=True)

    # Fetch reviews from database
    reviews = get_all_reviews()

    # -----------------------------------------
    # NO REVIEWS
    # -----------------------------------------

    if not reviews:

        st.info("📭 No reviews found in the database.")

    # -----------------------------------------
    # REVIEWS EXIST
    # -----------------------------------------

    else:

        # THIS CREATES df
        df = pd.DataFrame(
            reviews,
            columns=[
                "ID",
                "Filename",
                "Language",
                "Score",
                "Review",
                "Created At"
            ]
        )

        # Search
        search = st.text_input(
            "🔍 Search by Filename",
            placeholder="Example: main.py"
        )

        if search:

            df = df[
                df["Filename"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.markdown("<br>", unsafe_allow_html=True)

        # -----------------------------------------
        # Summary
        # -----------------------------------------

        if not df.empty:

            total_count = len(df)
            average_score = round(df["Score"].mean(), 1)
            highest_score = int(df["Score"].max())
            lowest_score = int(df["Score"].min())

        else:

            total_count = 0
            average_score = 0
            highest_score = 0
            lowest_score = 0

        st.subheader("📈 Review Summary")

        s1, s2, s3, s4 = st.columns(4)

        with s1:
            st.metric(
                "📄 Total Reviews",
                total_count
            )

        with s2:
            st.metric(
                "⭐ Average Score",
                f"{average_score}/100"
            )

        with s3:
            st.metric(
                "🏆 Highest Score",
                f"{highest_score}/100"
            )

        with s4:
            st.metric(
                "📉 Lowest Score",
                f"{lowest_score}/100"
            )

        st.markdown("---")

        # -----------------------------------------
        # Saved Reviews
        # -----------------------------------------

        st.subheader("📂 Saved Reviews")

        if df.empty:

            st.warning(
                "No reviews match your search."
            )

        else:

            for _, row in df.iterrows():

                c1, c2, c3, c4 = st.columns(
                    [3, 2, 1.5, 2]
                )

                with c1:
                    st.markdown(
                        f"**📄 {row['Filename']}**"
                    )

                with c2:
                    st.write(
                        f"💻 {row['Language']}"
                    )

                with c3:

                    score = int(row["Score"])

                    if score >= 80:
                        st.success(f"{score}/100")

                    elif score >= 60:
                        st.warning(f"{score}/100")

                    else:
                        st.error(f"{score}/100")

                with c4:
                    st.caption(
                        str(row["Created At"])
                    )

                # Full AI Review
                with st.expander(
                    f"📋 View AI Review — {row['Filename']}"
                ):

                    st.markdown(
                        row["Review"]
                    )

                # Delete
                delete_left, delete_right = st.columns(
                    [6, 1]
                )

                with delete_right:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{row['ID']}"
                    ):

                        delete_review(
                            int(row["ID"])
                        )

                        st.success(
                            "Review deleted successfully!"
                        )

                        st.rerun()

                st.markdown("---")

        # -----------------------------------------
        # Table
        # -----------------------------------------

        if not df.empty:

            st.subheader("📊 Review Records")

            table_df = df.drop(
                columns=["Review"]
            )

            st.dataframe(
                table_df,
                use_container_width=True,
                hide_index=True
            )

        # -----------------------------------------
        # Footer
        # -----------------------------------------

        st.markdown("""
        <br><br>

        <center>

        <span style="color:#94A3B8;">

        📜 Review History powered by SQLite

        <br>

        AI Review Bot • Streamlit • Gemini AI

        </span>

        </center>
        """, unsafe_allow_html=True)