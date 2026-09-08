import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
import pandas as pd

from review_engine import review_code, generate_improved_code
from project_knowledge import (
    get_relevant_categories,
    get_project_knowledge
)
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
    "language": "",
    "improved_code_result": None
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
                language=st.session_state.language.lower(),
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
                    relevant_categories = get_relevant_categories(code)

                    retrieved_knowledge = get_project_knowledge(
                        relevant_categories
                    )

                    review = review_code(
                        code,
                        return_retrieval=True
                    )

                    retrieved_results = review.pop(
                        "_retrieved_knowledge",
                        []
                    )

                with st.expander("🧠 Semantic Retrieval"):

                    st.write("**Top Retrieved Project Rules:**")

                    for i, result in enumerate(
                        retrieved_results,
                        start=1
                    ):

                        st.markdown(
                            f"### {i}. {result['category'].title()}"
                        )

                        st.write(
                            f"**Semantic Similarity:** "
                            f"{result['similarity']:.4f}"
                        )

                        st.write(
                            f"**Hybrid Score:** "
                            f"{result['score']:.4f}"
                        )

                        st.info(
                            f"📚 {result['rule']}"
                        )

                        st.markdown("---")

                    if "error" in review:
                        st.error(review["error"])
                        st.stop()

                    score = review["score"]

                    save_review(
                        uploaded_file.name,
                        language,
                        score,
                        json.dumps(review, indent=2)
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

    if st.session_state.review_result is not None:

        review = st.session_state.review_result

        if not isinstance(review, dict):
            st.error("Invalid review format returned by AI.")
            st.stop()

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <h2 style="color:white;">
        📊 Review Summary
        </h2>
        """, unsafe_allow_html=True)

        score = st.session_state.code_score

        # ----------------------------------------------------------
        # REVIEW SUMMARY METRICS
        # ----------------------------------------------------------

        all_issues = []

        for category in [
            "bugs",
            "security",
            "performance",
            "best_practices"
        ]:
            all_issues.extend(
                review.get(category, [])
            )

        critical_count = sum(
            1 for issue in all_issues
            if issue.get("severity") == "CRITICAL"
        )

        high_count = sum(
            1 for issue in all_issues
            if issue.get("severity") == "HIGH"
        )

        medium_count = sum(
            1 for issue in all_issues
            if issue.get("severity") == "MEDIUM"
        )

        low_count = sum(
            1 for issue in all_issues
            if issue.get("severity") == "LOW"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "⭐ Code Score",
                f"{score}/100"
            )

        with col2:
            st.metric(
                "🔴 Critical",
                critical_count
            )

        with col3:
            st.metric(
                "🟠 High",
                high_count
            )

        with col4:
            st.metric(
                "🟡 Medium",
                medium_count
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Additional low-severity information
        if low_count > 0:
            st.info(f"🟢 Low Severity Issues: {low_count}")

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("📈 Code Quality")

        # Score visualization
        score_col1, score_col2 = st.columns([1, 2])

        with score_col1:

            st.metric(
                "Overall Score",
                f"{score}/100"
            )

        with score_col2:

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

        # ==========================================================
        # SEVERITY DISTRIBUTION
        # ==========================================================

        st.subheader("📊 Severity Distribution")

        severity_data = pd.DataFrame({
            "Severity": [
                "Critical",
                "High",
                "Medium",
                "Low"
            ],
            "Issues": [
                critical_count,
                high_count,
                medium_count,
                low_count
            ]
        })

        fig = px.bar(
            severity_data,
            x="Severity",
            y="Issues",
            text="Issues",
            title="Issues by Severity"
        )

        fig.update_layout(
            xaxis_title="Severity",
            yaxis_title="Number of Issues",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ==========================================================
        # CATEGORY-WISE ISSUE DISTRIBUTION
        # ==========================================================

        st.subheader("📂 Issues by Category")

        category_data = pd.DataFrame({
            "Category": [
                "Bugs",
                "Security",
                "Performance",
                "Best Practices"
            ],
            "Issues": [
                len(review.get("bugs", [])),
                len(review.get("security", [])),
                len(review.get("performance", [])),
                len(review.get("best_practices", []))
            ]
        })

        fig_category = px.bar(
            category_data,
            x="Category",
            y="Issues",
            text="Issues",
            title="Issues Detected by Category"
        )

        fig_category.update_layout(
            xaxis_title="Category",
            yaxis_title="Number of Issues",
            showlegend=False
        )

        st.plotly_chart(
            fig_category,
            width="stretch"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ==========================================================
        # RAG / PROJECT KNOWLEDGE
        # ==========================================================

        retrieved_knowledge = review.get(
            "_retrieved_knowledge",
            []
        )

        if retrieved_knowledge:

            st.subheader("🧠 Project Knowledge Used")

            st.caption(
                "These project-specific rules were retrieved "
                "and provided as context during the AI review."
            )

            for index, item in enumerate(
                retrieved_knowledge,
                start=1
            ):

                category = item.get(
                    "category",
                    "Unknown"
                )

                rule = item.get(
                    "rule",
                    ""
                )

                similarity = item.get(
                    "similarity",
                    0
                )

                hybrid_score = item.get(
                    "score",
                    0
                )

                with st.expander(
                    f"{index}. {category.replace('_', ' ').title()}"
                ):

                    st.write(
                        f"**Rule:** {rule}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Semantic Similarity",
                            f"{similarity:.3f}"
                        )

                    with col2:

                        st.metric(
                            "Hybrid Score",
                            f"{hybrid_score:.3f}"
                        )

            st.markdown("<br>", unsafe_allow_html=True)

        # ==========================================================
        # STRUCTURED AI REVIEW
        # ==========================================================

        review = st.session_state.review_result

        # ==========================================================
        # ISSUE FILTERS
        # ==========================================================

        st.subheader("🔎 Filter Issues")

        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:

            selected_category = st.selectbox(
                "Category",
                [
                    "All",
                    "Bugs",
                    "Security",
                    "Performance",
                    "Best Practices"
                ]
            )

        with filter_col2:

            selected_severity = st.selectbox(
                "Severity",
                [
                    "All",
                    "CRITICAL",
                    "HIGH",
                    "MEDIUM",
                    "LOW"
                ]
            )

        # Collect all issues
        filtered_issues = []

        category_mapping = {
            "Bugs": "bugs",
            "Security": "security",
            "Performance": "performance",
            "Best Practices": "best_practices"
        }

        categories_to_check = (
            [category_mapping[selected_category]]
            if selected_category != "All"
            else [
                "bugs",
                "security",
                "performance",
                "best_practices"
            ]
        )

        for category in categories_to_check:

            for issue in review.get(category, []):

                if (
                    selected_severity == "All"
                    or issue.get("severity") == selected_severity
                ):

                    filtered_issues.append({
                        "category": category,
                        "issue": issue
                    })

        st.caption(
            f"Showing {len(filtered_issues)} matching issue(s)"
        )

        # ==========================================================
        # REVIEW STATUS
        # ==========================================================

        if len(all_issues) == 0:

            st.success(
                "✅ No issues were detected. "
                "Your code passed the AI review."
            )

        elif critical_count > 0:

            st.error(
                f"🚨 Review requires attention: "
                f"{critical_count} critical issue(s) detected."
            )

        elif high_count > 0:

            st.warning(
                f"⚠️ Review requires attention: "
                f"{high_count} high-severity issue(s) detected."
            )

        else:

            st.info(
                "ℹ️ Minor improvements are recommended."
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ==========================================================
        # FILTERED ISSUE RESULTS
        # ==========================================================

        if not filtered_issues:

            st.success("🎉 No issues match the selected filters.")

        else:

            for item in filtered_issues:

                category = item["category"]
                issue = item["issue"]

                # Category heading
                if category == "bugs":
                    category_label = "🐛 Bug"

                elif category == "security":
                    category_label = "🔐 Security"

                elif category == "performance":
                    category_label = "⚡ Performance"

                else:
                    category_label = "📋 Best Practice"

                severity = issue.get("severity", "UNKNOWN")
                confidence = issue.get("confidence", 0)

                with st.expander(
                    f"{category_label} — {severity}",
                    expanded=True
                ):

                    st.markdown(
                        f"### {issue.get('issue', 'Issue detected')}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        if severity == "CRITICAL":
                            st.error("🔴 CRITICAL")

                        elif severity == "HIGH":
                            st.warning("🟠 HIGH")

                        elif severity == "MEDIUM":
                            st.info("🟡 MEDIUM")

                        else:
                            st.success("🟢 LOW")

                    with col2:

                        st.metric(
                            "🤖 AI Confidence",
                            f"{confidence}%"
                        )

                    if issue.get("evidence"):

                        st.markdown("**🔎 Evidence**")

                        st.code(
                            issue["evidence"],
                            language=st.session_state.language.lower()
                        )

                    if issue.get("explanation"):

                        st.markdown("**💡 Explanation**")

                        st.write(
                            issue["explanation"]
                        )

                    if issue.get("suggestion"):

                        st.markdown("**🛠️ Suggested Fix**")

                        st.info(
                            issue["suggestion"]
                        )
        # ==========================================================
        # V2.6 — AI-GENERATED IMPROVED CODE
        # ==========================================================

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            "**✨ AI-Generated Improved Code**"
        )

        st.caption(
            "Generate an improved version of the submitted code "
            "based on the validated AI review findings."
        )

        if st.button(
            "✨ Generate Improved Code",
            key="generate_improved_code",
            use_container_width=True
        ):

            with st.spinner(
                "🧠 Gemini is generating the improved code..."
            ):

                improved_result = generate_improved_code(
                    st.session_state.uploaded_code,
                    review,
                    st.session_state.language
                )

            st.session_state.improved_code_result = improved_result


        # ==========================================================
        # DISPLAY IMPROVED CODE
        # ==========================================================

        improved_result = st.session_state.improved_code_result

        if improved_result:

            if "error" in improved_result:

                st.error(
                    improved_result["error"]
                )

            else:

                improved_code = improved_result.get(
                    "improved_code",
                    ""
                )

                changes = improved_result.get(
                    "changes",
                    []
                )

                st.success(
                    "✅ Improved code generated successfully!"
                )

                # --------------------------------------------------
                # Original vs Improved Code
                # --------------------------------------------------

                original_col, improved_col = st.columns(2)

                with original_col:

                    st.markdown(
                        "**📄 Original Code**"
                    )

                    st.code(
                        st.session_state.uploaded_code,
                        language=st.session_state.language.lower(),
                        line_numbers=True
                    )

                with improved_col:

                    st.markdown(
                        "**✨ Improved Code**"
                    )

                    st.code(
                        improved_code,
                        language=st.session_state.language.lower(),
                        line_numbers=True
                    )

                # --------------------------------------------------
                # Download Improved Code
                # --------------------------------------------------

                st.download_button(
                    label="⬇️ Download Improved Code",
                    data=improved_code,
                    file_name=f"improved_{st.session_state.file_name}",
                    mime="text/plain",
                    use_container_width=True,
                    key="download_improved_code"
                )

                # --------------------------------------------------
                # Changes Made
                # --------------------------------------------------

                if changes:

                    st.markdown(
                        "**📝 Changes Made**"
                    )

                    for change in changes:

                        st.markdown(
                            f"- {change}"
                        )


        # ==========================================================
        # PDF REPORT
        # ==========================================================

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

        # ==========================================================
        # REVIEW HISTORY FILTERS
        # ==========================================================

        filter_col1, filter_col2, filter_col3 = st.columns(3)

        with filter_col1:

            search = st.text_input(
                "🔍 Search by Filename",
                placeholder="Example: main.py"
            )

        with filter_col2:

            languages = ["All"] + sorted(
                df["Language"]
                .dropna()
                .unique()
                .tolist()
            )

            selected_language = st.selectbox(
                "💻 Programming Language",
                languages
            )

        with filter_col3:

            score_filter = st.selectbox(
                "⭐ Score Range",
                [
                    "All",
                    "90–100",
                    "75–89",
                    "60–74",
                    "0–59"
                ]
            )

        # ----------------------------------------------------------
        # Apply filename filter
        # ----------------------------------------------------------

        if search:

            df = df[
                df["Filename"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        # ----------------------------------------------------------
        # Apply language filter
        # ----------------------------------------------------------

        if selected_language != "All":

            df = df[
                df["Language"] == selected_language
            ]

        # ----------------------------------------------------------
        # Apply score filter
        # ----------------------------------------------------------

        if score_filter == "90–100":

            df = df[
                df["Score"].between(90, 100)
            ]

        elif score_filter == "75–89":

            df = df[
                df["Score"].between(75, 89)
            ]

        elif score_filter == "60–74":

            df = df[
                df["Score"].between(60, 74)
            ]

        elif score_filter == "0–59":

            df = df[
                df["Score"].between(0, 59)
            ]
        # ==========================================================
        # SORT REVIEW HISTORY
        # ==========================================================

        sort_option = st.selectbox(
            "↕️ Sort Reviews",
            [
                "Newest First",
                "Oldest First",
                "Highest Score",
                "Lowest Score"
            ]
        )

        if sort_option == "Newest First":

            df = df.sort_values(
                by="Created At",
                ascending=False
            )

        elif sort_option == "Oldest First":

            df = df.sort_values(
                by="Created At",
                ascending=True
            )

        elif sort_option == "Highest Score":

            df = df.sort_values(
                by="Score",
                ascending=False
            )

        elif sort_option == "Lowest Score":

            df = df.sort_values(
                by="Score",
                ascending=True
            )

        st.caption(
            f"Showing {len(df)} review(s)"
        )

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

                    try:

                        review = json.loads(row["Review"])

                        # ----------------------------------------------------------
                        # Issue Severity Summary
                        # ----------------------------------------------------------

                        all_issues = []

                        for category in [
                            "bugs",
                            "security",
                            "performance",
                            "best_practices"
                        ]:

                            all_issues.extend(
                                review.get(category, [])
                            )

                        critical = sum(
                            1 for issue in all_issues
                            if issue.get("severity") == "CRITICAL"
                        )

                        high = sum(
                            1 for issue in all_issues
                            if issue.get("severity") == "HIGH"
                        )

                        medium = sum(
                            1 for issue in all_issues
                            if issue.get("severity") == "MEDIUM"
                        )

                        low = sum(
                            1 for issue in all_issues
                            if issue.get("severity") == "LOW"
                        )

                        st.markdown(
                            f"**Issues:** "
                            f"🔴 {critical} Critical  |  "
                            f"🟠 {high} High  |  "
                            f"🟡 {medium} Medium  |  "
                            f"🟢 {low} Low"
                        )

                        # -----------------------------
                        # Score
                        # -----------------------------

                        review_score = review.get("score", row["Score"])

                        st.metric(
                            "⭐ Code Quality Score",
                            f"{review_score}/100"
                        )

                        st.markdown("---")

                        # -----------------------------
                        # Review Sections
                        # -----------------------------

                        sections = [
                            ("🐛 Bugs", "bugs"),
                            ("🛡 Security", "security"),
                            ("⚡ Performance", "performance"),
                            ("⭐ Best Practices", "best_practices")
                        ]

                        for section_title, section_key in sections:

                            st.markdown(
                                f"### {section_title}"
                            )

                            issues = review.get(
                                section_key,
                                []
                            )

                            if not issues:

                                st.success(
                                    "No issues found."
                                )

                            else:

                                for index, issue in enumerate(
                                    issues,
                                    start=1
                                ):

                                    severity = issue.get(
                                        "severity",
                                        "UNKNOWN"
                                    )

                                    confidence = issue.get(
                                        "confidence",
                                        0
                                    )

                                    st.markdown(
                                        f"**Issue {index} — {severity}**"
                                    )

                                    st.write(
                                        f"**Confidence:** {confidence}"
                                    )

                                    st.write(
                                        f"**Issue:** {issue.get('issue', '')}"
                                    )

                                    # Evidence
                                    if issue.get("evidence"):

                                        st.markdown(
                                            "**🔎 Evidence from Source Code**"
                                        )

                                        st.code(
                                            issue["evidence"]
                                        )

                                    # Explanation
                                    st.write(
                                        f"**Explanation:** "
                                        f"{issue.get('explanation', '')}"
                                    )

                                    # Suggested fix
                                    st.info(
                                        f"💡 **Suggestion:** "
                                        f"{issue.get('suggestion', '')}"
                                    )

                                    st.markdown("---")

                    except Exception:

                        # Backward compatibility for older reviews
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