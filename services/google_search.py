import urllib.parse
import logging

logger = logging.getLogger(__name__)


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        if not query:
            return []

        # רשימת האתרים המורשים
        target_sites = [
            "gotfriends.co.il",
            "jobinfo.co.il",
            "nisha.co.il",
            "alljobs.co.il",
            "drushim.co.il"
        ]

        # בניית השאילתה
        site_query = " OR ".join([f"site:{site}" for site in target_sites])
        full_query = f"({site_query}) {query}"

        # יצירת הקישור
        encoded_query = urllib.parse.quote(full_query)
        search_url = f"https://www.google.com/search?q={encoded_query}"

        return [{
            'title': f'לחצי כאן לצפייה בתוצאות עבור: {query}',
            'link': search_url,
            'snippet': """חיפוש ממוקד בלוחות המשרות המובילים (גוטפרנדס, נישה, אולג'ובס ועוד). 
התוצאות מותאמות לסינון נטפרי ויוצגו ישירות בגוגל."""
        }]