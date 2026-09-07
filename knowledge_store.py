import streamlit as st
import math

from project_knowledge import PROJECT_KNOWLEDGE
from embeddings import generate_document_embedding


# -------------------------------------------------------
# BUILD KNOWLEDGE VECTOR STORE
# -------------------------------------------------------

@st.cache_resource
def build_knowledge_store():

    knowledge_store = []

    for category, rules in PROJECT_KNOWLEDGE.items():

        for rule in rules:

            embedding = generate_document_embedding(rule)

            knowledge_store.append({
                "category": category,
                "rule": rule,
                "embedding": embedding
            })

    return knowledge_store


# -------------------------------------------------------
# COSINE SIMILARITY
# -------------------------------------------------------

def cosine_similarity(vector_a, vector_b):

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


# -------------------------------------------------------
# SEARCH KNOWLEDGE STORE
# -------------------------------------------------------

def search_knowledge(
    query_embedding,
    knowledge_store,
    top_k=5,
    query_text=""
):

    query_lower = query_text.lower()

    # ---------------------------------------------------
    # DETECT RELEVANT REVIEW CATEGORIES
    # ---------------------------------------------------

    relevant_categories = set()

    security_keywords = [
        "sql",
        "select",
        "insert",
        "update",
        "delete",
        "execute",
        "password",
        "token",
        "secret",
        "api key",
        "input",
        "authentication",
        "authorization"
    ]

    performance_keywords = [
        "loop",
        "for ",
        "while ",
        "database",
        "query",
        "cache",
        "slow",
        "performance"
    ]

    best_practice_keywords = [
        "def ",
        "class ",
        "try:",
        "except",
        "raise ",
        "import "
    ]

    if any(
        keyword in query_lower
        for keyword in security_keywords
    ):
        relevant_categories.add("security")

    if any(
        keyword in query_lower
        for keyword in performance_keywords
    ):
        relevant_categories.add("performance")

    if any(
        keyword in query_lower
        for keyword in best_practice_keywords
    ):
        relevant_categories.add("best_practices")

    # Always consider code quality
    relevant_categories.add("code_quality")

    # ---------------------------------------------------
    # CALCULATE HYBRID RELEVANCE
    # ---------------------------------------------------
    print("DEBUG query:", query_text)
    print("DEBUG categories:", relevant_categories)

    results = []

    for item in knowledge_store:

        similarity = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        category_bonus = 0.0

        if item["category"] == "security" and "security" in relevant_categories:
            category_bonus = 0.20

        elif item["category"] == "performance" and "performance" in relevant_categories:
            category_bonus = 0.10

        elif item["category"] == "best_practices" and "best_practices" in relevant_categories:
            category_bonus = 0.05

        final_score = similarity + category_bonus

        results.append({
            "category": item["category"],
            "rule": item["rule"],
            "similarity": similarity,
            "score": final_score
        })

    # ---------------------------------------------------
    # SORT BY HYBRID SCORE
    # ---------------------------------------------------

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]