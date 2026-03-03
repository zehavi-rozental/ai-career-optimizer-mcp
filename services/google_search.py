import requests
import logging
import certifi
import warnings
import urllib3

# Suppress SSL warnings (temporary)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        try:
            import streamlit as st
            api_key = st.secrets.get("GOOGLE_API_KEY")
            search_id = st.secrets.get("SEARCH_ENGINE_ID")
            has_streamlit = True
        except:
            # Running outside of Streamlit context
            import os
            api_key = os.getenv("GOOGLE_API_KEY")
            search_id = os.getenv("SEARCH_ENGINE_ID")
            has_streamlit = False

        if not api_key or not search_id:
            error_msg = "❌ API keys not configured. Please update .streamlit/secrets.toml with GOOGLE_API_KEY and SEARCH_ENGINE_ID"
            if has_streamlit:
                st.error(error_msg)
            else:
                logger.error(error_msg)
            return []

        if not query:
            return []

        url = "https://www.googleapis.com/customsearch/v1"
        params = {'q': query, 'key': api_key, 'cx': search_id, 'num': 5}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=15,
                verify=False  # Disable SSL verification (temporary workaround)
            )
            logger.debug(f"API Response Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                logger.debug(f"Found {len(items)} search results")
                return items
            elif response.status_code == 403:
                error_msg = "❌ API quota exceeded or access forbidden. Check your API key and quota limits."
                if has_streamlit:
                    st.error(error_msg)
                else:
                    logger.error(error_msg)
                logger.error(f"Google API 403 Error: {response.text[:200]}")
                return []
            elif response.status_code == 400:
                error_msg = "❌ Invalid search query or parameters."
                if has_streamlit:
                    st.error(error_msg)
                else:
                    logger.error(error_msg)
                logger.error(f"Google API 400 Error: {response.text[:200]}")
                return []
            else:
                error_msg = f"❌ API Error: Status {response.status_code}"
                if has_streamlit:
                    st.error(error_msg)
                else:
                    logger.error(error_msg)
                logger.error(f"Google API Error {response.status_code}: {response.text[:200]}")
                return []
        except requests.exceptions.Timeout:
            error_msg = "❌ Search request timed out. Please try again."
            if has_streamlit:
                st.error(error_msg)
            else:
                logger.error(error_msg)
            logger.error("Search API timeout")
            return []
        except requests.exceptions.ConnectionError:
            error_msg = "❌ Connection error. Please check your internet connection."
            if has_streamlit:
                st.error(error_msg)
            else:
                logger.error(error_msg)
            logger.error("Searcction error")
            return []
        except requests.exceptions.SSLError as e:
            error_msg = f"❌ SSL Certificate Error: {str(e)[:100]}"
            if has_streamlit:
                st.error(error_msg)
            else:
                logger.error(error_msg)
            logger.debug(f"SSL Error details: {str(e)}")
            return []
        except Exception as e:
            error_msg = f"❌ Search error: {str(e)}"
            if has_streamlit:
                st.error(error_msg)
            else:
                logger.error(error_msg)
            logger.error(f"Unexpected search error: {str(e)}")
            return []