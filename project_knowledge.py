# ==========================================================
# PROJECT KNOWLEDGE BASE
# ==========================================================

PROJECT_KNOWLEDGE = {

    "security": [
        "Never hardcode passwords, API keys, tokens, or secrets.",
        "Use parameterized queries instead of string concatenation for SQL.",
        "Validate and sanitize user input before processing it.",
        "Do not expose sensitive information in logs or error messages."
    ],

    "performance": [
        "Avoid unnecessary loops over large datasets.",
        "Prefer efficient data structures and algorithms.",
        "Avoid repeated database queries inside loops.",
        "Use caching when expensive operations are repeatedly performed."
    ],

    "best_practices": [
        "Use meaningful variable and function names.",
        "Keep functions focused on a single responsibility.",
        "Avoid unnecessary code duplication.",
        "Handle exceptions appropriately.",
        "Add comments where the logic is not obvious."
    ],

    "code_quality": [
        "Write readable and maintainable code.",
        "Keep functions reasonably small.",
        "Use consistent formatting and naming conventions.",
        "Avoid unused variables and unreachable code."
    ]
}


def get_project_knowledge(categories=None):

    knowledge = []

    if categories is None:
        categories = PROJECT_KNOWLEDGE.keys()

    for category in categories:

        if category not in PROJECT_KNOWLEDGE:
            continue

        knowledge.append(
            f"\n{category.upper()} RULES:"
        )

        for rule in PROJECT_KNOWLEDGE[category]:

            knowledge.append(
                f"- {rule}"
            )

    return "\n".join(knowledge)

def get_relevant_categories(code):

    code_lower = code.lower()

    categories = []

    # ---------------------------------------------------
    # SECURITY
    # ---------------------------------------------------

    security_keywords = [
        "password",
        "api_key",
        "api key",
        "token",
        "secret",
        "execute(",
        "sqlite3",
        "sql injection",
        "select ",
        "insert ",
        "update ",
        "delete ",
        "input("
    ]

    if any(keyword in code_lower for keyword in security_keywords):
        categories.append("security")


    # ---------------------------------------------------
    # PERFORMANCE
    # ---------------------------------------------------

    performance_keywords = [
        "for ",
        "while ",
        "cache",
        "large dataset",
        "database connection",
        "connection pool",
        "nested loop",
        "time complexity"
    ]

    if any(keyword in code_lower for keyword in performance_keywords):
        categories.append("performance")


    # ---------------------------------------------------
    # BEST PRACTICES
    # ---------------------------------------------------

    best_practice_keywords = [
        "def ",
        "class ",
        "try:",
        "except",
        "import ",
        "pass",
        "raise "
    ]

    if any(keyword in code_lower for keyword in best_practice_keywords):
        categories.append("best_practices")


    # ---------------------------------------------------
    # CODE QUALITY
    # ---------------------------------------------------

    if code.strip():
        categories.append("code_quality")


    # ---------------------------------------------------
    # REMOVE DUPLICATES
    # ---------------------------------------------------

    return list(dict.fromkeys(categories))