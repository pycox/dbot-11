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
    driver.get(url)

    data = []

    if "UK" in locations:

        flag = True
        while flag:
            driver.execute_script("window.scrollBy(0, 10000);")
            time.sleep(4)
            
            items = driver.find_elements(By.CSS_SELECTOR, "#vacancies article.single-job-opportunity")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                data.append(
                    [
                        driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, "h4")).strip(),
                        com,
                        "UK",
                        link,
                    ]
                )
                
            try:
                button = driver.find_element(By.CSS_SELECTOR, 'a.next')
                driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(2)
                driver.execute_script("arguments[0].click();", button)
            except Exception as e:
                flag = False
                print("No More Jobs", e)

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
