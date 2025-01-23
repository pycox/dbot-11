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
            url="https://alphapet-ventures.jobs.personio.de/search.json",
            verify=False,
            headers=headers,
            timeout=500,
        )

        data = []

        results = json.loads(response.text)

        for post in results:
            title = post.get("name", "")
            link = post.get("id", "")
            location = post.get("office", "")

            data.append(
                [
                    title,
                    com,
                    location,
                    f"https://alphapet-ventures.jobs.personio.de/{link}",
                ]
            )

        updateDB(key, data)

    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
