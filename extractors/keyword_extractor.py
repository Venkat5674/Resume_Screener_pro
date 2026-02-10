import re
from typing import Set, Dict

class KeywordExtractor:
    def __init__(self, skills_taxonomy: Dict[str, Dict[str, list]]):
        self.skills_taxonomy = skills_taxonomy

    def extract_skills(self, text: str) -> Set[str]:
        text_lower = text.lower()
        found_skills = set()

        for category, skills_dict in self.skills_taxonomy.items():
            for skill_name, variations in skills_dict.items():
                for variation in variations:
                    # Prevent "Java" matching "JavaScript"
                    # Use \b for word boundaries. 
                    # Escape variation in case it contains special regex chars (like C++)
                    pattern = r"\b" + re.escape(variation.lower()) + r"\b"
                    if re.search(pattern, text_lower):
                        found_skills.add(skill_name)
                        # Once a skill is found via one variation, we don't need to check other variations for the same skill
                        break 

        return found_skills
    
    def extract_experience(self, text: str) -> str:
        # Basic extraction for example purposes - looking for common patterns
        # In a real system, this would be more complex NLP
        # Patterns like: "3 years experience", "5+ years", "10 years of"
        pattern = r"(\d+\+?)\s*(?:years?|yrs?)"
        match = re.search(pattern, text.lower())
        if match:
            return match.group(1)
        return "0"
