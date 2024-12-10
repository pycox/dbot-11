import requests
from utils import updateDB, eventHander
import json


def main(key, com, url):
    try:
        response = requests.get(
            "https://gateway.harri.com/core/api/v1/harri_search/search_jobs"
        )

        data = []

        obj = json.loads(response.text)

        result = obj.get("data", {}).get("results", [])

        for post in result:
            title = post.get("position").get("name")
            link = post.get("id", "")

            locations = post.get("locations", [])
            location = ", ".join(loc.get("country") for loc in locations)

            data.append(
                [
                    title,
                    com,
                    location,
                    f"https://harri.com/grind-careers/apply/{link}",
                ]
            )

        updateDB(key, data)

    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
