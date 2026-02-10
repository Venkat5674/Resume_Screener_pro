import os
from openai import OpenAI
import json

class LLMClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def generate_interview_questions(self, candidate_name: str, missing_skills: list, jd_text: str) -> str:
        if not missing_skills:
            return "No missing skills identified. Ready for general interview!"
            
        skills_str = ", ".join(missing_skills)
        prompt = f"""
        You are an expert technical recruiter. 
        Candidate Name: {candidate_name}
        Missing Skills: {skills_str}
        
        Job Description:
        {jd_text[:1000]}... (truncated)
        
        Task:
        Generate 3 specific technical interview questions to test the candidate's knowledge on the missing skills. 
        Focus on practical scenarios.
        Output format: Numbered list.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="google/gemini-flash-1.5", # Use a cost-effective model
                messages=[
                    {"role": "system", "content": "You are a helpful recruitment assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating questions: {str(e)}"

    def suggest_improvements(self, resume_text: str, jd_text: str) -> str:
        prompt = f"""
        Analyze this resume against the JD.
        Resume: {resume_text[:2000]}
        JD: {jd_text[:1000]}
        
        Provide 3 concrete bullet points on how the candidate can improve their resume to better match this job.
        """
        try:
            response = self.client.chat.completions.create(
                model="google/gemini-flash-1.5",
                messages=[
                    {"role": "system", "content": "You are a expert resume coach."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error gathering suggestions: {str(e)}"
