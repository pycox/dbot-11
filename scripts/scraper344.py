# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from utils import updateDB, eventHander
# import time
# import undetected_chromedriver as uc
# from selenium_stealth import stealth


# def main(key, com, url):
#     user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Safari/537.36"
#     options = uc.ChromeOptions()
#     options.add_argument("--log-level=3")
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--enable-unsafe-swiftshader")
#     options.add_argument("user-agent={}".format(user_agent))
#     options.add_argument("--disable-blink-features")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument("--disable-dev-shm-usage")

#     driver = uc.Chrome(options=options)

#     stealth(
#         driver,
#         languages=["en-US", "en"],
#         vendor="Google Inc.",
#         platform="Win32",
#         webgl_vendor="Intel Inc.",
#         renderer="Intel Iris OpenGL Engine",
#         fix_hairline=True,
#     )

#     driver.execute_cdp_cmd(
#         "Page.addScriptToEvaluateOnNewDocument",
#         {
#             "source": """
#         Object.defineProperty(navigator, 'webdriver', {
#           get: () => undefined
#         })
#     """
#         },
#     )

#     try:
#         driver.get(url)

#         time.sleep(4)

#         data = []

#         driver.find_element(By.CSS_SELECTOR, 'div."vsr-job')
#         items = driver.find_elements(By.CSS_SELECTOR, 'div."vsr-job')

#         for item in items:
#             link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()

#             data.append(
#                 [
#                     item.find_element(By.CSS_SELECTOR, "a").text.strip(),
#                     com,
#                     "UK",
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


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander
import time
import undetected_chromedriver as uc
from selenium_stealth import stealth


def main(key, com, url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent={}".format(user_agent))
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    # driver.execute_cdp_cmd(
    #     "Page.addScriptToEvaluateOnNewDocument",
    #     {
    #         "source": """
    #     Object.defineProperty(navigator, 'webdriver', {
    #       get: () => undefined
    #     })
    # """
    #     },
    # )

    try:
        driver.get(url)

        time.sleep(4)

        data = []

        driver.find_element(By.CSS_SELECTOR, "div.vsr-job")
        items = driver.find_elements(By.CSS_SELECTOR, "div.vsr-job")

        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()

            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "a").text.strip(),
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
