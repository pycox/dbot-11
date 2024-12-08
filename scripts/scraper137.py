from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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

    data = []
    regions = []

    if "UK" in locations:
        regions.append("United Kingdom")
    if "US" in locations:
        regions.append("United States")
    
    button = driver.find_element(By.CSS_SELECTOR, "div[data-filter=\"city.id\"] .sidebar__filter-title-toggle")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    driver.execute_script("arguments[0].click();", button)
    time.sleep(3)

    for region in regions:
        span_element = driver.find_element(By.CSS_SELECTOR, f'span[data-original-title="{region}"]')
        driver.execute_script("arguments[0].scrollIntoView();", span_element)
        checkbox = span_element.find_element(By.XPATH, "./preceding-sibling::div//input[@type='checkbox']")
        checkbox.click()
        time.sleep(4)

    flag = True
    
    if regions:
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "#jobs-accordion .card")
            for item in items:
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".card-header__job-position").text.strip(),
                        com,
                        item.find_element(By.CSS_SELECTOR, ".card-header__job-place").text.strip(),
                        item.find_element(By.CSS_SELECTOR, "a.job-link-open").get_attribute("href").strip(),
                    ]
                )
            
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'a.page-next')
                if "page-link__disabled" in next_button.get_attribute("class"):
                    flag = False
                else:
                    driver.execute_script("arguments[0].click();", next_button)
                    
                time.sleep(4)
            except Exception as e:
                flag = False
                print("No More Jobs", e)
    
    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
