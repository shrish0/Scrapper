import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Selenium WebDriver
options = Options()
options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)

# Replace with your path to chromedriver executable
chromedriver_path = 'chromedriver-win64/chromedriver.exe'  # Specify the path to your chromedriver executable
service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service, options=options)


# Function to scrape Event 1
def scrape_event1():
    print("Scraping Event 1...")
    
    # URLs for different pages of Event 1
    main_url = 'https://b2bmarketing.exchange/east/'
    registration_url = 'https://b2bmarketing.exchange/east/registration/'
    agenda_url = 'https://b2bmarketing.exchange/east/agenda/'
    
    # Scrape main event page
    print(f"Fetching main event page: {main_url}")
    main_response = requests.get(main_url)
    main_soup = BeautifulSoup(main_response.content, 'html.parser')
    
    # Event Name
    event_name = main_soup.find('title').text.strip()
    print(f"Event Name: {event_name}")
    
    # Location and Date
    h3_tag = main_soup.find('h3', class_='elementor-heading-title elementor-size-default')
    if h3_tag:
        event_info = h3_tag.text.split('|')
        event_date = event_info[0].strip()
        location = event_info[1].strip()
        print(f"Event Date: {event_date}")
        print(f"Location: {location}")
    else:
        event_date = "N/A"
        location = "N/A"
        print("h3 tag not found.")
    
    # Description
    description_tag = main_soup.find('div', class_='elementor-widget-text-editor')
    description = ""
    if description_tag:
        spans = description_tag.find_all('span', class_='NormalTextRun SCXW261742822 BCX0')
        description = ' '.join(span.text.strip() for span in spans)
    else:
        description = "N/A"
    print(f"Description: {description}")

    # Key Speakers
    key_speakers = [speaker.text.strip() for speaker in main_soup.find_all('div', class_='elementor-slide-heading')]
    print(f"Key Speakers: {key_speakers}")

    # Categories
    registration_response = requests.get(registration_url)
    registration_soup = BeautifulSoup(registration_response.content, 'html.parser')
    categories = [category.text.strip() for category in registration_soup.find_all('h3', class_='elementor-price-table__heading')]
    print(f"Categories: {categories}")

    # Audience Type
    audience_type_tag = main_soup.find('div', class_='audience-type')
    audience_type = audience_type_tag.text.strip() if audience_type_tag else "N/A"
    print(f"Audience type: {audience_type}")

    # Scrape schedule from agenda page
    print(f"Fetching agenda page: {agenda_url}")
    agenda_response = requests.get(agenda_url)
    agenda_soup = BeautifulSoup(agenda_response.content, 'html.parser')
    
    
    # Scrape schedule
    schedule_tags = agenda_soup.find_all('h3', class_='sc-dab8fe09-5 fwiXyw')
    
    schedule = [tag.text.strip() for tag in schedule_tags]
    schedule_text = ', '.join(schedule) if schedule else "N/A"
    print(f"Agenda/Schedule: {schedule_text}")

    # Scrape registration page
    print(f"Fetching registration page: {registration_url}")
    
    
    registration_details_tag = registration_soup.find('div', class_='registration-details')
    registration_details = registration_details_tag.text.strip() if registration_details_tag else "N/A"
    print(f"Registration Details: {registration_details}")
    
    #pricing
    pricing = [ price.text.strip() for price in registration_soup.find_all('span', class_='elementor-price-table__integer-part')]
    print(f"Pricing: {pricing}")

    print("Finished scraping Event 1.")
    
    return {
        'Event Name': event_name,
        'Event Date(s)': event_date,
        'Location': location,
        'Website URL': main_url,
        'Description': description,
        'Key Speakers': key_speakers,
        'Agenda/Schedule': schedule_text,
        'Registration Details': registration_details,
        'Pricing': pricing,
        'Categories': categories,
        'Audience type': audience_type
    }

#function for scrap 2
def scrape_event2():
    print("Scraping Event 2...")
    
    # URLs for different pages of Event 1
    main_url = 'https://www.b2bmarketingexpo.us/'
    speaker_url = 'https://www.b2bmarketingexpo.us/speakers'
    

    main_response = requests.get(main_url)
    main_soup = BeautifulSoup(main_response.content, 'html.parser')
    
    
    meta_tag = main_soup.find('meta', {'property': 'og:site_name'})

    # Extract the content attribute
    if meta_tag and 'content' in meta_tag.attrs:
        event_name = meta_tag['content']
    else:
        print("No meta tag with property 'og:site_name' found")
    print(f"Event Name: {event_name}")
    
    # Location and Date
    article = main_soup.find('article', class_='article--boxed-primary')

    # Extract text from each <p> tag within the article
    info_paragraphs = article.find_all('p')
    info = [p.get_text(strip=True) for p in info_paragraphs]
   # Separate dates and locations
    dates_locations = [info[1], info[2]]

    # Split dates and locations using "-"
    dates_and_locations = [entry.split(' - ') for entry in dates_locations]
    
    # Separate lists for dates and locations
    event_date = [entry[0].strip() for entry in dates_and_locations]
    location = [entry[1].strip() for entry in dates_and_locations]
    print(f"Event Date: {event_date}")
    print(f"Location: {location}")
   
    # Description
    description = main_soup.find('p', class_='ck-intro-text').text.strip()
    print(f"Description: {description}")

    # Key Speakers
    speaker_response = requests.get(speaker_url)
    speaker_soup = BeautifulSoup(speaker_response.content, 'html.parser')
    key_speakers = [speaker.text.strip() for speaker in speaker_soup.find_all('a', class_='m-speakers-list__items__item__header__title__link')]
    print(f"Key Speakers: {key_speakers}")

    # Categories
    categories = [category.text.strip() for category in main_soup.find_all('div', class_='event-category')]
    print(f"Categories: {categories}")

    # Audience Type
    audience_type_tag = main_soup.find('div', class_='audience-type')
    audience_type = audience_type_tag.text.strip() if audience_type_tag else "N/A"
    print(f"Audience type: {audience_type}")

    # Scrape schedule from agenda page 
    schedule_text = [[info[3], info[4]]]
    print(f"Agenda/Schedule: {schedule_text}")

    # Scrape registration page
    print(f"Fetching registration page: ")
    
    try:
        # Replace with the URL of the page you want to scrape
        url = 'https://www.cognitoforms.com/BusinessShowMedia1/TheBusinessShowLA2024Registration'
        driver.get(url)
        
        # Wait for the elements to be present
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'cog-label')))
        
        # Find all label elements with the class "cog-label"
        label_elements = driver.find_elements(By.CLASS_NAME, 'cog-label')
        
        # Extract and clean text from each label element
        registration_details = []
        for label in label_elements:
            clean_text = label.text.replace('\n', ' ').replace('*', '').replace('(required)', '').strip()
            registration_details.append(clean_text)
        
        print("registration details:", registration_details)
        
    finally:
        driver.quit()


    print("Finished scraping Event 2.")
    
    return {
        'Event Name': event_name,
        'Event Date(s)': event_date,
        'Location': location,
        'Website URL': main_url,
        'Description': description,
        'Key Speakers': key_speakers,
        'Agenda/Schedule': schedule_text,
        'Registration Details': registration_details,
        'Pricing': "free",
        'Categories': categories,
        'Audience type': audience_type
    }


# Function to scrape Event 3
def scrape_event3():
    print("Scraping Event 1...")
    
    # URLs for different pages of Event 1
    main_url = 'https://b2bmarketing.exchange/east/'
    registration_url = 'https://b2bmarketing.exchange/east/registration/'
    agenda_url = 'https://b2bmarketing.exchange/east/agenda/'
    
    # Scrape main event page
    print(f"Fetching main event page: {main_url}")
    main_response = requests.get(main_url)
    main_soup = BeautifulSoup(main_response.content, 'html.parser')
    
    # Event Name
    event_name = main_soup.find('title').text.strip()
    print(f"Event Name: {event_name}")
    
    # Location and Date
    h3_tag = main_soup.find('h3', class_='elementor-heading-title elementor-size-default')
    if h3_tag:
        event_info = h3_tag.text.split('|')
        event_date = event_info[0].strip()
        location = event_info[1].strip()
        print(f"Event Date: {event_date}")
        print(f"Location: {location}")
    else:
        event_date = "N/A"
        location = "N/A"
        print("h3 tag not found.")
    
    # Description
    description_tag = main_soup.find('div', class_='elementor-widget-text-editor')
    description = ""
    if description_tag:
        spans = description_tag.find_all('span', class_='NormalTextRun SCXW261742822 BCX0')
        description = ' '.join(span.text.strip() for span in spans)
    else:
        description = "N/A"
    print(f"Description: {description}")

    # Key Speakers
    key_speakers = [speaker.text.strip() for speaker in main_soup.find_all('div', class_='elementor-slide-heading')]
    print(f"Key Speakers: {key_speakers}")

    # Categories
    registration_response = requests.get(registration_url)
    registration_soup = BeautifulSoup(registration_response.content, 'html.parser')
    categories = [category.text.strip() for category in registration_soup.find_all('h3', class_='elementor-price-table__heading')]
    print(f"Categories: {categories}")

    # Audience Type
    audience_type_tag = main_soup.find('div', class_='audience-type')
    audience_type = audience_type_tag.text.strip() if audience_type_tag else "N/A"
    print(f"Audience type: {audience_type}")

    # Scrape schedule from agenda page
    print(f"Fetching agenda page: {agenda_url}")
    agenda_response = requests.get(agenda_url)
    agenda_soup = BeautifulSoup(agenda_response.content, 'html.parser')
    
    
    # Scrape schedule
    schedule_tags = agenda_soup.find_all('h3', class_='sc-dab8fe09-5 fwiXyw')
    
    schedule = [tag.text.strip() for tag in schedule_tags]
    schedule_text = ', '.join(schedule) if schedule else "N/A"
    print(f"Agenda/Schedule: {schedule_text}")

    # Scrape registration page
    print(f"Fetching registration page: {registration_url}")
    
    
    registration_details_tag = registration_soup.find('div', class_='registration-details')
    registration_details = registration_details_tag.text.strip() if registration_details_tag else "N/A"
    print(f"Registration Details: {registration_details}")
    
    #pricing
    pricing = [ price.text.strip() for price in registration_soup.find_all('span', class_='elementor-price-table__integer-part')]
    print(f"Pricing: {pricing}")

    print("Finished scraping Event 1.")
    
    return {
        'Event Name': event_name,
        'Event Date(s)': event_date,
        'Location': location,
        'Website URL': main_url,
        'Description': description,
        'Key Speakers': key_speakers,
        'Agenda/Schedule': schedule_text,
        'Registration Details': registration_details,
        'Pricing': pricing,
        'Categories': categories,
        'Audience type': audience_type
    }


