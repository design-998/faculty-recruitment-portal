import requests
from bs4 import BeautifulSoup

# Ignore SSL certificate warnings


def scrape_iit_indore(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True).lower()

        status = "Open"

        if "extension of last date" in text:
            deadline = "Extended (See Official Advertisement)"
        elif "rolling advertisement" in text:
            deadline = "Rolling Advertisement"
        else:
            deadline = "21 July 2026"

        if "closed" in text:
            status = "Closed"

        return {
            "post": "Assistant Professor / Associate Professor / Professor",
            "eligibility": "Ph.D. in relevant discipline",
            "deadline": deadline,
            "status": status
        }

    except Exception as e:
        print("IIT Indore Error:", e)
        return None
