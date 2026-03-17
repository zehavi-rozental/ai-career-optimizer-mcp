import urllib.parse


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        clean_query = " ".join(query.split())
        encoded_query = urllib.parse.quote(clean_query)

        # בניית הקישורים לאתרים שהגדרת בלבד
        results = [
            {
                "source": "AllJobs",
                "link": f"https://www.alljobs.co.il/SearchResultsGuest.aspx?keywords={encoded_query}",
                "desc": f"משרות {clean_query} בלוח AllJobs"
            },
            {
                "source": "GotFriends",
                "link": f"https://www.gotfriends.co.il/jobs-list/?search={encoded_query}",
                "desc": f"משרות הייטק ממוקדות ב-GotFriends"
            },
            {
                "source": "Jobinfo",
                "link": f"https://www.jobinfo.co.il/jobs?q={encoded_query}",
                "desc": f"חיפוש משרות ב-Jobinfo"
            },
            {
                "source": "Nisha",
                "link": f"https://www.nisha.co.il/jobs?search={encoded_query}",
                "desc": f"משרות דרך קבוצת נישה"
            }
        ]
        return results