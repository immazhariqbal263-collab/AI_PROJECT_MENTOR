    client = genai.Client(api_key=api_key)
    prompt = f"""
You are AI Project Mentor, a practical and encouraging software-project guide.
Create a realistic, beginner-friendly but impressive project blueprint from the user's idea.

USER DETAILS
Project idea: {idea}
Current skill level: {skill}
Preferred programming language: {language}
Time available: {time_available}
Interests/domain: {interests or "Not specified"}
Extra requirements: {extra or "None"}

RESPONSE REQUIREMENTS
- Keep the project achievable within the stated time and skill level.
- Make the idea feel distinctive through one practical feature, not unnecessary complexity.
- Use clear Markdown headings and concise explanations.
- Include these sections in this exact order:
  1. Project title and one-line pitch
  2. Problem it solves and target users
  3. What makes it stand out (3 specific points)
  4. Core features (MVP first; separate optional future features)
  5. Recommended tech stack with a short reason for each tool
  6. User workflow (numbered steps)
  7. Build roadmap divided into realistic phases, with estimated time per phase
  8. Suggested folder/file structure in a code block
  9. Implementation guidance: explain the first 3 tasks to start coding
  10. Testing checklist
  11. Demo presentation: a 60-second explanation suitable for a class/project presentation
  12. Possible viva/interview questions (5) with short answers
- Do not claim that code has been tested or that external services are connected.
- Avoid paid tools unless a free alternative is available.
- If the user's idea is too broad, narrow it into a useful MVP.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.65,
            max_output_tokens=5000,
        ),
    )
    return response.text or "The AI returned an empty response. Please try again."

st.markdown("""
<div class="hero">
  <h1>🚀 AI Project Mentor</h1>
  <div class="muted">Turn a rough idea into a practical project blueprint you can actually build and present.</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Settings")
    st.caption("Add your Gemini API key here, or save it as a Streamlit secret.")
    api_key_input = st.text_input("Gemini API key", type="password", placeholder="Enter your Gemini API key")
    st.markdown("---")
    st.markdown("**How it works**")
    st.write("1. Describe your project idea.")
    st.write("2. Choose your skill level and available time.")
    st.write("3. Generate a step-by-step blueprint.")
    st.markdown("---")
    st.caption("Your API key is used for the request and is not displayed in the app.")

api_key = api_key_input.strip() or get_api_key()

left, right = st.columns([1.25, 0.75], gap="large")
with left:
    st.subheader("💡 Describe your idea")
    idea = st.text_area(
        "What do you want to build?",
        placeholder="Example: An app that helps students understand difficult textbook topics...",
        height=125,
        help="A rough idea is enough. The AI will help narrow it into a manageable project.",
    )
    interests = st.text_input(
        "Domain or interests (optional)",
        placeholder="Education, health, productivity, agriculture..."
    )
    extra = st.text_area(
        "Any special requirements? (optional)",
        placeholder="Example: Must have a simple dashboard and work well on mobile.",
        height=85,
    )

with right:
    st.subheader("🧭 Your build preferences")
    skill = st.selectbox("Current skill level", ["Beginner", "Intermediate", "Advanced"])
    language = st.selectbox(
        "Preferred programming language",
        ["Python", "JavaScript", "Java", "C++", "No preference"]
    )
    time_available = st.selectbox(
        "Time available",
        ["1–2 days", "1 week", "2 weeks", "1 month", "2–3 months"]
    )
    st.info("Tip: Choose the time you can realistically spend. The plan will be scaled to it.")

generate = st.button("✨ Generate my project blueprint", type="primary", use_container_width=True)

if generate:
    if not idea.strip():
        st.warning("Please describe your project idea first.")
    elif not api_key:
        st.error("Gemini API key not found. Enter it in the sidebar or add GEMINI_API_KEY to your Streamlit secrets.")
        st.markdown("Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).")
    else:
        with st.spinner("Your AI mentor is designing the project..."):
            try:
                result = generate_blueprint(
                    api_key, idea.strip(), skill, language, time_available, interests.strip(), extra.strip()
                )
                st.session_state["blueprint"] = result
                st.session_state["last_idea"] = idea.strip()
            except Exception as exc:
                st.error(f"Could not generate the blueprint: {exc}")
                st.caption("Check your API key, internet connection, and Gemini model availability, then try again.")

if "blueprint" in st.session_state:
    st.markdown("---")
    st.subheader("📘 Your project blueprint")
    st.caption(f"Generated for: {st.session_state.get('last_idea', 'Your idea')}")
    st.markdown(st.session_state["blueprint"])
    st.download_button(
        "⬇️ Download blueprint as Markdown",
        data=st.session_state["blueprint"],
        file_name="ai_project_blueprint.md",
        mime="text/markdown",
        use_container_width=True,
