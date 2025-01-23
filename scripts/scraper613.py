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
            url="https://jobs.ajg.com/api/jobs",
            verify=False,
            headers=headers,
            timeout=500,
        )

        data = []

        obj = json.loads(response.text)

        results = obj.get("jobs", [])

        for result in results:
            post = result.get("data", {})
            title = post.get("title", "")
            link = post.get("req_id", "")
            location = post.get("country", "")

            if location == None:
                location = "UK"

            data.append(
                [
                    title,
                    com,
                    location,
                    f"https://jobs.ajg.com/ajg-home/jobs/{link}",
                ]
            )

        updateDB(key, data)

    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
