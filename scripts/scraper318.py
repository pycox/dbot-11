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

#         time.sleep(4)

#         data = []

#         flag = True

#         while flag:
#             items = driver.find_elements(
#                 By.CSS_SELECTOR, "div.job-listing .job-summary"
#             )

#             for item in items:
#                 link = (
#                     item.find_element(By.CSS_SELECTOR, ".job-summary-heading a")
#                     .get_attribute("href")
#                     .strip()
#                 )
#                 location = item.find_element(
#                     By.CSS_SELECTOR, ".job-summary-location"
#                 ).text.strip()

#                 data.append(
#                     [
#                         item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
#                         com,
#                         location,
#                         link,
#                     ]
#                 )

#             try:
#                 driver.find_element(By.CSS_SELECTOR, "li.page-next").click()
#                 time.sleep(4)
#             except:
#                 flag = False

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
            "Content-Type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }

        response = requests.get(
            url="https://careers.dazn.com/postings.json",
            verify=False,
            headers=headers,
            timeout=500,
        )

        data = []

        obj = json.loads(response.text)

        result = obj.get("data", [])

        for post in result:
            title = post.get("title")
            link = f"https://careers.dazn.com{post.get("path")}"
            location = post.get("location").get("name")

            data.append([title, com, location, link])

        updateDB(key, data)

    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
