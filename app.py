import os
import time
import streamlit as st
from google import genai
from google.genai import types

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Project Mentor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HEADER ---
st.title("🚀 AI Project Mentor")
st.markdown("Turn your software idea into a practical, step-by-step project blueprint powered by Google Gemini.")
st.divider()

# --- SIDEBAR: API KEY & SETTINGS ---
with st.sidebar:
    st.header("⚙️ Configuration")

    api_key = ""
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ API Key loaded from Streamlit Secrets")
    elif os.environ.get("GEMINI_API_KEY"):
        api_key = os.environ.get("GEMINI_API_KEY")
        st.success("✅ API Key loaded from Environment")
    else:
        api_key = st.text_input(
            "Enter Gemini API Key",
            type="password",
            help="Get an API key from Google AI Studio (aistudio.google.com)"
        )
        if not api_key:
            st.warning("⚠️ Please enter your Gemini API Key or add `GEMINI_API_KEY` to your Streamlit Secrets.")

    st.divider()
    st.subheader("Model Settings")
    model_options = ["gemini-3.8-flash", "gemini-4-hydrogen", "gemini-3.5-flash-lite"]
    model_choice = st.selectbox(
        "Gemini Model",
        options=model_options,
        index=0,
        help="If the chosen model hits high traffic (503), the app will retry and fall back automatically."
    )
    auto_fallback = st.checkbox("Auto-fallback to another model on 503", value=True)

    st.markdown("---")
    st.caption("Built with Streamlit & Google GenAI SDK")

# --- MAIN INTERFACE ---
left_col, right_col = st.columns([1, 1.3], gap="large")

with left_col:
    st.subheader("💡 Project Details")

    with st.form("project_form"):
        project_idea = st.text_area(
            "Describe your software idea*",
            placeholder="e.g., A personal finance tracker that scans receipts using OCR and categorizes expenses automatically...",
            height=140
        )

        col1, col2 = st.columns(2)
        with col1:
            skill_level = st.selectbox(
                "Your Skill Level",
                ["Beginner", "Intermediate", "Advanced", "Full-Stack Pro"]
            )
            project_type = st.selectbox(
                "Application Type",
                ["Web App", "Mobile App", "CLI Tool", "AI / ML Pipeline", "API / Backend", "Desktop App", "Browser Extension"]
            )

        with col2:
            tech_stack = st.text_input(
                "Preferred Languages / Stack",
                placeholder="e.g., Python, React, PostgreSQL",
                value="Python, Streamlit"
            )
            timeline = st.selectbox(
                "Target Timeline",
                ["Weekend Hackathon (48 hrs)", "2 Weeks", "1 Month", "3 Months (Production MVP)"]
            )

        focus_areas = st.multiselect(
            "Include in Blueprint",
            [
                "Core & Stretch Features",
                "Recommended Tech Stack & Architecture",
                "Database Schema Design",
                "Step-by-Step Development Roadmap",
                "Folder & File Structure",
                "Potential Pitfalls & Security Tips"
            ],
            default=[
                "Core & Stretch Features",
                "Recommended Tech Stack & Architecture",
                "Step-by-Step Development Roadmap",
                "Folder & File Structure"
            ]
        )

        submitted = st.form_submit_button("✨ Generate Project Blueprint", use_container_width=True, type="primary")


def _call_gemini_with_retry(client, model_name, prompt, max_retries=3):
    last_error = None
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                )
            )
            return response.text, model_name
        except Exception as e:
            last_error = e
            err_str = str(e)
            is_transient = "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str
            if not is_transient or attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # 1s, 2s backoff
    raise last_error


def generate_blueprint(key, primary_model, allow_fallback, idea, level, p_type, stack, time_limit, areas):
    client = genai.Client(api_key=key)

    areas_str = ", ".join(areas) if areas else "All standard architectural sections"

    prompt = f"""
    Act as a Senior Staff Software Engineer and Technical Mentor.
    Create a comprehensive, actionable, and practical software project blueprint based on the following specifications:

    - **Project Idea:** {idea}
    - **Developer Skill Level:** {level}
    - **Application Type:** {p_type}
    - **Preferred Tech Stack:** {stack if stack else "Recommend the best fit"}
    - **Target Timeline:** {time_limit}
    - **Requested Sections:** {areas_str}

    **Formatting & Quality Guidelines:**
    1. Tailor the complexity, libraries, and architectural patterns strictly to a **{level}** developer working within a **{time_limit}** timeframe.
    2. Use clear Markdown headings, bullet points, and text-based diagrams or file trees where helpful.
    3. Be concrete: name specific libraries, packages, APIs, and database tables rather than giving generic advice.
    4. Keep the tone encouraging, structured, and mentor-like.
    """

    candidates = [primary_model]
    if allow_fallback:
        for m in ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-4-hydrogen"]:
            if m not in candidates:
                candidates.append(m)

    last_exc = None
    for idx, candidate in enumerate(candidates):
        try:
            return _call_gemini_with_retry(client, candidate, prompt, max_retries=3)
        except Exception as e:
            last_exc = e
            err_str = str(e)
            is_transient = "503" in err_str or "UNAVAILABLE" in err_str
            if is_transient and idx < len(candidates) - 1:
                continue
            raise
    raise last_exc


# --- OUTPUT DISPLAY ---
with right_col:
    st.subheader("📋 Your Project Blueprint")

    if "blueprint" not in st.session_state:
        st.session_state.blueprint = None
    if "used_model" not in st.session_state:
        st.session_state.used_model = None

    if submitted:
        if not api_key:
            st.error("🔑 Missing API Key! Please add your `GEMINI_API_KEY` in the sidebar or Streamlit Secrets.")
        elif not project_idea.strip():
            st.warning("✍️ Please describe your project idea before generating a blueprint.")
        else:
            with st.spinner(f"🧠 Architecting your project blueprint with {model_choice}..."):
                try:
                    result, model_used = generate_blueprint(
                        key=api_key,
                        primary_model=model_choice,
                        allow_fallback=auto_fallback,
                        idea=project_idea,
                        level=skill_level,
                        p_type=project_type,
                        stack=tech_stack,
                        time_limit=timeline,
                        areas=focus_areas
                    )
                    st.session_state.blueprint = result
                    st.session_state.used_model = model_used
                except Exception as e:
                    st.error(f"❌ Error communicating with Gemini API: {str(e)}")

    if st.session_state.blueprint:
        if st.session_state.used_model:
            st.caption(f"Generated using `{st.session_state.used_model}`")

        st.download_button(
            label="📥 Download Blueprint (.md)",
            data=st.session_state.blueprint,
            file_name="project_blueprint.md",
            mime="text/markdown",
            use_container_width=True
        )

        with st.container(border=True):
            st.markdown(st.session_state.blueprint)
    else:
        st.info("👈 Fill out your project details on the left and click **Generate Project Blueprint** to get started.")
