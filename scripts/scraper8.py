from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander
from bs4 import BeautifulSoup


def main(key, com, url):
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        driver.implicitly_wait(8)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # try:
        #     driver.find_element(By.CSS_SELECTOR, "button[role='dialog']").find_element(
        #         By.CSS_SELECTOR, "button"
        #     ).click()
        # except Exception as e:
        #     print(f"{key} ==== cookiee button ====: {e}")
        #     eventHander(key, "ELEMENT")

        # flag = True
        data = []

        # while flag:
        #     try:
        #         driver.implicitly_wait(4)

        #         nextBtn = driver.find_elements(
        #             By.CSS_SELECTOR, "button.news__load-more"
        #         )

        #         if len(nextBtn) > 0:
        #             nextBtn[0].click()
        #         else:
        #             flag = False
        #     except:
        #         flag = False

        driver.find_element(By.CSS_SELECTOR, "div.jobs__card")
        items = soup.select("div.jobs__card")

        for item in items:
            link = item.select_one("a").get("href").strip()

            data.append(
                [
                    item.select_one("h2").text.strip(),
                    com,
                    "GB",
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
