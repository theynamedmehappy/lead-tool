import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def scrape_google_maps(query, location, num_results):
    driver = uc.Chrome(headless=True)
    search_url = f"https://www.google.com/maps/search/{query} in {location}"
    driver.get(search_url)
    time.sleep(5)

    # Scroll to load more results
    for _ in range(5):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

    leads = []
    elements = driver.find_elements(By.CLASS_NAME, "hfpxzc")[:num_results]

    for i, el in enumerate(elements):
        try:
            el.click()
            time.sleep(3)

            name = driver.find_element(By.CLASS_NAME, "DUwDvf").text
            try:
                address = driver.find_element(By.CSS_SELECTOR, '[data-item-id="address"]').text
            except:
                address = ""
            try:
                phone = driver.find_element(By.CSS_SELECTOR, '[data-tooltip="Copy phone number"]').text
            except:
                phone = ""
            try:
                website = driver.find_element(By.CSS_SELECTOR, '[data-item-id="authority"]').text
            except:
                website = ""
            try:
                rating = driver.find_element(By.CLASS_NAME, "F7nice").text
            except:
                rating = ""

            leads.append({
                "Name": name,
                "Address": address,
                "Phone": phone,
                "Website": website,
                "Rating": rating,
            })

        except Exception as e:
            print(f"[{i}] Error: {e}")
            continue

    driver.quit()
    df = pd.DataFrame(leads)
    return df
