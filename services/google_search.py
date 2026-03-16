import streamlit as st

class GoogleSearchService:
    @staticmethod
    def search_jobs(role):
        # יצירת רשימה של לוחות משרות רלוונטיים לפי התפקיד שהוקלד
        # זה מדמה "סריקה" ומאפשר למשתמש לבחור מקור
        platforms = [
            {
                "title": f"משרות {role} ב-Drushim",
                "link": f"https://www.drushim.co.il/jobs/search/{role}/",
                "source": "דרושים",
                "desc": f"צפי בכל משרות ה-{role} החדשות באתר דרושים."
            },
            {
                "title": f"משרות {role} ב-AllJobs",
                "link": f"https://www.alljobs.co.il/SearchResultsGuest.aspx?description={role}",
                "source": "AllJobs",
                "desc": f"חיפוש משרות {role} בלוח AllJobs."
            },
            {
                "title": f"משרות {role} ב-LinkedIn",
                "link": f"https://www.linkedin.com/jobs/search/?keywords={role}&location=Israel",
                "source": "LinkedIn",
                "desc": "משרות מרשת הלינקדאין בישראל."
            }
        ]
        return platforms