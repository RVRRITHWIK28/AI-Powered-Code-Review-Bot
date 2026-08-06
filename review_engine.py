import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def review_code(code):

    prompt = f"""
You are a Senior Software Engineer.

Analyze the following code.

Return:

1. Code Quality Score (/100)
2. Bugs
3. Security Issues
4. Performance Improvements
5. Best Practices
6. Improved Version

Code:
{code}
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )

            return response.text

        except Exception as e:

            if attempt < 2:
                time.sleep(5)
            else:
                if "429" in str(e):
                    return """[WARNING] Gemini API quota exceeded.

You have reached the free daily request limit.

Please wait until the quota resets or use another API key."""
                else:
                    return f"""[ERROR] Unexpected Error

{str(e)}"""