from typing import Dict, List

class JDParser:
    def parse(self, jd_text: str) -> Dict[str, List[str]]:
        """
        Parses the JD text to extract structured sections.
        Assumes a format with "Required Skills" and "Preferred Skills" headers.
        """
        lines = jd_text.split('\n')
        sections = {
            "required_skills": [],
            "preferred_skills": [],
            "experience": []
        }
        
        current_section = None
        
        # Simple heuristic parser
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            line_lower = line.lower()
            
            if "required skills" in line_lower:
                current_section = "required_skills"
                continue
            elif "preferred skills" in line_lower:
                current_section = "preferred_skills"
                continue
            elif "experience" in line_lower:
                current_section = "experience"
                continue
                
            if current_section and (line.startswith('-') or line.startswith('•')):
                # Remove bullet points
                content = line.lstrip('-• ').strip()
                if current_section == "experience":
                    sections["experience"].append(content)
                else:
                    # For skills, we might want to clean simply
                    sections[current_section].append(content)
            elif current_section:
                 # Try to capture lines that might not have bullets but are in the section
                 # This relies on the structure being somewhat clean
                 sections[current_section].append(line)

        return sections
