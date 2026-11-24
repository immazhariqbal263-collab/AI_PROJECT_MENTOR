import os

import streamlit as st
from google import genai
from google.genai import types


# ------------------------------------------------------------
# Page setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="AI Project Mentor",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 AI Project Mentor")
st.write(
    "Turn your software idea into a practical project blueprint "
    "with help from Google Gemini."
)


# ------------------------------------------------------------
# Gemini configuration
# ------------------------------------------------------------
def load_api_key():
    """Load the API key from Streamlit Secrets or environment variables."""
    try:
        secrets_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        secrets_key = ""

    environment_key = os.getenv("GEMINI_API_KEY", "")
    return secrets_key or environment_key


def create_project_blueprint(
    api_key,
    project_idea,
    skill_level,
    programming_language,
    available_time,
    domain,
    extra_requirements,
):
    """Ask Gemini to create a detailed software project plan."""
    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an experienced software project mentor.
Create a realistic, useful, and achievable project blueprint.

PROJECT DETAILS
Project idea: {project_idea}
Skill level: {skill_level}
Preferred programming language: {programming_language}
Available time: {available_time}
Domain/interests: {domain or "Not specified"}
Extra requirements: {extra_requirements or "None"}

Write the answer in clear Markdown. Include these sections:

1. Project title and short description
2. Problem statement and target users
3. What makes the project unique
4. Main features (separate essential MVP features from future features)
5. Recommended technology stack with reasons
6. How the user will use the application
7. Step-by-step development roadmap with estimated time
8. Suggested project folder and file structure in a code block
9. The first three coding tasks
10. Testing checklist
11. A short presentation script for a university project demo
12. Five viva questions with short answers

Keep the scope suitable for the user's skill level and available time.
Prefer free tools and explain technical terms simply.
Do not claim that code has been tested or deployed.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.6,
            max_output_tokens=5000,
        ),
    )

    answer = response.text
    if not answer:
        raise RuntimeError("Gemini returned an empty response. Please try again.")

    return answer
