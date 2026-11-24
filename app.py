import os
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
    model_choice = st.selectbox(
        "Gemini Model",
        options=["gemini-3.8-flash", "gemini-4-hydrogen", "gemini-3.5-flash-lite"],
        index=0,
        help="gemini-3.8-flash is fast and reliable; gemini-4-hydrogen is great for coding & agentic workflows."
    )

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


def generate_blueprint(key, model, idea, level, p_type, stack, time, areas):
    client = genai.Client(api_key=key)

    areas_str = ", ".join(areas) if areas else "All standard architectural sections"

    prompt = f"""
    Act as a Senior Staff Software Engineer and Technical Mentor.
    Create a comprehensive, actionable, and practical software project blueprint based on the following specifications:

    - **Project Idea:** {idea}
    - **Developer Skill Level:** {level}
    - **Application Type:** {p_type}
    - **Preferred Tech Stack:** {stack if stack else "Recommend the best fit"}
    - **Target Timeline:** {time}
    - **Requested Sections:** {areas_str}

    **Formatting & Quality Guidelines:**
    1. Tailor the complexity, libraries, and architectural patterns strictly to a **{level}** developer working within a **{time}** timeframe.
    2. Use clear Markdown headings, bullet points, and text-based diagrams or file trees where helpful.
    3. Be concrete: name specific libraries, packages, APIs, and database tables rather than giving generic advice.
    4. Keep the tone encouraging, structured, and mentor-like.
    """

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
        )
    )
    return response.text


# --- OUTPUT DISPLAY ---
with right_col:
    st.subheader("📋 Your Project Blueprint")

    if "blueprint" not in st.session_state:
        st.session_state.blueprint = None

    if submitted:
        if not api_key:
            st.error("🔑 Missing API Key! Please add your `GEMINI_API_KEY` in the sidebar or Streamlit Secrets.")
        elif not project_idea.strip():
            st.warning("✍️ Please describe your project idea before generating a blueprint.")
        else:
            with st.spinner(f"🧠 Architecting your project blueprint with {model_choice}..."):
                try:
                    result = generate_blueprint(
                        key=api_key,
                        model=model_choice,
                        idea=project_idea,
                        level=skill_level,
                        p_type=project_type,
                        stack=tech_stack,
                        time=timeline,
                        areas=focus_areas
                    )
                    st.session_state.blueprint = result
                except Exception as e:
                    st.error(f"❌ Error communicating with Gemini API: {str(e)}")

    if st.session_state.blueprint:
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
