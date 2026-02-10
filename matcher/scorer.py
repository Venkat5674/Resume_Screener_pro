from typing import Set, Dict, List

class Scorer:
    def __init__(self, weights: Dict[str, float]):
        self.weights = weights

    def score(self, resume_skills: Set[str], jd_data: Dict[str, List[str]]) -> Dict:
        """
        Calculates a score (0-100) and returns detailed analysis.
        """
        
        # 1. Required Skills Match
        # Normalize resume skills to lower case for comparison
        resume_skills_lower = {s.lower() for s in resume_skills}
        
        required_skills_jd = self._normalize_skills(jd_data.get('required_skills', []))
        
        if not required_skills_jd:
            score_req = 0
            matches_req = set()
            missing_req = set()
        else:
            matches_req = resume_skills_lower.intersection(required_skills_jd)
            missing_req = required_skills_jd - matches_req
            score_req = (len(matches_req) / len(required_skills_jd)) * 100

        # 2. Preferred Skills Match
        preferred_skills_jd = self._normalize_skills(jd_data.get('preferred_skills', []))
        
        if not preferred_skills_jd:
            score_pref = 0
            matches_pref = set()
            missing_pref = set()
        else:
            matches_pref = resume_skills_lower.intersection(preferred_skills_jd)
            missing_pref = preferred_skills_jd - matches_pref
            score_pref = (len(matches_pref) / len(preferred_skills_jd)) * 100
            
        # 3. Experience Match
        # Placeholder: Award 50 points if we are just screening. 
        score_exp = 50

        # 4. Keywords Match (Contextual/Domain)
        # Score based on density of skills. Capped at 100 for 10 skills.
        score_keys = min((len(resume_skills) / 10) * 100, 100)

        total_score = (
            (score_req * self.weights['required_skills']) +
            (score_pref * self.weights['preferred_skills']) +
            (score_exp * self.weights['experience']) +
            (score_keys * self.weights['keywords'])
        )
        
        return {
            "total_score": round(total_score, 2),
            "breakdown": {
                "required": round(score_req, 2),
                "preferred": round(score_pref, 2),
                "experience": round(score_exp, 2),
                "keywords": round(score_keys, 2)
            },
            "details": {
                "matched_required": list(matches_req),
                "missing_required": list(missing_req),
                "matched_preferred": list(matches_pref),
                "missing_preferred": list(missing_pref)
            }
        }

    def _normalize_skills(self, skills_list: List[str]) -> Set[str]:
        # Normalize JD skills to lower case
        normalized = set()
        for s in skills_list:
            clean = s.lower().strip()
            normalized.add(clean)
        return normalized
