import re

def extract_score(review_text):

    match = re.search(
        r'(\d{1,3})\s*/\s*100',
        review_text
    )

    if match:
        return int(match.group(1))

    return 0


def detect_language(filename):

    filename = filename.lower()

    if filename.endswith(".py"):
        return "Python"

    elif filename.endswith(".java"):
        return "Java"

    elif filename.endswith(".sql"):
        return "SQL"

    elif filename.endswith(".js"):
        return "JavaScript"

    elif filename.endswith(".cpp"):
        return "C++"

    elif filename.endswith(".c"):
        return "C"

    return "Unknown"