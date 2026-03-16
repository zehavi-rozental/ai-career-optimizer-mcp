import requests
import json
import streamlit as st
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AIService:
    @staticmethod
    def get_response(prompt, is_json=True):
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            st.error("Missing API Key in Secrets!")
            return None

        # בנייה נקייה של הכתובת ללא רווחים
        base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        url = f"{base_url}?key={api_key}".strip()

        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        if is_json:
            payload["generationConfig"] = {"response_mime_type": "application/json"}

        try:
            # שימוש ב-Session כדי למנוע בעיות חיבור
            session = requests.Session()
            res = session.post(url, json=payload, headers=headers, timeout=30, verify=False)
            res.raise_for_status()

            raw_response = res.json()
            text_out = raw_response['candidates'][0]['content']['parts'][0]['text']

            if is_json:
                clean_text = text_out.replace('```json', '').replace('```', '').strip()
                return json.loads(clean_text)
            return text_out
        except Exception as e:
            st.error(f"AI Error: {str(e)}")
            return None