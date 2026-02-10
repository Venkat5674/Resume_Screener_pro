import os
import json
import argparse
from pathlib import Path
from parsers.resume_parser import ResumeParser
from parsers.jd_parser import JDParser
from extractors.keyword_extractor import KeywordExtractor
from matcher.scorer import Scorer

def main():
    parser = argparse.ArgumentParser(description="Résumé Screening System CLI")
    parser.add_argument("--jd", type=str, help="Path to Job Description file (txt)", default="input/jd.txt")
    parser.add_argument("--input", type=str, help="Directory containing resumes", default="input")
    args = parser.parse_args()

    # Load Config
    try:
        with open('data/config.json', 'r') as f:
            config = json.load(f)
        with open('data/skills_taxonomy.json', 'r') as f:
            skills_taxonomy = json.load(f)
    except FileNotFoundError as e:
        print(f"Error loading configuration: {e}")
        return

    # Initialize Components
    resume_parser = ResumeParser()
    jd_parser = JDParser()
    keyword_extractor = KeywordExtractor(skills_taxonomy)
    scorer = Scorer(config['weights'])

    # Read JD
    jd_path = Path(args.jd)
    if not jd_path.exists():
        print(f"JD file not found at {jd_path}. Please create it or provide path with --jd.")
        # Create a dummy JD for testing if default
        if str(jd_path) == "input/jd.txt":
            print("Creating sample JD at input/jd.txt...")
            with open(jd_path, "w") as f:
                f.write("Required Skills:\n- Python\n- SQL\n\nPreferred Skills:\n- Docker\n")
        else:
            return
    
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    jd_data = jd_parser.parse(jd_text)
    print("Job Description Parsed.")
    print(f"Required: {jd_data['required_skills']}")
    print(f"Preferred: {jd_data['preferred_skills']}")
    print("-" * 50)

    # Process Resumes
    input_dir = Path(args.input)
    if not input_dir.exists():
        print(f"Input directory {input_dir} not found.")
        return

    results = []
    print(f"Scanning {input_dir} for resumes...")
    
    files = list(input_dir.glob("*.pdf")) + list(input_dir.glob("*.docx")) + list(input_dir.glob("*.txt"))
    # Exclude the jd file itself if it's in the same dir and matches extension
    files = [f for f in files if f.resolve() != jd_path.resolve()]

    for file_path in files:
        print(f"Processing {file_path.name}...")
        try:
            resume_text = resume_parser.parse(file_path)
            resume_skills = keyword_extractor.extract_skills(resume_text)
            score_data = scorer.score(resume_skills, jd_data)
            score = score_data['total_score']
            
            results.append({
                "name": file_path.name,
                "score": score,
                "matched": list(resume_skills)
            })
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")

    # Sort and Display
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print("\n" + "="*60)
    print("SCREENING RESULTS")
    print("="*60)
    for i, res in enumerate(results):
        print(f"Rank #{i+1}: {res['name']} | Score: {res['score']:.2f}/100 | Matched: {', '.join(res['matched'])}")

if __name__ == "__main__":
    main()
