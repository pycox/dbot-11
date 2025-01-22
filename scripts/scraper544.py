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

        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)

        data = []
        regions = ["UK", "US"]

        items = driver.find_elements(
            By.CSS_SELECTOR, ".hhs-accordion-1.accordion-controls"
        )

        for index, location in enumerate(regions):
            try:
                sub_items = items[index].find_elements(By.CSS_SELECTOR, "li a h4")
            except:
                continue

            # location_element = driver.find_element(By.XPATH, "//p[strong[text()='Job Location']]")
            # job_location = location_element.text.split(":")[1].strip()

            for sub_item in sub_items:
                data.append(
                    [
                        sub_item.text.strip(),
                        com,
                        location,
                        url,
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

#         try:
#             driver.find_element(By.CSS_SELECTOR, "#hs-eu-confirmation-button").click()
#         except Exception as e:
#             print(f"{key} ==== cookiee button ====: {e}")
#             eventHander(key, "ELEMENT")

#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#         time.sleep(3)

#         data = []
#         regions = ["UK", "US"]

#         items = driver.find_elements(
#             By.CSS_SELECTOR, ".hhs-accordion-1.accordion-controls"
#         )

#         for sub_item in items:
#             location_element = sub_item.find_element(
#                 By.XPATH, "//p[strong[text()='Job Location']]"
#             )
#             job_location = location_element.text.split(":")[1].strip()

#             data.append(
#                 [
#                     sub_item.text.strip(),
#                     com,
#                     job_location,
#                     url,
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
