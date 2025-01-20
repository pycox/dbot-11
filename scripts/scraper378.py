from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander
import time


def main(key, com, url):
    options = Options()

    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        time.sleep(4)

        data = []

        flag = True

        dom = driver.find_element(By.CSS_SELECTOR, "div.js-results")

        dom.find_element(By.CSS_SELECTOR, "div.mb-4.col-lg-4.col-12")

        while flag:
            items = dom.find_elements(By.CSS_SELECTOR, "div.mb-4.col-lg-4.col-12")

            for item in items:
                link = (
                    item.find_element(By.CSS_SELECTOR, "a")
                    .get_attribute("href")
                    .strip()
                )
                location = (
                    item.find_element(By.CSS_SELECTOR, "dd")
                    .text.strip()
                    .split("\n")[-1]
                )

                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h4").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )

            try:
                button = driver.find_element(
                    By.CSS_SELECTOR, 'a[aria-label="Next page"]'
                )

                if button.get_attribute("aria-disabled") == "true":
                    flag = False
                else:
                    time.sleep(2)
                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(8)
            except:
                flag = False

        updateDB(key, data)
    except Exception as e:
        print(key, "========", e)
        if "ERR_CONNECTION_TIMED_OUT" in str(e):
            eventHander(key, "CONNFAILED")
        elif "no such element" in str(e):
            eventHander(key, "UPDATED")
        elif "ERR_NAME_NOT_RESOLVED" in str(e):
            eventHander(key, "CONNFAILED")
        else:
            eventHander(key, "UNKNOWN")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

# import requests
# from utils import updateDB, eventHander
# import json
# import time


# def main(key, com, url):
#     try:
#         headers = {
#             "Content-Type": "application/json",
#             "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
#         }

#         response = requests.post(
#             url="https://careers.northhighland.com/_sf/api/v1/jobs/search.json",
#             json={
#                 "job_search": {
#                     "query": "",
#                     "location": {
#                         "address": "",
#                         "radius": 5,
#                         "region": "GB",
#                         "radius_units": "miles",
#                     },
#                     "filters": {
#                         "ec3b2956-1fa7-4c0c-b572-16e51ce20bd1": ["null"],
#                         "d78e0bc3-d1a6-4ae6-948e-3cca7d8494dc": ["null"],
#                         "374742a0-f169-4be5-a2ff-12616a4dca35": ["null"],
#                         "2646ef5c-bfc7-4bf4-9722-531716527df6": ["null"],
#                         "454c3138-ab13-4d6e-9912-8f96ba33f190": ["null"],
#                         "b123789a-cea0-4d00-b56c-de7850fbf677": ["null"],
#                         "5c9d4bbf-e81f-4f4d-b512-e4fd96cfd5f9": ["null"],
#                     },
#                     "commute_filter": {},
#                     "offset": 0,
#                     "jobs_per_page": 12,
#                 }
#             },
#             verify=False,
#             headers=headers,
#             timeout=100,
#         )

#         data = []

#         if response.status_code == 200:
#             obj = json.loads(response.text)
#             total = obj.get("total_size", 0)

#             # Calculate the number of pages needed
#             pages = (total // 20) + (1 if total % 20 != 0 else 0)

#             for i in range(pages):
#                 try:
#                     time.sleep(2)

#                     response = requests.post(
#                         url="https://careers.northhighland.com/_sf/api/v1/jobs/search.json",
#                         json={
#                             "job_search": {
#                                 "query": "",
#                                 "location": {
#                                     "address": "",
#                                     "radius": 5,
#                                     "region": "GB",
#                                     "radius_units": "miles",
#                                 },
#                                 "filters": {
#                                     "ec3b2956-1fa7-4c0c-b572-16e51ce20bd1": ["null"],
#                                     "d78e0bc3-d1a6-4ae6-948e-3cca7d8494dc": ["null"],
#                                     "374742a0-f169-4be5-a2ff-12616a4dca35": ["null"],
#                                     "2646ef5c-bfc7-4bf4-9722-531716527df6": ["null"],
#                                     "454c3138-ab13-4d6e-9912-8f96ba33f190": ["null"],
#                                     "b123789a-cea0-4d00-b56c-de7850fbf677": ["null"],
#                                     "5c9d4bbf-e81f-4f4d-b512-e4fd96cfd5f9": ["null"],
#                                 },
#                                 "commute_filter": {},
#                                 "offset": 12 * i,
#                                 "jobs_per_page": 12,
#                             }
#                         },
#                         verify=False,
#                         headers=headers,
#                         timeout=100,
#                     )

#                     if response.status_code == 200:
#                         obj = json.loads(response.text)
#                         items = obj.get("results", [])

#                         for tmp in items:
#                             post = tmp.get("job")
#                             title = post.get("title")
#                             link = post.get("url_slug")
#                             locations = post.get("addresses")
#                             location = locations.join(", ")

#                             data.append(
#                                 [
#                                     title,
#                                     com,
#                                     location,
#                                     f"https://careers.northhighland.com/jobs/{link}",
#                                 ]
#                             )
#                 except:
#                     continue

#         updateDB(key, data)

#     except Exception as e:
#         print(key, "========", e)
#         eventHander(key, "CONNFAILED")


# if __name__ == "__main__":
#     main()
