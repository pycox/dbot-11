import requests
from utils import updateDB, eventHander
import json


def main(key, com, url):
    try:
        headers = {
            "Content-Type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }

        response = requests.get(
            url="https://irbureau.keka.com/careers/api/embedjobs/default/active/a7a0d531-f154-4753-a2d2-33c0fbd52bd2",
            verify=False,
            headers=headers,
            timeout=500,
        )

        data = []

        result = json.loads(response.text)
        for post in result:
            title = post.get("title")
            link = f"https://irbureau.keka.com/careers/jobdetails/{post.get("id")}"
            locations = post.get("jobLocations", [])
            location = ", ".join(loc.get("countryName") for loc in locations)

            data.append([title, com, location, link])

        updateDB(key, data)

    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
