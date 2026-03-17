import urllib.parse


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        clean_query = " ".join(query.strip().split())
        encoded_query = urllib.parse.quote(clean_query)

        # פונקציית עזר ליצירת קישור גוגל ממוקד לאתר ספציפי
        def make_smart_link(site_domain):
            return f"https://www.google.com/search?q=site:{site_domain}+{encoded_query}"

        results = [
            {
                "source": "AllJobs",
                "link": make_smart_link("alljobs.co.il"),
                "desc": f"כל משרות {clean_query} מתוך AllJobs"
            },
            {
                "source": "GotFriends",
                "link": make_smart_link("gotfriends.co.il"),
                "desc": f"משרות הייטק ב-GotFriends"
            },
            {
                "source": "Jobinfo",
                "link": make_smart_link("jobinfo.co.il"),
                "desc": f"משרות פיתוח ב-Jobinfo"
            },
            {
                "source": "Nisha",
                "link": make_smart_link("nisha.co.il"),
                "desc": f"משרות דרך קבוצת נישה"
            }
        ]
        return results