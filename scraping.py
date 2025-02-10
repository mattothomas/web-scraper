import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime

# Define the URL of the Penn State Engineering Events page
url = "https://www.engr.psu.edu/events/"

# Fetch the content of the page
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all the events (you need to inspect the page to find the correct HTML structure)
events = []

# Example: Find all event blocks, this depends on how the HTML is structured on the page
event_blocks = soup.find_all('div', class_='event-details')  # Update this based on actual structure

# Loop through event blocks and extract relevant data
for block in event_blocks:
    date = block.find('span', class_='event-date').text.strip()  # Example of extracting date
    title = block.find('span', class_='event-title').text.strip()  # Example of extracting title
    location = block.find('span', class_='event-location').text.strip()  # Example of location
    description = block.find('p', class_='event-description').text.strip()  # Example of description
    time = block.find('span', class_='event-time').text.strip()  # Example of time
    
    # Convert date and time into proper format (you may need to adjust based on the format)
    event_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %I:%M %p")

    # Add event data to list
    events.append({
        "date": event_datetime,
        "title": title,
        "location": location,
        "description": description
    })

# Create an iCalendar file using the ics library
calendar = Calendar()

# Loop through the events and add them to the calendar
for event in events:
    cal_event = Event()
    cal_event.name = event['title']
    cal_event.begin = event['date']
    cal_event.location = event['location']
    cal_event.description = event['description']
    
    calendar.events.add(cal_event)

# Save the calendar to an ICS file
with open("penn_state_engineering_events.ics", "w") as f:
    f.writelines(calendar)
    
print("ICS file created: penn_state_engineering_events.ics")