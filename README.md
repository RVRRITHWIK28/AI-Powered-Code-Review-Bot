# 🤖 AI-Powered Code Review Bot

An AI-powered code review application that analyzes source code using **Google Gemini**, retrieves project-specific coding knowledge using **RAG and embeddings**, validates AI-generated evidence to reduce unsupported findings, and presents the results through an interactive **Streamlit dashboard**.

### 🚀 Live Demo

👉 **[AI-Powered Code Review Bot · Streamlit](https://rvrrithwik28aipoweredcodereviewbot.streamlit.app/)**

---

## 📌 Overview

The **AI-Powered Code Review Bot** is a full-stack GenAI application designed to automate and improve the code review process.

Users can submit source code and receive a structured review covering:

* 🐛 Bugs
* 🔐 Security vulnerabilities
* ⚡ Performance issues
* 📋 Best practices
* 🎯 Severity
* 🤖 AI confidence
* 🔎 Evidence from the submitted source code
* 🛠️ Recommended fixes

The application combines **LLM-based code analysis, Retrieval-Augmented Generation (RAG), embedding-based retrieval, evidence validation, SQLite persistence, PDF reporting, and an interactive Streamlit interface**.

---

## ✨ Key Features

### 🧠 AI-Powered Code Review

Uses **Google Gemini** to analyze submitted source code and return structured review results.

The model evaluates:

* Bugs
* Security
* Performance
* Best practices
* Overall code quality

The review is returned using a structured JSON schema rather than relying on unstructured text generation.

---

### 🎯 Severity & Confidence

Every detected issue can include:

| Field       | Description                    |
| ----------- | ------------------------------ |
| Severity    | LOW, MEDIUM, HIGH, or CRITICAL |
| Confidence  | AI confidence score            |
| Issue       | Description of the problem     |
| Evidence    | Code demonstrating the issue   |
| Explanation | Why the issue matters          |
| Suggestion  | Recommended improvement        |

This makes the output easier to interpret and process programmatically.

---

### 🔎 Evidence Validation

The system doesn't blindly trust every AI-generated finding.

For each detected issue, the application checks whether the supplied evidence actually exists in the submitted source code.

The validation process supports:

* Exact evidence matching
* Normalized whitespace matching
* Removal of unsupported findings

This helps reduce **false positives and hallucinated evidence**.

---

### 🧠 RAG / Project Knowledge

The application includes a project-specific knowledge base containing coding guidelines for areas such as:

* Security
* Performance
* Best practices
* Code quality

Knowledge items are converted into embeddings using **Gemini Embeddings**.

The system retrieves relevant knowledge using:

1. Query embedding generation
2. Document embeddings
3. Cosine similarity
4. Category-aware ranking
5. Hybrid retrieval scoring

This allows the review engine to use project-specific rules instead of relying exclusively on the model's general knowledge.

---

### 📊 Interactive Streamlit Dashboard

The application provides an interactive dashboard containing:

* ⭐ Overall code quality score
* 🔴 Critical issue count
* 🟠 High issue count
* 🟡 Medium issue count
* 🟢 Low issue count
* 📈 Code quality visualization
* 📊 Severity distribution
* 📂 Category-wise issue distribution
* 🔎 Issue filtering
* 🧠 Retrieved project knowledge
* 🤖 AI confidence
* 🔎 Source-code evidence

---

### 🔍 Issue Filtering

Review findings can be filtered by:

**Category**

* All
* Bugs
* Security
* Performance
* Best Practices

**Severity**

* All
* Critical
* High
* Medium
* Low

This allows users to focus on the most important findings.

---

### 📜 Review History

Reviews are persisted using **SQLite**.

The application provides:

* Filename search
* Programming-language filtering
* Score-range filtering
* Review sorting
* Saved structured reviews
* Severity summaries
* Evidence from previous reviews
* Delete functionality

This allows users to compare and revisit previous code reviews.

---

### 📄 PDF Reports

The application can generate PDF reports containing the AI review results.

Reports provide a portable version of the review for sharing or documentation.

---

## 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │    Streamlit UI      │
                         │                      │
                         │ Dashboard / Filters  │
                         │ Review History       │
                         │ PDF Generation       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Review Engine      │
                         │                      │
                         │ Gemini Code Review   │
                         │ Structured JSON      │
                         │ Severity / Confidence│
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
              ┌──────────┐   ┌────────────┐   ┌─────────────┐
              │   RAG    │   │ Evidence   │   │   SQLite    │
              │ Retrieval│   │ Validation │   │   History   │
              └────┬─────┘   └────────────┘   └─────────────┘
                   │
                   ▼
          ┌────────────────────┐
          │ Gemini Embeddings  │
          │                    │
          │ Knowledge Base     │
          │ Cosine Similarity  │
          │ Hybrid Ranking     │
          └────────────────────┘
```

---

## 🔄 Review Workflow

```text
User submits source code
          │
          ▼
Language detection
          │
          ▼
Generate query embedding
          │
          ▼
Retrieve relevant project knowledge
          │
          ▼
Send code + relevant knowledge
to Gemini
          │
          ▼
Structured JSON review
          │
          ▼
Evidence validation
          │
          ▼
Validated findings
          │
          ├───────────────┐
          ▼               ▼
   Streamlit Dashboard   SQLite
          │               │
          ▼               ▼
      PDF Report     Review History
```

---

## 🧪 Example

### Submitted Code

```python
def get_user(username):

    query = "SELECT * FROM users WHERE name = '" + username + "'"

    return query
```

### Detected Finding

```text
Category: Security

Severity: CRITICAL

Issue:
SQL Injection vulnerability

Evidence:
query = "SELECT * FROM users WHERE name = '" + username + "'"

Explanation:
User input is directly concatenated into the SQL query.

Suggested Fix:
Use parameterized SQL queries instead of string concatenation.
```

The system also retrieves the relevant project rule:

```text
Use parameterized queries instead of string concatenation for SQL.
```

The evidence is then validated against the submitted source code before the finding is displayed.

---

## 🛠️ Tech Stack

### Frontend

* Streamlit
* Plotly

### AI / GenAI

* Google Gemini
* Gemini Embeddings
* Structured JSON generation
* Retrieval-Augmented Generation (RAG)

### Backend

* Python
* SQLite

### Data Processing

* Pandas
* NumPy

### Reporting

* ReportLab

### Configuration

* python-dotenv

### Deployment

* Streamlit Community Cloud
* GitHub

---

## 📁 Project Structure

```text
AI_Code_Review_Bot/
│
├── app.py
├── review_engine.py
├── database.py
├── report_generator.py
├── utils.py
│
├── project_knowledge.py
├── embeddings.py
├── knowledge_store.py
│
├── test_review.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── pages/
├── database/
├── reports/
└── screenshots/
```

### Core Components

| File                   | Responsibility                             |
| ---------------------- | ------------------------------------------ |
| `app.py`               | Streamlit application and UI               |
| `review_engine.py`     | Gemini review engine and validation        |
| `project_knowledge.py` | Project-specific coding rules              |
| `embeddings.py`        | Gemini embedding generation                |
| `knowledge_store.py`   | Knowledge retrieval and similarity ranking |
| `database.py`          | SQLite persistence                         |
| `report_generator.py`  | PDF report generation                      |
| `utils.py`             | Utility functions                          |
| `test_review.py`       | Review testing                             |

---

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud** and connected to the GitHub repository.

Deployment configuration:

```text
Repository: AI_Code_Review_Bot
Branch: main
Entry point: app.py
```

Secrets such as the Gemini API key are configured through the deployment platform rather than committed to the repository.

Streamlit Community Cloud supports deploying directly from GitHub and automatically updating the application when repository changes are pushed.

---

## 🔐 Security

Sensitive configuration is intentionally excluded from version control.

Ignored files include:

```text
.env
.venv/
__pycache__/
reviews.db
review_report.pdf
```

The Gemini API key is supplied through environment variables locally and deployment secrets in Streamlit Cloud.

---

## 📈 Project Evolution

### V1 — Initial MVP

* Streamlit interface
* Gemini-powered review
* SQLite storage
* PDF report generation

### V2.1 — Structured AI Review

* Native structured JSON output
* Category-based findings
* Severity
* Confidence
* Evidence
* Suggestions

### V2.3 — RAG

* Project knowledge base
* Gemini embeddings
* Cosine similarity
* Hybrid category-aware retrieval

### V2.4 — Review Validation

* Evidence verification
* Unsupported finding removal
* False-positive reduction
* Conservative review behavior

### V2.5 — Advanced UI

* Dashboard metrics
* Severity visualization
* Category visualization
* Interactive filtering
* RAG visibility
* Professional issue cards
* Review history filtering
* Review sorting
* Severity summaries
* Evidence history
* Deployment on Streamlit Community Cloud

---

## 🎯 Key Engineering Concepts Demonstrated

This project demonstrates practical experience with:

* Generative AI
* Large Language Models
* Structured LLM output
* Prompt engineering
* Retrieval-Augmented Generation
* Vector embeddings
* Cosine similarity
* Hybrid information retrieval
* AI output validation
* Hallucination / false-positive reduction
* Python
* Streamlit
* SQLite
* Data visualization
* PDF generation
* Git & GitHub
* Cloud deployment

---

## 🚀 Future Improvements

Potential future extensions include:

* GitHub Pull Request integration
* Automated PR comments
* Repository-level code analysis
* Automated CI/CD code review
* Additional programming languages
* Larger vector databases
* More advanced semantic retrieval
* Unit-test generation
* Automatic code-fix suggestions
* Authentication and user-specific review history

---

## 👨‍💻 Author

**Rithwik Ramadugu**

B.Tech | AI / ML / Data Analytics / Data Scientist / Data Engineering

### 🔗 Live Application

**[AI-Powered Code Review Bot](https://rvrrithwik28aipoweredcodereviewbot.streamlit.app/)**

---

## ⭐ Project Status

**V2.5 — Advanced Streamlit UI + RAG + Evidence Validation + Cloud Deployment**

**Status: ✅ Completed and Deployed**
