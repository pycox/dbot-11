# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
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

#         time.sleep(6)

#         data = []

#         driver.execute_script(
#             "arguments[0].scrollIntoView();",
#             driver.find_element(By.CSS_SELECTOR, "#icims_content_iframe"),
#         )
#         iframe = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "icims_content_iframe"))
#         )
#         driver.switch_to.frame(iframe)
#         time.sleep(6)

#         flag = True

#         driver.find_element(By.CSS_SELECTOR, ".iCIMS_JobsTable .row")

#         while flag:
#             items = driver.find_elements(By.CSS_SELECTOR, ".iCIMS_JobsTable .row")

#             for item in items:
#                 link = (
#                     item.find_element(By.CSS_SELECTOR, "a")
#                     .get_attribute("href")
#                     .strip()
#                 )
#                 location = item.find_elements(By.CSS_SELECTOR, "span")[1].text.strip()

#                 data.append(
#                     [
#                         item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
#                         com,
#                         location,
#                         link,
#                     ]
#                 )

#             try:
#                 button = driver.find_element(
#                     By.CSS_SELECTOR,
#                     'a:not(.invisible) span[title="Next page of results"',
#                 )
#                 driver.execute_script("arguments[0].scrollIntoView();", button)
#                 driver.execute_script("arguments[0].click();", button)
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
                url=f"https://apply.dwfgroup.com/api/jobs?page={page}&sortBy=relevance&descending=false&internal=false&deviceId=undefined&domain=dwfgroup.jibeapply.com",
                verify=False,
                headers=headers,
                timeout=500,
            )

            result = json.loads(response.text)

            posts = result.get("jobs", [])

            if len(posts) == 0:
                flag = False
                break

            for post in posts:
                item = post.get("data", {})

                title = item.get("title", "")
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
