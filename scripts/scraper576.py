# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from utils import updateDB, eventHander
# import time


# def main(key, com, url):
#     options = Options()

#     options.add_argument("--log-level=3")
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--enable-unsafe-swiftshader")
#     options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
#     )

#     driver = webdriver.Chrome(options=options)

#     try:
#         driver.get(url)

#         time.sleep(3)

#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#         time.sleep(3)

#         data = []

#         driver.find_element(
#             By.CSS_SELECTOR,
#             ".accordians-container .accordion .accordian-content-container",
#         )
#         items = driver.find_elements(
#             By.CSS_SELECTOR,
#             ".accordians-container .accordion .accordian-content-container",
#         )

#         for item in items:
#             title = item.find_element(By.CSS_SELECTOR, "h2").text.strip().split("-")
#             title = title[0]
#             if len(title) == 1:
#                 location = "UK"
#             else:
#                 location = title[1]
#                 if location != "USA":
#                     location = "UK"

#             link = f"{url}#{item.get_attribute('id')}"

#             data.append(
#                 [
#                     com,
#                     location,
#                     link,
#                 ]
#             )

#         updateDB(key, data)
#     except Exception as e:
#         print(key, "========", e)
#         if "ERR_CONNECTION_TIMED_OUT" in str(e):
#             eventHander(key, "CONNFAILED")
#         elif "no such element" in str(e):
#             eventHander(key, "UPDATED")
#         elif "ERR_NAME_NOT_RESOLVED" in str(e):
#             eventHander(key, "CONNFAILED")
#         else:
#             eventHander(key, "UNKNOWN")
#     finally:
#         driver.quit()


# if __name__ == "__main__":
#     main()


import requests
from utils import updateDB, eventHander
import json


def main(key, com, url):
    try:
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en",
            "companyidentifier": "equiteq",
            "priority": "u=1, i",
            "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }

        response = requests.get(
            url="https://theinsightsfamily.careers.hibob.com/api/job-ad",
            verify=False,
            headers=headers,
            timeout=500,
        )

        data = []

        obj = json.loads(response.text)

        result = obj.get("jobAdDetails", [])

        for post in result:
            title = post.get("title", "")
            link = post.get("id", "")
            location = post.get("country", "")

            data.append(
                [
                    title,
                    com,
                    f"{location}",
                    f"https://theinsightsfamily.careers.hibob.com/jobs/{link}",
                ]
            )

        updateDB(key, data)

    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
