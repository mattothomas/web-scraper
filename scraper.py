# Install with pip install firecrawl-py
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from typing import Any, Optional, List

app = FirecrawlApp(api_key='[YOUR KEY HERE]')

class NestedModel1(BaseModel):
    date: str
    title: str
    location: str
    time: str
    description: str

class ExtractSchema(BaseModel):
    events: list[NestedModel1]

data = app.extract([
  "https://engr.psu.edu/events/*"
], {
    'prompt': 'Ensure each event includes a date, title, location, time, and description.',
    'schema': ExtractSchema.model_json_schema(),
})


# Scraping using firecrawl. data is now what's below 
"""
{'success': True, 'data': {'events': [{'date': '2025-02-10', 'time': '10:00 a.m.–3:00 p.m.', 'title': 'CareerPREP: In-Person Résumé Review', 'location': '117 Hammond Building', 'description': 'Sign up for a timeslot to have your résumé reviewed by a Penn State alum or employer volunteer! All engineering majors and levels welcome. Plan to bring a printed copy of your résumé.'}, {'date': '2025-02-10', 'time': '', 'title': 'Engineering Career Week', 'location': 'The Penn Stater Hotel & Conference Center', 'description': 'Engineering Career Week events help connect employers with Penn State engineering and technical students who are seeking internship, co-op, and entry-level full-time positions. Students from all engineering majors and degree levels are welcome.'}, {'date': '2025-02-11', 'time': '7:30–8:30 p.m.', 'title': 'Taiwan Semiconductor Manufacturing Company (TSMC) Information Session', 'location': '220 Deike Building', 'description': 'Meet with recruiters and learn about careers at TSMC! All engineering majors. Casual attire.'}, {'date': '2025-02-12', 'time': '6:00–7:00 p.m.', 'title': 'Taiwan Semiconductor Manufacturing Company (TSMC) Green Manufacturing Information Session', 'location': '247 ECoRE', 'description': 'Join this session to learn about the cutting-edge world of green manufacturing at Taiwan Semiconductor Manufacturing Company (TSMC), a global leader in semiconductor production. All engineering majors. Casual attire.'}, {'date': '2025-02-13', 'time': '7:00–8:15 p.m. (ET)', 'title': 'Rise Up & Embark at KPMG Virtual Information Session', 'location': 'via Brazen Connect', 'description': 'Connect one-on-one with a KPMG professional to learn more about the work they do. All majors welcome.'}, {'date': '2025-02-13', 'time': '12:00 noon–12:45 p.m. (ET)', 'title': 'Veeva Virtual Information Session', 'location': 'Virtual', 'description': "In this session, learn about Veeva's impact and Generation Veeva development programs for new graduates, ask questions from a current Associate in Generation Veeva, and explore next steps to apply for summer 2025 and how to keep in touch with the GV Program team. All engineering and science majors welcome."}, {'date': '2025-02-14', 'time': '1:25 p.m.', 'title': 'QuEra: advancing quantum computing with neutral atoms', 'location': '220 Hammond Building', 'description': ''}, {'date': '2025-02-14', 'time': '10:00–11:00 a.m.', 'title': 'Research Experience for Undergraduates Virtual Information Sessions', 'location': 'via Zoom', 'description': 'Are you looking for a way to build your résumé, learn more about your major and future career, and connect with a faculty member in a meaningful way? Consider getting involved in research during your time as an undergraduate student!'}, {'date': '2025-02-19', 'time': '10:00 AM-3:00 PM', 'title': 'Fall in Love with Study Abroad! Engineering Study Abroad Fair', 'location': '', 'description': ''}, {'date': '2025-02-19', 'time': '12:00 PM', 'title': 'The University College Dublin - Virtual Information Session', 'location': '', 'description': ''}, {'date': '2025-02-20', 'time': '10:00 a.m.–4:00 p.m.& West Student Symposium', 'location': 'Penn State University Park', 'description': 'ASCE Student Symposiums are a great way to meet like-minded individuals and network with other schools while having fun. We hope to capture the excitement with our ASCE Student Symposium this year and are grateful to all judges, volunteers, and participating students for allowing this ASCE Student Symposium to happen. We look forward to welcoming 30 ASCE Student Chapters from Delaware, Maryland, Pennsylvania and the DC Metro area to compete in 2025 to compete!'}, {'date': '2025-03-29', 'time': '', 'title': 'ESM Today', 'location': 'EDI Buildng', 'description': 'Student Poster and Oral Presentations Departmental Engagement Keynote Speaker Cash Prizes and Much More!'}, {'date': '2025-05-15', 'time': '', 'title': 'Penn State Study Abroad Applications - Spring 2026', 'location': '', 'description': ''}, {'date': '2025-05-20', 'time': '', 'title': 'industryXchange 2025: Energy', 'location': 'The Nittany Lion Inn', 'description': 'industryXchange 2025: Energy will bring together Penn State faculty, industry leaders, and government agencies to network, discuss industry needs, and explore energy research collaboration opportunities.'}, {'date': '2025-06-16', 'time': '9am - 3pm', 'title': 'CSE Summer Camp - Digital Dreamers: Girls that Bridge Virtual and Physical Worlds', 'location': 'Westgate', 'description': 'Welcome to CSE Summer camp for Girls, an exciting and immersive program designed to inspire and empower young women in the field of computer science and electrical engineering. The camp offers a unique opportunity to explore the cutting-edge worldned to inspire and empower young women in the field of computer science and electrical engineering. The camp offers a unique opportunity to explore the cutting-edge world of digital twins, where technologies like extended reality (XR) are used to seamlessly connect virtual and physical worlds. Participants will be introduced to the fascinating concepts of digital twin , virtual reality (VR) and augmented realityVR) and augmented reality (AR). One of the highlights of the camp is the exploration of digital twin applications in the domain of smart grids, where campers will learn how XR can be used to create virtual replicas of physical systems for monitoring and optimization.'}, {'date': '2025-07-21', 'time': '', 'title': 'EE Summer Camp - APOGEE', 'location': 'TBD', 'description': 'This five day camp, tailored for girls, will give campers an opportunity to experience and explore the exciting world behind our modern, technological society. They will learn about the electronics and signals that surround us every day, get the chance to interact and work with female electrical engineers and students, and be introduced to the hands-on, Do-it-yourself (DIY) culture. Campers will, first and foremost, become Makers! The camp will be tiered, with plenty to explore for both first-timers as well as advanced or returning students.'}]}, 'status': 'completed', 'expiresAt': '2025-02-10T13:47:08.000Z'}
"""

""" ------------------------------------------------------------------------ """

from ics import Calendar, Event
from datetime import datetime
from zoneinfo import ZoneInfo
import re

eastern_tz = ZoneInfo("America/New_York")
calendar = Calendar()

def parse_event_times(event):
    """
    Given an event dict with 'date' and 'time' keys, return a tuple of (begin, end) datetime objects
    with the America/New_York timezone attached.
    
    If the time string is empty or parsing fails, the event will use midnight on the event date.
    """
    date_str = event["date"]
    time_str = event["time"].strip()
    fmt_date = "%Y-%m-%d"
    base_date = datetime.strptime(date_str, fmt_date).replace(tzinfo=eastern_tz)
    
    if not time_str:
        return base_date, base_date

    # Update regex to include hyphen, en dash, and em dash
    parts = re.split(r'\s*[-–—]\s*', time_str)
    
    if len(parts) == 2:
        start_time, end_time = parts[0].strip(), parts[1].strip()
        
        # Replace "noon" with "12:00 PM" if needed
        if "NOON" in start_time.upper():
            start_time = re.sub("(?i)noon", "12:00 PM", start_time)
        if "NOON" in end_time.upper():
            end_time = re.sub("(?i)noon", "12:00 PM", end_time)
        
        # If the start time lacks an AM/PM indicator but the end time has it, append it.
        if not re.search(r'AM|PM', start_time, flags=re.IGNORECASE) and re.search(r'AM|PM', end_time, flags=re.IGNORECASE):
            if "PM" in end_time.upper():
                start_time += " PM"
            elif "AM" in end_time.upper():
                start_time += " AM"
        
        # Clean up each time string
        start_clean = start_time.replace('.', '').upper()
        end_clean = re.sub(r'\(.*?\)', '', end_time.replace('.', '').upper()).strip()
        
        try:
            start_dt = datetime.strptime(f"{date_str} {start_clean}", "%Y-%m-%d %I:%M %p").replace(tzinfo=eastern_tz)
            end_dt = datetime.strptime(f"{date_str} {end_clean}", "%Y-%m-%d %I:%M %p").replace(tzinfo=eastern_tz)
            return start_dt, end_dt
        except ValueError:
            # Fall back to the base date if parsing fails
            return base_date, base_date
    else:
        # Single time value provided – parse and set both start and end to the same time
        try:
            single_clean = time_str.replace('.', '').upper()
            event_dt = datetime.strptime(f"{date_str} {single_clean}", "%Y-%m-%d %I:%M %p").replace(tzinfo=eastern_tz)
            return event_dt, event_dt
        except ValueError:
            return base_date, base_date

# Iterate over each event and create an ICS event with timezone adjustments
for event in data["data"]["events"]:
    ev = Event()
    ev.name = event["title"]
    ev.description = event["description"]
    ev.location = event["location"]

    start, end = parse_event_times(event)
    ev.begin = start
    ev.end = end

    calendar.events.add(ev)

# Write the calendar out to an .ics file
with open("events.ics", "w") as file:
    file.write(str(calendar))