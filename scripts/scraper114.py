import requests
from utils import updateDB, eventHander
import json


def main(key, com, url):
    try:
        response = requests.get("https://scopegroup.bamboohr.com/careers/list")

        data = []

        obj = json.loads(response.text)

        result = obj.get("result", [])

        for post in result:
            title = post.get("jobOpeningName")
            link = post.get("id")
            location = post.get("departmentLabel")

            data.append(
                [
                    title,
                    com,
                    location,
                    f"https://scopegroup.bamboohr.com/careers/{link}",
                ]
            )

        updateDB(key, data)

    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
