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
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        driver.implicitly_wait(8)

        flag = True
        data = []

        driver.find_element(By.CSS_SELECTOR, "div.career-hold")

        while flag:
            try:
                driver.implicitly_wait(4)

                items = driver.find_elements(By.CSS_SELECTOR, "div.career-hold")

                for item in items:
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "h5").text.strip(),
                            com,
                            item.find_element(By.XPATH, "//div[strong = 'Location:']")
                            .text.split(":", 1)[1]
                            .strip(),
                            item.find_element(By.CSS_SELECTOR, "a").get_attribute(
                                "href"
                            ),
                        ]
                    )

                nextBtn = driver.find_element(
                    By.CSS_SELECTOR, "ul.pagination"
                ).find_elements(By.CSS_SELECTOR, "li")[-2]

                if not "disabled" in nextBtn.get_attribute("class"):
                    nextBtn.click()
                else:
                    flag = False
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
