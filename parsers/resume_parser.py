import os
from pathlib import Path
import PyPDF2
from docx import Document

class ResumeParser:
    def parse(self, file_path: str) -> str:
        file_path = Path(file_path)
        ext = file_path.suffix.lower()
        if ext == '.pdf':
            return self._extract_pdf(file_path)
        elif ext == '.docx':
            return self._extract_docx(file_path)
        elif ext == '.txt':
            return self._extract_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _extract_pdf(self, file_path: Path) -> str:
        text = ""
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()

    def _extract_docx(self, file_path: Path) -> str:
        doc = Document(file_path)
        return "\n".join(
            para.text for para in doc.paragraphs
        ).strip()
    
    def _extract_txt(self, file_path: Path) -> str:
         with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            return file.read().strip()
