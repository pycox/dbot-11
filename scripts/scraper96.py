import requests
from utils import updateDB, eventHander
import json


def main(key, com, url):
    try:
        response = requests.get(
            "https://api.lever.co/v0/postings/RevolutionParts?group=team&mode=json"
        )

        data = []

        obj = json.loads(response.text)

        for category in obj:
            # Access postings under each category
            postings = category.get("postings", [])

            # Extract relevant information from each posting
            for post in postings:
                title = post.get("text")
                link = post.get("hostedUrl")
                location = post["categories"].get("location")

                # Append a dictionary with the desired fields to the job list
                data.append(
                    [
                        title,
                        com,
                        location,
                        link,
                    ]
                )

        updateDB(key, data)

    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
