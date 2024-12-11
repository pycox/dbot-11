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
            url="https://www.palantir.com/api/lever/v1/postings?state=published",
            verify=False,
            headers=headers,
            timeout=500,
        )

        data = []

        obj = json.loads(response.text)

        result = obj.get("data", [])

        for post in result:
            title = post.get("text")
            link = post.get("urls").get("show")
            location = post.get("categories").get("location")

            data.append([title, com, location, link])

        updateDB(key, data)

    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
