from scrapping import *
import json
import pandas as pd

def compile_event_data():
    events_data = []
    events_data.append(scrape_event1())
    events_data.append(scrape_event2())
    events_data.append(scrape_event3())
    events_data.append(scrape_event4())
    events_data.append(scrape_event5())
    # Add calls to other scraping functions here, e.g., scrape_event2(), scrape_event3(), etc.
    return events_data

# Compile the data
print("Starting to scrape events...")
events_data = compile_event_data()
print("Finished scraping all events.")

# Save data to JSON
print("Saving data to JSON...")
with open('b2b_events.json', 'w') as json_file:
    json.dump(events_data, json_file, indent=4)
print("Data saved to b2b_events.json.")

# Save data to CSV
print("Saving data to CSV...")
df = pd.DataFrame(events_data)
df.to_csv('b2b_events.csv', index=False)
print("Data saved to b2b_events.csv.")
