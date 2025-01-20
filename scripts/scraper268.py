# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import Select
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
#         regions = []

#         if "UK" in locations:
#             regions.append(("London", "031b2e9d653801a327cde1b30a0126b5"))

#         for location, location_id in regions:
#             try:
#                 driver.find_element(
#                     By.CSS_SELECTOR, "button[data-automation-id='distanceLocation']"
#                 ).click()
#                 time.sleep(2)
#                 driver.find_element(
#                     By.CSS_SELECTOR, f"label[for='{location_id}']"
#                 ).click()
#                 time.sleep(2)
#                 driver.find_element(
#                     By.CSS_SELECTOR, "button[data-automation-id='viewAllJobsButton'"
#                 ).click()
#                 time.sleep(3)
#             except:
#                 continue

#             flag = True

#             while flag:
#                 items = driver.find_elements(By.CSS_SELECTOR, "li.css-1q2dra3")
#                 for item in items:
#                     link = (
#                         item.find_element(By.CSS_SELECTOR, "h3 a")
#                         .get_attribute("href")
#                         .strip()
#                     )
#                     data.append(
#                         [
#                             item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
#                             com,
#                             location,
#                             link,
#                         ]
#                     )

#                 try:
#                     driver.execute_script(
#                         "arguments[0].click();",
#                         driver.find_element(
#                             By.CSS_SELECTOR, 'button[data-uxi-element-id="next"]'
#                         ),
#                     )

#                     time.sleep(4)
#                 except:
#                     flag = False

#             try:
#                 driver.find_element(
#                     By.CSS_SELECTOR, 'button[data-automation-id="clearAllButton"]'
#                 ).click()
#             except:
#                 pass

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


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import Select
# from utils import updateDB, eventHander
# import time


# def main(key, com, url):

#     options = Options()
#     options.add_argument("--log-level=3")
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--enable-unsafe-swiftshader")
#     driver = webdriver.Chrome(options=options)

#     try:
#         driver.get(url)

#         time.sleep(4)

#         data = []

#         flag = True

#         driver.find_element(By.CSS_SELECTOR, "li.css-1q2dra3")

#         while flag:
#             items = driver.find_elements(By.CSS_SELECTOR, "li.css-1q2dra3")
#             for item in items:
#                 link = (
#                     item.find_element(By.CSS_SELECTOR, "h3 a")
#                     .get_attribute("href")
#                     .strip()
#                 )

#                 try:
#                     location = item.find_element(
#                         By.CSS_SELECTOR, ".css-248241 .css-129m7dg"
#                     ).text.strip()
#                 except:
#                     continue

#                 data.append(
#                     [
#                         item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
#                         com,
#                         location,
#                         link,
#                     ]
#                 )

#             try:
#                 driver.find_element(
#                     By.CSS_SELECTOR, 'button[aria-label="next"]'
#                 ).click()
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
                            location = post.get("locationsText")

                            data.append(
                                [
                                    title,
                                    com,
                                    f"UK - {location}",
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
