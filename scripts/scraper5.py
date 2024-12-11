from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander


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

        driver.implicitly_wait(4)

        flag = True
        data = []

        while flag:
            try:
                driver.implicitly_wait(4)

                nextBtn = driver.find_elements(By.CSS_SELECTOR, "div#load-more-jobs")

                if len(nextBtn) > 0:
                    nextBtn[0].find_element(By.CSS_SELECTOR, "a").click()
                else:
                    flag = False
            except:
                flag = False

        driver.find_element(By.CSS_SELECTOR, "div.job")

        items = driver.find_elements(By.CSS_SELECTOR, "div.job")

        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            location = item.find_element(By.CSS_SELECTOR, "div.sub-text").text.strip()

            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "a").text.strip(),
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
