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
            url="https://cg-job-search-microservices.azurewebsites.net/api/job-search?page=1&size=10000",
            verify=False,
            headers=headers,
            timeout=500,
        )

        data = []

        obj = json.loads(response.text)

        result = obj.get("data", [])

        for post in result:
            title = post.get("title")
            link = post.get("apply_job_url")
            location = post.get("location")
            country_code = post.get("country_code")

            data.append(
                [
                    title,
                    com,
                    f"{country_code} - {location}",
                    link,
                ]
            )

        updateDB(key, data)

    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
