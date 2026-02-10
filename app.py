import streamlit as st
import os
import json
import pandas as pd
from parsers.resume_parser import ResumeParser
from parsers.jd_parser import JDParser
from extractors.keyword_extractor import KeywordExtractor
from matcher.scorer import Scorer
from utils.llm_client import LLMClient
from utils.email_client import EmailClient

# Page Config
st.set_page_config(page_title="Resume Screener Pro", page_icon="📄", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .skill-chip-missing {
        background-color: #ffcccc;
        color: #cc0000;
        padding: 5px 10px;
        border-radius: 15px;
        margin: 2px;
        display: inline-block;
        font-size: 0.9em;
    }
    .skill-chip-matched {
        background-color: #ccffcc;
        color: #006600;
        padding: 5px 10px;
        border-radius: 15px;
        margin: 2px;
        display: inline-block;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# Load Configuration
@st.cache_data
def load_data():
    with open('data/config.json', 'r') as f:
        config = json.load(f)
    with open('data/skills_taxonomy.json', 'r') as f:
        skills = json.load(f)
    return config, skills

config, skills_taxonomy = load_data()

# Initialize Components
resume_parser = ResumeParser()
jd_parser = JDParser()
keyword_extractor = KeywordExtractor(skills_taxonomy)
scorer = Scorer(config['weights'])

# Sidebar Inputs
with st.sidebar:
    st.title("🚀 Job Config")
    
    # API Keys Expander
    with st.expander("🔑 API Keys", expanded=True):
        # Try to load from secrets first
        default_key = st.secrets.get("general", {}).get("OPENROUTER_API_KEY", "")
        openrouter_key = st.text_input("OpenRouter API Key", value=default_key, type="password")
        firebase_cred_path = st.text_input("Firebase Service Account Path", value="firebase_credentials.json")
    
    st.info("Paste your JD and upload resumes to start screening.")
    
    jd_text = st.text_area(
        "Job Description:",
        height=300,
        placeholder="Required Skills: ...\nPreferred Skills: ..."
    )
    
    uploaded_files = st.file_uploader(
        "Upload Resumes:",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )
    
    process_btn = st.button("Start Screening", type="primary", use_container_width=True)

# Initialize Optional Clients
llm_client = LLMClient(openrouter_key) if openrouter_key else None
email_client = None
if firebase_cred_path and os.path.exists(firebase_cred_path):
    try:
        email_client = EmailClient(firebase_cred_path)
    except Exception as e:
        st.sidebar.error(f"Firebase Init Error: {e}")

st.title("📄 AI Resume Insights")
st.markdown("---")

if process_btn:
    if not jd_text:
        st.error("⚠️ Please provide a valid Job Description.")
    elif not uploaded_files:
        st.error("⚠️ Please upload at least one résumé.")
    else:
        with st.spinner("Analyzing candidates..."):
            # ... (Parsing JD & Resumes - same as before)
            jd_data = jd_parser.parse(jd_text)
            
            # Display JD Stats
            col1, col2 = st.columns(2)
            col1.metric("Required Skills", len(jd_data['required_skills']))
            col2.metric("Preferred Skills", len(jd_data['preferred_skills']))
            st.divider()

            results = []
            
            # Process Loop
            if not os.path.exists("temp"):
                os.makedirs("temp")
            
            progress_bar = st.progress(0)
            
            for i, uploaded_file in enumerate(uploaded_files):
                temp_path = os.path.join("temp", uploaded_file.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                try:
                    resume_text = resume_parser.parse(temp_path)
                    resume_skills = keyword_extractor.extract_skills(resume_text)
                    result = scorer.score(resume_skills, jd_data)
                    
                    results.append({
                        "name": uploaded_file.name,
                        "data": result,
                        "text": resume_text # Store text for LLM
                    })
                    
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {e}")
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            # Sort Results
            results.sort(key=lambda x: x['data']['total_score'], reverse=True)
            
            # Display Detailed Results
            for res in results:
                data = res['data']
                score = data['total_score']
                name = res['name']
                
                with st.expander(f"**{name}** - Score: {score}/100", expanded=(res == results[0])):
                    
                    # Top Level Metrics
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Match Score", f"{score}%")
                    m2.metric("Required", f"{data['breakdown']['required']}%")
                    m3.metric("Preferred", f"{data['breakdown']['preferred']}%")
                    m4.metric("Experience", f"{data['breakdown']['experience']}")
                    
                    st.write("### 🔍 Skill Gap Analysis")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write("**✅ Matched Skills**")
                        if data['details']['matched_required']:
                            for s in data['details']['matched_required']:
                                st.markdown(f'<span class="skill-chip-matched">{s}</span>', unsafe_allow_html=True)
                        else:
                            st.caption("No required skills matched.")
                            
                    with c2:
                        st.write("**❌ Missing Critical Skills**")
                        if data['details']['missing_required']:
                            for s in data['details']['missing_required']:
                                st.markdown(f'<span class="skill-chip-missing">{s}</span>', unsafe_allow_html=True)
                        else:
                            st.caption("All required skills present! 🎉")
                            
                    st.write("---")
                    
                    # AI & Automation Section
                    st.write("### 🤖 AI & Automation")
                    
                    a1, a2 = st.columns(2)
                    
                    with a1:
                        if st.button(f"Generate Interview Questions for {name}", key=f"btn_q_{name}"):
                            if llm_client:
                                with st.spinner("Generating questions..."):
                                    questions = llm_client.generate_interview_questions(
                                        name, 
                                        data['details']['missing_required'], 
                                        jd_text
                                    )
                                    st.info(questions)
                            else:
                                st.warning("Please enter OpenRouter API Key in sidebar.")
                                
                    with a2:
                        if st.button(f"Send Interview Invite to {name}", key=f"btn_e_{name}"):
                            if email_client:
                                # Mock email for demo if not extracted from resume
                                candidate_email = "candidate@example.com" 
                                success, msg = email_client.send_invite(name, candidate_email, "Senior Developer")
                                if success:
                                    st.success(msg)
                                else:
                                    st.error(msg)
                            else:
                                st.warning("Firebase credentials not configured.")

                    if data['details']['missing_required']:
                        st.warning(f"To increase score, candidate needs: **{', '.join(data['details']['missing_required'])}**.")

            
else:
    st.markdown("""
    ### Welcome!
    Use the sidebar to upload documents. 
    The AI will analyze resumes against your JD and provide a detailed scoring breakdown.
    """)
