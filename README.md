# 🤖 AI-Powered Code Review Bot

An AI-powered code review application that analyzes source code using **Google Gemini**, retrieves project-specific coding knowledge using **RAG and embeddings**, validates AI-generated evidence to reduce unsupported findings, generates improved code based on validated findings, and presents the results through an interactive **Streamlit dashboard**.

---

## 🚀 Live Demo

[**AI-Powered Code Review Bot →**](https://rvrrithwik28aipoweredcodereviewbot.streamlit.app/)

---

## 📌 Overview

The **AI-Powered Code Review Bot** is a full-stack GenAI application designed to automate and improve the code review process.

Users can submit source code and receive a structured review covering:

- 🐛 Bugs
- 🔐 Security vulnerabilities
- ⚡ Performance issues
- 📋 Best practices
- 🎯 Severity
- 🤖 AI confidence
- 🔎 Evidence from the submitted source code
- 🛠️ Recommended fixes

The application combines **LLM-based code analysis, Retrieval-Augmented Generation (RAG), embedding-based retrieval, evidence validation, AI-generated improved code, SQLite persistence, PDF reporting, and an interactive Streamlit interface**.

---

## ✨ Key Features

### 🧠 AI-Powered Code Review

Uses **Google Gemini** to analyze submitted source code and return structured review results.

The model evaluates:

- Bugs
- Security
- Performance
- Best practices
- Overall code quality

The review is returned using a structured JSON schema rather than relying on unstructured text generation.

---

### 🎯 Severity & Confidence

Every detected issue can include:

| Field | Description |
|---|---|
| Severity | LOW, MEDIUM, HIGH, or CRITICAL |
| Confidence | AI confidence score |
| Issue | Description of the problem |
| Evidence | Code demonstrating the issue |
| Explanation | Why the issue matters |
| Suggestion | Recommended improvement |

This makes the output easier to interpret and process programmatically.

---

### 🔎 Evidence Validation

The system doesn't blindly trust every AI-generated finding.

For each detected issue, the application checks whether the supplied evidence actually exists in the submitted source code.

The validation process supports:

- Exact evidence matching
- Normalized whitespace matching
- Removal of unsupported findings

This helps reduce **false positives and hallucinated evidence**.

---

### 🧠 RAG / Project Knowledge

The application includes a project-specific knowledge base containing coding guidelines for areas such as:

- Security
- Performance
- Best practices
- Code quality

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

- ⭐ Overall code quality score
- 🔴 Critical issue count
- 🟠 High issue count
- 🟡 Medium issue count
- 🟢 Low issue count
- 📈 Code quality visualization
- 📊 Severity distribution
- 📂 Category-wise issue distribution
- 🔎 Issue filtering
- 🧠 Retrieved project knowledge
- 🤖 AI confidence
- 🔎 Source-code evidence

---

### 🔍 Issue Filtering

Review findings can be filtered by:

**Category**

- All
- Bugs
- Security
- Performance
- Best Practices

**Severity**

- All
- Critical
- High
- Medium
- Low

This allows users to focus on the most important findings.

---

### 📜 Review History

Reviews are persisted using **SQLite**.

The application provides:

- Filename search
- Programming-language filtering
- Score-range filtering
- Review sorting
- Saved structured reviews
- Severity summaries
- Evidence from previous reviews
- Delete functionality

This allows users to compare and revisit previous code reviews.

---

### 📄 PDF Reports

The application can generate PDF reports containing the AI review results.

Reports provide a portable version of the review for sharing or documentation.

---

## ✨ AI-Generated Improved Code

The application can generate a complete improved version of the submitted source code based only on **validated review findings**.

Key safeguards include:

- Preserves the original functionality
- Fixes only validated findings
- Uses source-code evidence as the source of truth
- Avoids unrelated refactoring
- Preserves existing interfaces where possible
- Returns complete source code
- Validates generated Python syntax
- Supports improved-code generation for multiple programming languages
- Provides side-by-side original and improved code
- Allows users to download the improved source code

The generated code is designed to make **minimal, targeted changes** rather than performing unrelated modifications.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │      Streamlit UI       │
                    │       (app.py)          │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    Code Review Engine   │
                    │    (review_engine.py)   │
                    └────────────┬────────────┘
                                 │
                 ┌───────────────┼────────────────┐
                 │               │                │
                 ▼               ▼                ▼
        ┌────────────────┐ ┌──────────────┐ ┌───────────────┐
        │ Gemini LLM     │ │ RAG / Vector │ │ Validation    │
        │ Code Analysis  │ │ Retrieval    │ │ Engine        │
        └────────────────┘ └──────────────┘ └───────────────┘
                 │               │                │
                 └───────────────┼────────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │ Structured Review       │
                    │ JSON Result             │
                    └────────────┬────────────┘
                                 │
                 ┌───────────────┼────────────────┐
                 │               │                │
                 ▼               ▼                ▼
        ┌────────────────┐ ┌──────────────┐ ┌───────────────┐
        │ Review         │ │ AI-Generated │ │ PDF Report    │
        │ Dashboard      │ │ Improved Code│ │ Generator     │
        └────────────────┘ └──────────────┘ └───────────────┘
                 │               │                │
                 └───────────────┼────────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │      SQLite Database    │
                    │     Review History      │
                    └─────────────────────────┘
```

---

## 🔄 Review Workflow

```text
User uploads source code
          │
          ▼
Select programming language
          │
          ▼
Generate code embeddings
          │
          ▼
Retrieve relevant project knowledge
          │
          ▼
Send code + retrieved knowledge to Gemini
          │
          ▼
Structured JSON review
          │
          ▼
Severity + confidence assignment
          │
          ▼
Evidence validation
          │
          ▼
Remove unsupported findings
          │
          ▼
Display review dashboard
          │
          ├──────────────► Save review to SQLite
          │
          ├──────────────► Generate PDF report
          │
          └──────────────► Generate improved code
                                  │
                                  ▼
                         Validate generated code
                                  │
                                  ▼
                         Download improved code
```

---

## 🔍 Example Review

### Input

```python
def get_user(username):
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    return query
```

### AI Finding

```text
Category: Security
Severity: CRITICAL
Confidence: 100%

Issue:
SQL Injection vulnerability.

Evidence:
query = "SELECT * FROM users WHERE name = '" + username + "'"

Explanation:
User-controlled input is directly concatenated into a SQL query,
which can allow an attacker to manipulate the query.

Suggestion:
Use parameterized queries instead of string concatenation.
```

The evidence validation layer verifies that the reported evidence is actually present in the submitted source code before the finding is displayed.

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
├── embeddings.py
├── knowledge_store.py
├── project_knowledge.py
├── test_review.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── pages/
├── database/
├── reports/
├── screenshots/
│
└── .env
```

### Core Files

| File | Purpose |
|---|---|
| `app.py` | Streamlit application and interactive dashboard |
| `review_engine.py` | Gemini-powered code review, structured analysis, evidence validation, and improved-code generation |
| `database.py` | SQLite database operations and review history |
| `report_generator.py` | PDF report generation |
| `utils.py` | Utility functions |
| `embeddings.py` | Generates Gemini document and query embeddings |
| `knowledge_store.py` | Stores and retrieves project knowledge using vector similarity |
| `project_knowledge.py` | Contains project-specific coding and security rules |
| `test_review.py` | Testing and validation of the review engine |
| `requirements.txt` | Python dependencies |

## 🛠️ Tech Stack

### Frontend
- Streamlit
- Python

### AI / Machine Learning
- Google Gemini API
- Gemini 3.5 Flash-Lite
- Gemini Embedding Model
- Prompt Engineering
- Generative AI
- Natural Language Processing (NLP)
- Retrieval-Augmented Generation (RAG)
- Cosine Similarity

### Code Analysis
- AI-powered code review
- Structured JSON output
- Severity classification
- Confidence scoring
- Evidence-based validation
- False-positive reduction
- AI-generated improved code
- Python syntax validation

### Data & Storage
- SQLite
- Vector embeddings
- Local project knowledge store

### Reporting
- ReportLab
- PDF report generation

### Development Tools
- Git
- GitHub
- Virtual Environment (`venv`)
- Python-dotenv

### Deployment
- Streamlit Community Cloud

---

## 📁 Project Structure


AI_Code_Review_Bot/
│
├── app.py
├── review_engine.py
├── database.py
├── report_generator.py
├── utils.py
├── embeddings.py
├── knowledge_store.py
├── project_knowledge.py
├── test_review.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── pages/
├── database/
├── reports/
├── screenshots/
│
└── .env

### Core Files

| File | Purpose |
|---|---|
| `app.py` | Streamlit application and interactive dashboard |
| `review_engine.py` | Gemini-powered code review, structured analysis, evidence validation, and improved-code generation |
| `database.py` | SQLite database operations and review history |
| `report_generator.py` | PDF report generation |
| `utils.py` | Utility functions |
| `embeddings.py` | Generates Gemini document and query embeddings |
| `knowledge_store.py` | Stores and retrieves project knowledge using vector similarity |
| `project_knowledge.py` | Contains project-specific coding and security rules |
| `test_review.py` | Testing and validation of the review engine |
| `requirements.txt` | Python dependencies |

---

## 🚀 Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/RVRRITHWIK28/AI-Powered-Code-Review-Bot.git
cd AI-Powered-Code-Review-Bot
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

### Deployment Configuration

- Repository: `AI-Powered-Code-Review-Bot`
- Main application: `app.py`
- Platform: Streamlit Community Cloud
- API key: stored securely using Streamlit Secrets

---

## 🔐 Security

The project follows several security-focused practices:

- API keys are stored using environment variables or deployment secrets.
- `.env` is excluded from Git using `.gitignore`.
- AI findings require supporting evidence from the submitted source code.
- Unsupported findings are filtered out through evidence validation.
- The improved-code generator is restricted to validated findings.
- AI-generated code preserves the original functionality as much as possible.
- Python improved code is syntax-validated before being returned.
- No secrets or credentials are intentionally included in the source code.

---

## 📈 Project Evolution

### V1 — Basic AI Code Review
- Streamlit interface
- Gemini-powered code analysis
- Basic issue detection
- SQLite review storage
- PDF reports

### V2.1 — Structured AI Review
- Native JSON response schema
- Structured issue categories
- Consistent AI output

### V2.2 — Severity & Confidence
- LOW / MEDIUM / HIGH / CRITICAL severity
- AI confidence scores
- Better prioritization of findings

### V2.3 — RAG / Project Knowledge
- Gemini embeddings
- Semantic retrieval
- Project-specific coding rules
- Category-aware hybrid retrieval

### V2.4 — Evidence Validation
- Evidence-based issue validation
- False-positive reduction
- Conservative issue filtering
- Source-code evidence display

### V2.5 — Advanced Streamlit UI
- KPI dashboard
- Severity distribution
- Category-wise analysis
- Interactive filtering
- Review history
- RAG visibility
- Evidence display
- Improved user experience
- Cloud deployment

### V2.6 — AI-Generated Improved Code
- AI-generated corrected source code
- Fixes validated findings only
- Preserves original functionality
- Minimal code modifications
- Complete source-code output
- Python syntax validation
- Multi-language support
- Downloadable improved code

---

## 🧠 Key Engineering Concepts

This project demonstrates practical implementation of:

- Generative AI
- Large Language Models (LLMs)
- Prompt Engineering
- Structured AI Output
- Retrieval-Augmented Generation (RAG)
- Vector Embeddings
- Semantic Search
- Cosine Similarity
- Hybrid Retrieval
- AI Evaluation
- Evidence-Based Validation
- False-Positive Reduction
- Code Analysis
- Software Security
- Data Persistence
- Interactive Data Visualization
- Cloud Deployment

---

## 🔮 Future Improvements

Potential future enhancements include:

- GitHub Pull Request integration
- Automatic code review on new Pull Requests
- Line-level code comments
- Support for additional programming languages
- Advanced AST-based code analysis
- Automated test generation
- Code quality metrics
- CI/CD integration
- Team-based review dashboards
- Review analytics and trends
- Authentication and user management

---

## 👨‍💻 Author

**Ramadugu Venkata Rama Rithwik**

B.Tech | AI / ML / Data Analytics / Data Science / Data Engineering

---

## 🌐 Final Project Status

**V2.6 — AI-Powered Code Review + RAG + Evidence Validation + AI-Generated Improved Code + Advanced Streamlit UI + Cloud Deployment**

## 🚀 Live Application

[**AI-Powered Code Review Bot**](https://rvrrithwik28aipoweredcodereviewbot.streamlit.app/)

V2.5 — Advanced Streamlit UI + RAG + Evidence Validation + Cloud Deployment

Status: ✅ Completed and Deployed
