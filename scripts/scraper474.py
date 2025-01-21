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

#         try:
#             driver.find_element(By.CSS_SELECTOR, "button#cookie-acknowledge").click()
#         except Exception as e:
#             print(f"{key} ==== cookiee button ====: {e}")
#             eventHander(key, "ELEMENT")

#         time.sleep(4)

#         data = []

#         regions = []

#         regions.append(("UK", "GB"))

#         regions.append(("US", "US"))

#         for location, location_code in regions:
#             driver.get(f"{url}?optionsFacetsDD_country={location_code}")

#             time.sleep(4)

#             flag = True

#             while flag:
#                 try:
#                     driver.find_element(By.CSS_SELECTOR, "#tile-more-results").click()
#                     time.sleep(7)
#                 except Exception:
#                     flag = False

#             items = driver.find_elements(By.CSS_SELECTOR, ".row.job.job-row")

#             for item in items:
#                 link = (
#                     item.find_element(By.CSS_SELECTOR, "a")
#                     .get_attribute("href")
#                     .strip()
#                 )

#                 data.append(
#                     [
#                         item.find_element(By.CSS_SELECTOR, ".tiletitle a").text.strip(),
#                         com,
#                         location,
#                         link,
#                     ]
#                 )

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

        flag = True
        page = 1
        data = []

        while flag:
            response = requests.get(
                url=f"https://career.globant.com/api/sap/job-requisition?&page={page}",
                verify=False,
                headers=headers,
                timeout=500,
            )

            result = json.loads(response.text)

            posts = result.get("jobRequisition", [])

            if len(posts) == 0:
                flag = False
                break

            for post in posts:
                item = post.get("data", {})

                title = item.get("jobTitle", "")
                link = item.get("req_id", "")
                location = item.get("country", "")

                data.append(
                    [
                        title,
                        com,
                        location,
                        f"https://apply.dwfgroup.com/careers-home/jobs/{link}",
                    ]
                )

            page = page + 1

        updateDB(key, data)
    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
