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

# -------------------------------------------------------
# AI-GENERATED IMPROVED CODE
# -------------------------------------------------------

def generate_improved_code(code, review, language="python"):
    """
    Generate an improved version of the submitted source code
    based on the validated AI review findings.
    """

    # Collect all validated issues
    all_issues = []

    for category in [
        "bugs",
        "security",
        "performance",
        "best_practices"
    ]:
        for issue in review.get(category, []):
            all_issues.append({
                "category": category,
                "severity": issue.get("severity"),
                "issue": issue.get("issue"),
                "evidence": issue.get("evidence"),
                "explanation": issue.get("explanation"),
                "suggestion": issue.get("suggestion")
            })

    # If no issues were detected, return the original code
    if not all_issues:
        return {
            "improved_code": code,
            "changes": [
                "No validated issues were detected.",
                "The original code was preserved."
            ]
        }

    issues_text = json.dumps(
        all_issues,
        indent=2
    )

    prompt = f"""
You are an expert software engineer responsible for improving source code.

Your task is to generate an improved version of the submitted code
based ONLY on the validated review findings provided below.

IMPORTANT RULES:

1. Preserve the original functionality of the program.
2. Fix ONLY the validated review findings provided below.
3. Do not introduce unrelated changes.
4. Do not remove existing functionality.
5. Keep the same programming language.
6. Preserve the existing function names unless a change is required to fix an issue.
7. Preserve the existing inputs and outputs unless a change is required for correctness or security.
8. Use the review evidence as the source of truth.
9. Do not invent additional problems or make speculative changes.
10. Make the smallest reasonable changes required to fix the findings.
11. Ensure the generated code is syntactically valid.
12. Ensure variables referenced in the improved code are defined or available in the original context.
13. Preserve important imports and add an import only when required by the fix.
14. Do not change database APIs, frameworks, libraries, or external interfaces unless the review finding requires it.
15. If a suggested fix depends on a library or framework, use the conventions already present in the original code.
16. Return the complete improved source code.
17. Do not return a patch or partial snippet.
18. Do not include Markdown code fences.
19. Do not include explanations outside the source code.

VALIDATED REVIEW FINDINGS:

{issues_text}

ORIGINAL SOURCE CODE:

{code}

Return ONLY the complete improved source code.
Do not include:
- Markdown code fences
- Explanations
- Comments about the review
- "Here is the improved code"
- Any text before or after the source code
"""

    # ---------------------------------------------------
    # RETRY LOGIC
    # ---------------------------------------------------

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            improved_code = response.text.strip()

            # Remove accidental Markdown code fences
            if improved_code.startswith("```"):
                lines = improved_code.splitlines()

                if lines and lines[0].startswith("```"):
                    lines = lines[1:]

                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]

                improved_code = "\n".join(lines).strip()

            if not improved_code:
                raise ValueError(
                    "Gemini returned empty improved code."
                )

            if all_issues and improved_code.strip() == code.strip():
                raise ValueError(
                    "Gemini returned the original code without applying "
                    "the validated fixes."
                )

            # Validate Python syntax only for Python code
            if language and language.lower() == "python":

                try:

                    compile(
                        improved_code,
                        "<improved_code>",
                        "exec"
                    )

                except SyntaxError as syntax_error:

                    if attempt < 2:
                        time.sleep(2)
                        continue

                    return {
                        "error": (
                            "Gemini generated Python code with a "
                            "syntax error after multiple attempts: "
                            f"{syntax_error}"
                        )
                    }

            return {
                "improved_code": improved_code,
                "changes": [
                    issue["suggestion"]
                    for issue in all_issues
                    if issue.get("suggestion")
                ]
            }
        
        except Exception as e:

            if attempt < 2:
                time.sleep(5)

            else:

                if "429" in str(e):
                    return {
                        "error": (
                            "Gemini API quota exceeded while generating "
                            "the improved code."
                        )
                    }

                return {
                    "error": (
                        f"Unable to generate improved code: {str(e)}"
                    )
                }