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
    driver.maximize_window()

    try:
        driver.get(url)

        driver.implicitly_wait(4)

        subDom = driver.find_element(
            By.CSS_SELECTOR, "div[data-slice='search_results']"
        ).find_element(By.CSS_SELECTOR, "ul")

        subDom.find_element(By.CSS_SELECTOR, "li")
        
        items = subDom.find_elements(By.CSS_SELECTOR, "li")

        data = []

        for item in items:
            item.click()

            driver.find_element(1)

            dom = driver.find_element(
                By.CSS_SELECTOR, 'div[data-testid="hit-result-preview"]'
            )

            location = (
                dom.find_element(By.CSS_SELECTOR, "div.kwJKQC")
                .text.strip()
                .split(",")[-1]
                .strip()
            )
            data.append(
                [
                    dom.find_element(By.CSS_SELECTOR, "p").text.strip(),
                    com,
                    location,
                    driver.current_url,
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
