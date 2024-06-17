from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Selenium WebDriver
options = Options()
# options.add_argument("--headless")  # Uncomment to run Chrome in headless mode (no GUI)

# Replace with your path to chromedriver executable
chromedriver_path = 'chromedriver-win64/chromedriver.exe'  # Specify the path to your chromedriver executable
service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service, options=options)
driver.set_window_size(600, 800)
driver.get('https://www.saastrannual2024.com/buy-tickets')

# Write the page source to a file for debugging
with open('page_source.html', 'w', encoding='utf-8') as f:
    f.write(driver.page_source)

# Increase the wait time to 20 seconds
wait = WebDriverWait(driver, 20)

# Wait until the element with class 'tickets-total-mobile' is present
try:
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tickets-total-mobile')))
    # Find all <div> elements with class 'tickets-total-mobile'
    row_elements = driver.find_elements(By.CLASS_NAME, 'tickets-total-mobile')

    # Extract prices from nested <h2> elements
    for row_element in row_elements:
        try:
            # Locate the nested <h2> element within the <div class="col-xs-6 text-right">
            price_element = row_element.find_element(By.CSS_SELECTOR, 'div.col-xs-6.text-right h2.currency-display')
            price_text = price_element.text.strip()
            print(price_text)
        except Exception as e:
            print(f"Error extracting price: {e}")
except Exception as e:
    print(f"Error waiting for element: {e}")

# Close the browser
driver.quit()
