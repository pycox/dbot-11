from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, "button[data-action='click->common--cookies--alert#disableAll']").click()
    except:
        print("No Cookie Button")

    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    data = []
    
    flag = True
    while flag:
        time.sleep(4)
        try:
            driver.find_element(By.CSS_SELECTOR, "a#show_more_button").click()
        except Exception:
            flag = False
    
    items = driver.find_elements(By.CSS_SELECTOR, "ul#jobs_list_container li")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, ".mt-1.text-md span:nth-child(3)")).strip()
        
        for str in locations:
            if (str in location):
                data.append(
                    [
                        driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, ".text-block-base-link.company-link-style")).strip(),
                        com,
                        str,
                        link,
                    ]
                )
                break


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
