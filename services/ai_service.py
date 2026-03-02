import requests
import json
import streamlit as st


class AIService:
    @staticmethod
    def get_response(prompt, is_json=True):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"response_mime_type": "application/json"} if is_json else {}
        }

        try:
            res = requests.post(url, json=payload, params={'key': api_key}, timeout=30)
            res.raise_for_status()
            return json.loads(res.json()['candidates'][0]['content']['parts'][0]['text'])
        except Exception as e:
            st.error(f"AI Service Error: {e}")
            return None