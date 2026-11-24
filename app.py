import os

import streamlit as st
from google import genai
from google.genai import types


st.set_page_config(page_title="AI Project Mentor", page_icon="🚀", layout="wide")


def get_api_key():
    try:
        key_from_secrets = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key_from_secrets = ""
    return key_from_secrets or os.getenv("GEMINI_API_KEY", "")


def generate_blueprint(api_key, idea, skill, language, time_available, interests, extra):
    client = genai.Client(api_key=api_key)

    prompt = f"""
You are AI Project Mentor. Create a realistic, beginner-friendly software project blueprint.

User details:
- Project idea: {idea}
- Skill level: {skill}
- Preferred language: {language}
- Time available: {time_available}
- Interests: {interests or "Not specified"}
- Extra requirements: {extra or "None"}

Return clear Markdown with these sections:
1. Project title and one-line pitch
2. Problem and target users
3. Three ways the project stands out
4. MVP features and optional future features
5. Recommended technology stack with reasons
6. User workflow
7. Development roadmap with phases and estimated time
8. Suggested folder/file structure in a code block
9. First three coding tasks
10. Testing checklist
11. A 60-second presentation script
12. Five viva questions with short answers

Keep the scope achievable for the selected skill level and time.
Prefer free tools. Do not claim code has been tested.
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
st.write("Turn a rough idea into a practical project blueprint you can build and present.")

with st.sidebar:
    st.header("⚙️ Settings")
    api_key_input = st.text_input(
        "Gemini API key",
        type="password",
        placeholder="Enter your Gemini API key",
    )
    st.caption("You can also set GEMINI_API_KEY in Streamlit Secrets.")
    st.markdown("[Get a Gemini API key](https://aistudio.google.com/apikey)")

api_key = api_key_input.strip() or get_api_key()

left_col, right_col = st.columns([1.2, 0.8])

with left_col:
    st.subheader("💡 Your project idea")
    idea = st.text_area(
        "What do you want to build?",
        placeholder="Example: An app that helps students understand difficult topics...",
        height=130,
    )
    interests = st.text_input(
        "Domain or interests (optional)",
        placeholder="Education, productivity, agriculture...",
    )
    extra = st.text_area(
        "Special requirements (optional)",
        placeholder="Example: A simple dashboard and mobile-friendly interface.",
        height=90,
    )

with right_col:
