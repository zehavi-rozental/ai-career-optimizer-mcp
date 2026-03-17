import requests
import json
import streamlit as st


class AIService:
    @staticmethod
    def get_response(prompt):
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            return None

        # ניקוי רווחים מהמפתח ובניית URL תקין
        api_key = api_key.strip()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"response_mime_type": "application/json"}
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            text_out = response.json()['candidates'][0]['content']['parts'][0]['text']
            return json.loads(text_out)
        except Exception as e:
            st.error(f"AI Error: {str(e)}")
            return None