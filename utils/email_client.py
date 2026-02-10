import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import streamlit as st
import datetime

class EmailClient:
    def __init__(self, cred_path: str):
        # Prevent re-initialization error in Streamlit
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def send_invite(self, candidate_name: str, candidate_email: str, job_title: str):
        """
        Writes a document to 'mail' collection to trigger Firebase Extension.
        Assumes 'Trigger Email' extension is installed.
        """
        try:
            # Construct email payload for Firebase Extension
            email_data = {
                "to": [candidate_email],
                "message": {
                    "subject": f"Interview Invitation for {job_title}",
                    "text": f"Dear {candidate_name},\n\nWe were impressed by your profile and would like to invite you for an interview for the {job_title} position.\n\nBest regards,\nRecruitment Team",
                    "html": f"<p>Dear {candidate_name},</p><p>We were impressed by your profile and would like to invite you for an interview for the <strong>{job_title}</strong> position.</p><p>Best regards,<br>Recruitment Team</p>"
                },
                "timestamp": datetime.datetime.now()
            }
            
            # Add to Firestore collection 'mail'
            self.db.collection("mail").add(email_data)
            return True, "Email queued successfully via Firebase!"
        except Exception as e:
            return False, f"Failed to queue email: {str(e)}"
