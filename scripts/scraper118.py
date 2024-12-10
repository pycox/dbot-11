import requests
from utils import updateDB, eventHander
import json


def main(key, com, url):
    try:
        response = requests.get(
            "https://api.ashbyhq.com/posting-api/job-board/v7labs.com"
        )

        data = []

        obj = json.loads(response.text)

        result = obj.get("jobs", [])

        for post in result:
            title = post.get("title")
            link = post.get("id")
            location = post.get("location")

            data.append(
                [
                    title,
                    com,
                    location,
                    f"https://jobs.ashbyhq.com/v7labs.com/{link}",
                ]
            )

        updateDB(key, data)

    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
