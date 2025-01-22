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

        time.sleep(100)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(4)

        data = []

        driver.find_element(By.CSS_SELECTOR, ".job-list-container .job-container")
        items = driver.find_elements(
            By.CSS_SELECTOR, ".job-list-container .job-container"
        )

        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()

            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, ".position-name").text.strip(),
                    com,
                    "UK",
                    link,
                ]
            )

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


# def main(key, com, url):
#     try:
#         headers = {
#             "Content-Type": "application/json",
#             "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
#         }

#         response = requests.get(
#             url="https://gateway.harri.com/core/api/v1/harri_search/search_jobs",
#             verify=False,
#             headers=headers,
#             timeout=500,
#         )

#         data = []

#         obj = json.loads(response.text)

#         result = obj.get("jobAdDetails")
#         posts = result.get("data", {}).get("results", [])

#         for post in posts:
#             title = post.get("position", {}).get("name", "")
#             link = post.get("id", "")
#             locations = post.get("locations", [])
#             location = ", ".join(loc.get("country") for loc in locations)

#             data.append(
#                 [
#                     title,
#                     com,
#                     f"{location}",
#                     f"https://equiteq.careers.hibob.com/{link}",
#                 ]
#             )

#         updateDB(key, data)

#     except Exception as e:
#         print(key, "========", e)
#         eventHander(key, "CONNFAILED")


# if __name__ == "__main__":
#     main()
