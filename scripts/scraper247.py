from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import updateDB, eventHander
import time


def main(key, com, url, locations):
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(2)

    try:
        driver.find_element(By.CSS_SELECTOR, "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
    except Exception as e:
        print(f"Scraper{key} cookiee button: {e}")

    time.sleep(2)
    data = []
    regions = []

    if "UK" in locations:
        regions.append("United Kingdom")
    if "US" in locations:
        regions.append("United States")
    
    for region in regions:
        Select(driver.find_element(By.CSS_SELECTOR, "select#careers_filter_dropdown")).select_by_value(region)
        driver.find_element(By.CSS_SELECTOR, "input[value=\"Update results\"]").click()
        time.sleep(4)
        
        flag = True
        
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, ".careers-search .careers-featured-cards")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                title = driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, "h3"))
                
                data.append(
                    [
                        title.strip(),
                        com,
                        region,
                        link,
                    ]
                )

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'a.px-4.py-2.border.bg-white.leading-2')
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(4)
            except:
                flag = False
                print("No More Jobs")
        
    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
