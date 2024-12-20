from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
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
    
    data = []
    regions = []
    
    if "UK" in locations:
        regions.append(("29247e57dbaf46fb855b224e03170bc7", "UK"))
    
    if "US" in locations:
        regions.append(("bc33aa3152ec42d4995f4791a106ed09", "US"))
    
    for location_id, location in regions:
        driver.get(f"{url}?locationCountry={location_id}")
        time.sleep(6)

        flag = True
        while flag:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            items = driver.find_elements(By.CSS_SELECTOR, "li.css-1q2dra3")
            for item in items:
                try:
                    link = item.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href").strip()
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                except:
                    continue

            try:
                driver.find_element(By.CSS_SELECTOR, 'button[aria-label="next"]').click()
            except:
                flag = False
                print("No More Jobs")

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
