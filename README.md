AI Project Mentor
AI Project Mentor turns a rough software idea into a practical, presentation-ready project blueprint.
What it does
A user enters:
- A project idea
- Current skill level (Beginner, Intermediate, Advanced)
- Preferred programming language
- Available development time
- Optional interests and special requirements
The app uses the Google Gemini API to generate:
- Project title, purpose, and target users
- Distinctive features and an MVP feature list
- Suggested technology stack
- User workflow
- Phased development roadmap
- Suggested folder structure
- First coding tasks
- Testing checklist
- A short project presentation script
- Viva/interview questions with answers
Users can download the generated blueprint as a Markdown file.
Tech stack
- Python
- Streamlit
- Google Gemini API (gemini-2.5-flash)
- Google Gen AI Python SDK (google-genai)
Run locally
1. Install Python 3.10 or newer.
2. Download or clone this project folder.
3. Open a terminal in the project folder.
4. Install dependencies:
   pip install -r requirements.txt
5. Start the app:
   streamlit run app.py
6. Open the local URL shown in your terminal (usually http://localhost:8501).
7. Enter your Gemini API key in the app sidebar.
Create a Gemini API key in Google AI Studio:
https://aistudio.google.com/apikey
Deploy on Streamlit Community Cloud
1. Create a GitHub repository.
2. Upload app.py, requirements.txt, and README.md to the repository's root.
3. Open https://share.streamlit.io/ and sign in with GitHub.
4. Select Create app and choose your repository and app.py.
5. Open the app's Settings → Secrets.
6. Add your key in TOML format:
   GEMINI_API_KEY = "your_gemini_api_key_here"
7. Save the secrets and deploy/reboot the app.
Important: Never upload your real API key to GitHub or write it directly into app.py. Use Streamlit Secrets for deployment.
Project structure
ai-project-mentor/
├── app.py
├── requirements.txt
└── README.md
Common issues
GEMINI_API_KEY is missing
Enter the key in the app sidebar, or add GEMINI_API_KEY to Streamlit Community Cloud Secrets.
API authentication error
Check that the key is copied correctly and is active in Google AI Studio.
Model not available
The app currently requests gemini-2.5-flash. If Google changes model availability, replace the model name in app.py with a currently supported Gemini model.
App does not start
Check that the three files are in the repository root and that Streamlit and google-genai are listed in requirements.txt.
Notes
The output is AI-generated guidance. Review the plan, verify technical details, and adjust the scope to your course or project requirements.
