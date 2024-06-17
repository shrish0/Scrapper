from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Setup Selenium WebDriver
options = Options()
# options.add_argument("--headless")  # Uncomment to run Chrome in headless mode (no GUI)

# Replace with your path to chromedriver executable
chromedriver_path = 'chromedriver-win64/chromedriver.exe'  # Specify the path to your chromedriver executable
service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service, options=options)
driver.set_window_size(600, 800)
driver.get('https://www.saastrannual2024.com/buy-tickets')

# Get the page source
page_source = driver.page_source

# Save page source to a text file
with open('page_source.txt', 'w', encoding='utf-8') as file:
    file.write(page_source)

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find all <span> elements with class 'label-text' and data-test attribute 'rf-form-element-label'
span_elements = soup.find_all('span', {'class': 'label-text', 'data-test': 'rf-form-element-label'})

# Extract and save the text content of each <span> element to a text file
with open('span_elements.txt', 'w', encoding='utf-8') as file:
    for span_element in span_elements:
        span_text = span_element.get_text(strip=True)
        file.write(span_text + '\n')

# Close the browser
driver.quit()
