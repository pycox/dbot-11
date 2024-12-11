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
#     options.add_argument("--start-maximized")
#     options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
#     )
#     driver = webdriver.Chrome(options=options)

#     try:
#         driver.get(url)

#         time.sleep(4)

#         try:
#             driver.find_element(By.CSS_SELECTOR, "input.js-consent-all-submit").click()
#         except Exception as e:
#             print(f"{key} ==== cookiee button ====: {e}")
#             eventHander(key, "ELEMENT")

#         flag = True
#         data = []

#         while flag:
#             try:
#                 time.sleep(4)

#                 # nextBtn = driver.find_elements(By.CSS_SELECTOR, "a.next")

#                 if len(driver.find_elements(By.CSS_SELECTOR, "a.oj-joblist-more")) > 0:
#                     element = driver.find_element(By.CSS_SELECTOR, "ul.dgt-list-items")
#                     driver.execute_script(
#                         "arguments[0].scrollTop = arguments[0].scrollHeight", element
#                     )
#                     # nextBtn[0].click()
#                 else:
#                     flag = False
#             except:
#                 flag = False

#         time.sleep(4)

#         driver.find_element(By.CSS_SELECTOR, "ul.dgt-list-items > li")[:-1]
#         items = driver.find_elements(By.CSS_SELECTOR, "ul.dgt-list-items > li")[:-1]

#         for item in items:
#             link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
#             location = item.find_element(By.CSS_SELECTOR, "span.location").text.strip()

#             data.append(
#                 [
#                     item.find_element(By.CSS_SELECTOR, "span.title").text.strip(),
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
            "Content-Type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }

        response = requests.post(
            url="https://orange.jobs/jobs/v3/offers/search?lang=en",
            json={
                "index": "1",
                "nb": 10000,
                "latmin": "",
                "latmax": "",
                "lngmin": "",
                "lngmax": "",
                "carto": "",
                "prelisteddomain": [],
                "contract": [],
                "domain": [],
                "place": [],
            },
            verify=False,
            headers=headers,
            timeout=50,
        )

        data = []

        obj = json.loads(response.text)

        result = obj.get("items", [])

        for post in result:
            title = post.get("title")
            link = post.get("id")
            location = post.get("fulllocation")

            data.append(
                [
                    title,
                    com,
                    location,
                    f"https://orange.jobs/jobs/v3/offers/{link}?lang=en",
                ]
            )

        updateDB(key, data)

    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
