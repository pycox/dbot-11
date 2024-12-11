from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import updateDB, eventHander
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

    time.sleep(3)


    try:
        driver.find_element(By.CSS_SELECTOR, 'button[data-role="all"]').click()
    except:
        print("No Cookie Button")

    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#gnewtonIframe")))
    driver.switch_to.frame(iframe)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)

    data = []
    
    regions = driver.find_elements(By.CSS_SELECTOR, ".gnewtonCareerGroupHeaderClass")
    for region in regions:
        location = region.text.strip()
        for str in locations:
            if (str in location):
                sibling = region.find_element(By.XPATH, "./following-sibling::*[contains(@class, 'gnewtonCareerGroupRowClass')]")
                while sibling and 'gnewtonCareerGroupRowClass' in sibling.get_attribute('class'):
                    link = sibling.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                    data.append(
                        [
                            sibling.find_element(By.CSS_SELECTOR, "a").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    sibling = sibling.find_element(By.XPATH, "./following-sibling::*[contains(@class, 'gnewtonCareerGroupRowClass') or contains(@class, 'gnewtonCareerGroupHeaderClass')]")
                    if sibling and 'gnewtonCareerGroupHeaderClass' in sibling.get_attribute('class'):
                        break
                break

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
