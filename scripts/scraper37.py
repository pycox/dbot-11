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
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(
            "https://www.personio.com/about-personio/careers/#see-our-open-roles"
        )

        driver.implicitly_wait(8)

        try:
            driver.find_element(
                By.XPATH, "//button[contains(text(), 'Accept All')]"
            ).click()
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        flag = True
        data = []

        while flag:
            try:
                driver.implicitly_wait(4)

                nextBtn = driver.find_elements(By.CSS_SELECTOR, "div#careers-load-more")

                if len(nextBtn) > 0:
                    nextBtn[0].find_element(By.CSS_SELECTOR, "a").click()
                else:
                    flag = False
            except:
                flag = False

        driver.find_element(By.CSS_SELECTOR, 'div[data-testid="job-listing"]')
        items = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="job-listing"]')

        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            title = item.find_elements(By.CSS_SELECTOR, "div")[0].text.strip()
            location = item.find_elements(By.CSS_SELECTOR, "div")[1].text.strip()

            data.append(
                [
                    title,
                    com,
                    location,
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
