import requests
from utils import updateDB, eventHander
import json
import time


def main(key, com, url):
    try:
        headers = {
            "Content-Type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }

        response = requests.post(
            url="https://thegymgroup.wd3.myworkdayjobs.com/wday/cxs/thegymgroup/TGG_External_Career_Site/jobs",
            json={"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": ""},
            verify=False,
            headers=headers,
            timeout=100,
        )

        data = []

        if response.status_code == 200:
            obj = json.loads(response.text)
            total = obj.get("total", 0)

            # Calculate the number of pages needed
            pages = (total // 20) + (1 if total % 20 != 0 else 0)

            for i in range(pages):
                try:
                    time.sleep(2)

                    response = requests.post(
                        url="https://thegymgroup.wd3.myworkdayjobs.com/wday/cxs/thegymgroup/TGG_External_Career_Site/jobs",
                        json={
                            "appliedFacets": {},
                            "limit": 20,
                            "offset": i * 20,
                            "searchText": "",
                        },
                        verify=False,
                        headers=headers,
                        timeout=100,
                    )

                    if response.status_code == 200:
                        obj = json.loads(response.text)
                        items = obj.get("jobPostings", [])

                        for post in items:
                            title = post.get("title")
                            link = post.get("externalPath")
                            location = post.get("locationsText", "")

                            data.append(
                                [
                                    title,
                                    com,
                                    location,
                                    f"https://thegymgroup.wd3.myworkdayjobs.com/en-US/TGG_External_Career_Site{link}",
                                ]
                            )
                except:
                    continue

        updateDB(key, data)

    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
