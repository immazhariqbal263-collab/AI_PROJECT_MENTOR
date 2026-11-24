import os

import streamlit as st
from google import genai
from google.genai import types


st.set_page_config(
    page_title="AI Project Mentor",
    page_icon="🚀",
    layout="wide",
)


def get_api_key():
    """Read the Gemini key from Streamlit Secrets or environment variables."""
    try:
        secret_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        secret_key = ""
    return secret_key or os.getenv("GEMINI_API_KEY", "")


def generate_blueprint(api_key, idea, skill, language, time_available, interests, extra):
    """Generate a project blueprint using Google Gemini."""
    client = genai.Client(api_key=api_key)

    prompt = f"""
You are AI Project Mentor, a practical and encouraging software-project guide.
Create a realistic, beginner-friendly but impressive software project blueprint.

USER DETAILS
Project idea: {idea}
Current skill level: {skill}
Preferred programming language: {language}
Time available: {time_available}
Interests/domain: {interests or "Not specified"}
Extra requirements: {extra or "None"}

Write clear Markdown and include these sections:
1. Project title and one-line pitch
2. Problem it solves and target users
3. What makes it stand out (3 points)
4. Core MVP features and optional future features
5. Recommended technology stack and reasons
6. User workflow
7. Development roadmap with phases and estimated time
8. Suggested folder/file structure in a code block
9. First 3 coding tasks
10. Testing checklist
11. A 60-second project presentation script
12. Five viva/interview questions with short answers

Keep the project achievable for the selected skill level and time.
Prefer free tools. Do not claim that code has been tested or services connected.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.65,
            max_output_tokens=5000,
        ),
    )

    return response.text or "Gemini returned an empty response. Please try again."


st.title("🚀 AI Project Mentor")
st.write(
    "Turn a rough idea into a practical project blueprint you can build and present."
)

with st.sidebar:
    st.header("⚙️ Settings")
    api_key_input = st.text_input(
        "Gemini API key",
        type="password",
        placeholder="Enter your Gemini API key",
    )
    st.caption(
        "Alternatively, add GEMINI_API_KEY to your Streamlit Community Cloud Secrets."
    )
    st.markdown("[Get a Gemini API key](https://aistudio.google.com/apikey)")

api_key = api_key_input.strip() or get_api_key()

col1, col2 = st.columns([1.2, 0.8])

with col1:
    st.subheader("💡 Your project idea")
    idea = st.text_area(
        "What do you want to build?",
        placeholder="Example: An app that helps students understand difficult topics...",
        height=130,
