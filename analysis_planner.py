import json

from google.genai import types
from prompts import ANALYSIS_PLANNER_PROMPT
from gemini_helper import generate_with_retry


def create_analysis_plan(
    client,
    dataset_context,
    question
):

    prompt = f"""
{ANALYSIS_PLANNER_PROMPT}

DATASET INFORMATION:

{dataset_context}

USER QUESTION:

{question}
"""

    response = generate_with_retry(
        client=client,
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    return json.loads(response.text)