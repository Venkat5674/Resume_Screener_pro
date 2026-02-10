# 📄 Résumé Screening System (AI-Powered)

An automated recruitment tool designed to parse, analyze, and rank résumés against a Job Description (JD). It features a **Premium Streamlit UI**, **Detailed Skill Gap Analysis**, **AI-Generated Interview Questions**, and **Email Automation**.

![Streamlit UI](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)

## 🚀 Features

### Core Capabilities
- **Multi-Format Parsing**: Extracts text from PDF, DOCX, and TXT files.
- **Smart JD Parsing**: Automatically identifies "Required" vs. "Preferred" skills in Job Descriptions.
- **Weighted Scoring Engine**: Ranks candidates based on:
  - Required Skills (50%)
  - Preferred Skills (25%)
  - Experience (15%)
  - Keyword Density (10%)
- **Detailed Analytics**: Breakdown of matched/missing skills, score distribution, and personalized recommendations.

### 🤖 AI & Automation (New!)
- **AI Interview Generator**: Uses **OpenRouter (LLM)** to specific technical interview questions based on a candidate's *missing* skills.
- **Email Automation**: Queues interview invites to **Firebase** for automated sending via Cloud Functions.

## 🛠️ Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/YOUR_USERNAME/resume-screening-system.git
    cd resume-screening-system
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

### 1. API Keys (Recommended)
This system uses **OpenRouter** for AI features and **Firebase** for emails.
-   Run the app and enter keys in the Sidebar.
-   **OR** Create a `.streamlit/secrets.toml` file to pre-load them:

    ```toml
    [general]
    OPENROUTER_API_KEY = "your_sk_or_key_here"
    ```

### 2. Skills Taxonomy
Data for skill matching is stored in `data/skills_taxonomy.json`. You can edit this file to add new skills or synonyms.

## ▶️ Usage

### Web Interface (Recommended)
Launch the interactive dashboard:
```bash
python -m streamlit run app.py
```
1.  Paste the Job Description in the sidebar.
2.  Upload one or more Résumés.
3.  Click **"Start Screening"**.
4.  Expand candidate cards to view scores, missing skills, and AI features.

### Command Line
Process a folder of résumés without valid UI:
```bash
python main.py --jd input/jd.txt --input input_folder/
```

## 📂 Project Structure
```
resume_screening_system/
├── app.py                  # Main Streamlit Application
├── main.py                 # CLI Entry Point
├── parsers/                # Document Parsers (PDF, DOCX, JD)
├── extractors/             # Keyword & Skill Extractors
├── matcher/                # Scoring Logic & Algorithm
├── utils/                  # AI & Email Clients
├── data/                   # Configuration Files (JSON)
├── input/                  # Sample Input Files
└── requirements.txt        # Dependencies
```

## 🤝 Contribution
Contributions are welcome! Please fork the repository and submit a Pull Request.

## 📄 License
MIT License.
