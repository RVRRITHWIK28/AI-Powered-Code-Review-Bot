import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


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
# GENERATE DOCUMENT EMBEDDING
# -------------------------------------------------------

def generate_document_embedding(text):

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=768
        )
    )

    return result.embeddings[0].values


# -------------------------------------------------------
# GENERATE QUERY EMBEDDING
# -------------------------------------------------------

def generate_query_embedding(text):

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=768
        )
    )

    return result.embeddings[0].values