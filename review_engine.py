import os
import time
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from embeddings import generate_query_embedding
from knowledge_store import (
    build_knowledge_store,
    search_knowledge
)
# -------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# -------------------------------------------------------

load_dotenv()


# -------------------------------------------------------
# GEMINI CLIENT
# -------------------------------------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# -------------------------------------------------------
# AI REVIEW JSON SCHEMA
# -------------------------------------------------------

review_schema = {
    "type": "object",
    "properties": {
        "score": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100
        },

        "bugs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {
                        "type": "string",
                        "enum": [
                            "LOW",
                            "MEDIUM",
                            "HIGH",
                            "CRITICAL"
                        ]
                    },
                    "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                    },
                    "issue": {
                        "type": "string"
                    },
                    "evidence": {
                        "type": "string"
                    },
                    "explanation": {
                        "type": "string"
                    },
                    "suggestion": {
                        "type": "string"
                    }
                },
                "required": [
                    "severity",
                    "confidence",
                    "issue",
                    "evidence",
                    "explanation",
                    "suggestion"
                ]
            }
        },

        "security": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {
                        "type": "string",
                        "enum": [
                            "LOW",
                            "MEDIUM",
                            "HIGH",
                            "CRITICAL"
                        ]
                    },
                    "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                    },
                    "issue": {
                        "type": "string"
                    },
                    "evidence": {
                        "type": "string"
                    },
                    "explanation": {
                        "type": "string"
                    },
                    "suggestion": {
                        "type": "string"
                    }
                },
                "required": [
                    "severity",
                    "confidence",
                    "issue",
                    "evidence",
                    "explanation",
                    "suggestion"
                ]
            }
        },

        "performance": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {
                        "type": "string",
                        "enum": [
                            "LOW",
                            "MEDIUM",
                            "HIGH",
                            "CRITICAL"
                        ]
                    },
                    "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                    },
                    "issue": {
                        "type": "string"
                    },
                    "evidence": {
                        "type": "string"
                    },
                    "explanation": {
                        "type": "string"
                    },
                    "suggestion": {
                        "type": "string"
                    }
                },
                "required": [
                    "severity",
                    "confidence",
                    "issue",
                    "evidence",
                    "explanation",
                    "suggestion"
                ]
            }
        },

        "best_practices": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {
                        "type": "string",
                        "enum": [
                            "LOW",
                            "MEDIUM",
                            "HIGH",
                            "CRITICAL"
                        ]
                    },
                    "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                    },
                    "issue": {
                        "type": "string"
                    },
                    "evidence": {
                        "type": "string"
                    },
                    "explanation": {
                        "type": "string"
                    },
                    "suggestion": {
                        "type": "string"
                    }
                },
                "required": [
                    "severity",
                    "confidence",
                    "issue",
                    "evidence",
                    "explanation",
                    "suggestion"
                ]
            }
        }
    },

    "required": [
        "score",
        "bugs",
        "security",
        "performance",
        "best_practices"
    ]
}

# -------------------------------------------------------
# VALIDATE AI-GENERATED EVIDENCE
# -------------------------------------------------------

def validate_issue_evidence(issue, code):
    """
    Check whether the evidence provided by Gemini
    exists in the submitted source code.
    """

    evidence = issue.get("evidence", "").strip()

    if not evidence:
        return False

    # Exact match
    if evidence in code:
        return True

    # Allow minor whitespace differences
    normalized_evidence = " ".join(evidence.split())
    normalized_code = " ".join(code.split())

    if normalized_evidence in normalized_code:
        return True

    return False


# -------------------------------------------------------
# AI CODE REVIEW
# -------------------------------------------------------

def review_code(code, return_retrieval=False):

    retrieval_query = f"""
    Find software engineering rules relevant to reviewing this source code.

    Focus on:
    - security vulnerabilities
    - database safety
    - input validation
    - bugs
    - performance problems
    - code quality
    - software engineering best practices

    SOURCE CODE:
    {code}
    """

    query_embedding = generate_query_embedding(retrieval_query)

    knowledge_store = build_knowledge_store()

    retrieved_results = search_knowledge(
        query_embedding,
        knowledge_store,
        top_k=5,
        query_text=code
    )

    project_knowledge = "\n".join(
        [
            f"- {result['rule']}"
            for result in retrieved_results
        ]
    )

    prompt = f"""
You are an expert software code reviewer.

You are reviewing code for a specific project.

PROJECT KNOWLEDGE:
{project_knowledge}

Use the project knowledge above when reviewing the code.

For every reported issue, provide concrete evidence from the submitted source code.

The evidence must be an exact or near-exact snippet from the source code that demonstrates the issue.

Do not report an issue if you cannot provide supporting evidence from the submitted code.

Be conservative and prefer false negatives over unsupported findings.

Important:
- Identify only issues that are actually present.
- Do not invent problems.
- Use project rules when relevant.
- Give conservative security findings.
- Score the overall code quality from 0 to 100.
- Confidence must be between 0.0 and 1.0.
- If a category has no real issues, return an empty array.
- Do not report an issue simply because a rule exists.
- Report a rule only when the submitted code actually violates it.

CODE TO REVIEW:

{code}
"""

    # ---------------------------------------------------
    # RETRY LOGIC
    # ---------------------------------------------------

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,

                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=review_schema
                )
            )

            # -------------------------------------------
            # CONVERT AI RESPONSE TO PYTHON DICTIONARY
            # -------------------------------------------

            result = json.loads(response.text)
            # -------------------------------------------------------
            # VALIDATE REVIEW FINDINGS
            # -------------------------------------------------------

            for category in [
                "bugs",
                "security",
                "performance",
                "best_practices"
            ]:

                validated_issues = []

                for issue in result.get(category, []):

                    if validate_issue_evidence(issue, code):
                        validated_issues.append(issue)

                result[category] = validated_issues

            if return_retrieval:
                result["_retrieved_knowledge"] = retrieved_results

            return result

        except json.JSONDecodeError:

            if attempt < 2:
                time.sleep(2)

            else:
                return {
                    "error": "AI returned an invalid JSON response."
                }

        except Exception as e:

            if attempt < 2:
                time.sleep(5)

            else:

                if "429" in str(e):

                    return {
                        "error": (
                            "Gemini API quota exceeded. "
                            "Please wait until the quota resets "
                            "or use another API key."
                        )
                    }

                return {
                    "error": f"Unexpected error: {str(e)}"
                }