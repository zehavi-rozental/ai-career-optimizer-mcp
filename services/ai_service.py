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

        # כתובת מעודכנת ויציבה
        url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=){api_key}"

        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        if is_json:
            payload["generationConfig"] = {"response_mime_type": "application/json"}

        try:
            res = requests.post(url, json=payload, headers=headers, timeout=30, verify=False)
            res.raise_for_status()

            raw_response = res.json()
            text_out = raw_response['candidates'][0]['content']['parts'][0]['text']

            return json.loads(text_out) if is_json else text_out
        except Exception as e:
            st.error(f"AI Error: {str(e)}")
            return None