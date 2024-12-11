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
#     driver = webdriver.Chrome(options=options)

#     try:
#         driver.get(url)
#         flag = True
#         data = []

#         driver.find_element(By.CSS_SELECTOR, "li.css-1q2dra3")

#         while flag:
#             try:
#                 time.sleep(4)

#                 items = driver.find_elements(By.CSS_SELECTOR, "li.css-1q2dra3")

#                 for item in items:
#                     link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
#                     location = item.find_element(By.CSS_SELECTOR, "dd").text.strip()

#                     data.append(
#                         [
#                             item.find_element(By.CSS_SELECTOR, "a").text.strip(),
#                             com,
#                             location,
#                             link,
#                         ]
#                     )

#                 if (
#                     len(
#                         driver.find_elements(
#                             By.CSS_SELECTOR, "button[data-uxi-element-id='next']"
#                         )
#                     )
#                     > 0
#                 ):
#                     driver.find_element(
#                         By.CSS_SELECTOR, "button[data-uxi-element-id='next']"
#                     ).click()
#                 else:
#                     flag = False
#                     break

#             except Exception as e:
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
            url="https://ntrs.wd1.myworkdayjobs.com/wday/cxs/ntrs/northerntrust/jobs",
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
                        url="https://ntrs.wd1.myworkdayjobs.com/wday/cxs/ntrs/northerntrust/jobs",
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
                                    location,
                                    f"https://ntrs.wd1.myworkdayjobs.com/en-US/northerntrust{link}",
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
