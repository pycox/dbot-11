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

#         flag = True

#         while flag:
#             try:
#                 button = driver.find_element(
#                     By.CSS_SELECTOR,
#                     "#roles-archive > div.min-h-\[300px\] > div > div > div:nth-child(2) > div.mt-10.flex.justify-center.sm\:mt-20 > button",
#                 )
#                 driver.execute_script("arguments[0].scrollIntoView();", button)
#                 driver.execute_script("arguments[0].click();", button)
#                 time.sleep(4)
#             except Exception:
#                 flag = False

#         time.sleep(4)

#         driver.find_element(By.CSS_SELECTOR, "div.grid.grid-cols-1.gap-6 > a")
#         items = driver.find_elements(By.CSS_SELECTOR, "div.grid.grid-cols-1.gap-6 > a")

#         data = []

#         for item in items:
#             link = item.get_attribute("href").strip()
#             location = item.find_element(
#                 By.CSS_SELECTOR, "span.body-small.body-bold.text-grey-secondary"
#             ).text.strip()

#             data.append(
#                 [
#                     item.find_element(By.CSS_SELECTOR, "h4").text.strip(),
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

        flag = True
        page = 1
        data = []

        while flag:
            response = requests.get(
                url=f"https://careers.deliveroo.co.uk/wp-json/wp/v2/roles?_adjust_ids=true&locations_slug=&teams_slug=&order=asc&orderby=title&per_page=20&page={page}",
                verify=False,
                headers=headers,
                timeout=500,
            )

            result = json.loads(response.text)

            if type(result) is not list:
                flag = False
                break

            for post in result:
                title = (
                    post.get("title", {}).get("rendered", "")
                    if isinstance(post.get("title"), dict)
                    else ""
                )
                link = post.get("link", "")
                location = (
                    post.get("meta", {}).get("greenhouse_location", "")
                    if isinstance(post.get("meta"), dict)
                    else ""
                )

                data.append([title, com, location, link])

            page = page + 1

        updateDB(key, data)
    except Exception as e:
        print(key, "========", e)
        eventHander(key, "CONNFAILED")


if __name__ == "__main__":
    main()
