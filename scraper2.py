from bs4 import BeautifulSoup
import requests
from datetime import datetime

url = "https://www.engr.psu.edu/events/index.aspx"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")


counter = 0
with open("converted_cal_file.ics", "w") as f:
    f.write("BEGIN:VCALENDAR")

while True:
    try:
        elements = doc.find_all(class_="individual-event")[counter]
        counter+=1
        date = elements.find(class_="individual-event-date").p.text.strip()
        title = elements.find(class_= "individual-event-title").p.text.strip()
        detail = elements.find(class_= "individual-event-detail").p.text.strip()
        link = elements.find(class_= "individual-event-detail").a.get('href')

        if ("a.m." not in detail) or ("AM" not in detail) or ("am" not in detail) or ("P.M." not in detail):
            start_time = ""
            end_time = ""

        if "am" in detail or "pm" in detail:
            if " - " in detail:
                hyphen_finder = detail.find(" - ")
                start_time = detail[hyphen_finder-3:hyphen_finder]
                end_time = detail[hyphen_finder+3:]
            elif "-" in detail:
                hyphen_finder = detail.find("-")
                start_time = detail[hyphen_finder-3:hyphen_finder]
                end_time = detail[hyphen_finder+1:]
            if "am" in start_time:
                start_time = "T" + "0" + start_time[0] + "0000"
            elif "pm" in start_time:
                start_time = "T" + str(int(start_time[0])+12) + "0000"
            if "am" in end_time:
                end_time = "T" + "0" + end_time[0] + "0000"
            elif "pm" in end_time:
                end_time = "T" + str(int(end_time[0])+12) + "0000"
            
        if ("AM EDT" in detail):
            if ":" in detail[:2]:
                start_hours = int(detail[:1])
                start_minutes = detail[2:4]
            elif ":" not in detail[:2]:
                start_hours = int(detail[:2])
                start_minutes = detail[3:5]

            if start_hours == 12: # adj for 12am
                start_hours = 0

            end_hours = start_hours + 1 # assume event runs for 1 hour

            start_time = "T" + str(start_hours) + start_minutes + "00"
            end_time = "T" + str(end_hours) + start_minutes + "00"

        elif ("PM EDT" in detail):
            if ":" in detail[:2]:
                start_hours = int(detail[:1])
                start_minutes = detail[2:4]
            elif ":" not in detail[:2]:
                start_hours = int(detail[:2])
                start_minutes = detail[3:5]

            if start_hours != 12:  # Only add 12 if not 12 PM
                start_hours += 12

            end_hours = start_hours + 1

            start_time = "T" + str(start_hours) + start_minutes + "00"
            end_time = "T" + str(end_hours) + start_minutes + "00"

        elif ("AM" in detail):
            dash_finder = detail.find("-")
            start_hours = detail[(dash_finder - 8): (dash_finder - 6)]
            start_minutes = detail[(dash_finder - 5): (dash_finder - 3)]

            if start_hours == 12: # adj for 12am
                start_hours = 0
                
            if (detail[dash_finder + 2] == ":"):
                end_hours = detail[dash_finder + 1:dash_finder + 2]
                if detail[-2:] == "PM":
                    end_hours = int(end_hours) + 12

            start_time = "T" + str(start_hours) + start_minutes + "00"
            end_time = "T" + str(end_hours) + start_minutes + "00"

        if ("p.m." in detail and "a.m." not in detail and "noon" not in detail):
            start_identifier = detail.find("–")
            if " " in detail[start_identifier-5:start_identifier]: 
                start_time = detail[start_identifier-4:start_identifier]
            else:
                start_time = detail[start_identifier-5:start_identifier]
            pm_identifier = detail.find(" p.m.")
            end_time = detail[start_identifier+1:pm_identifier]
            if (len(start_time) == 5):
                past_nine1 = True
            elif(len(start_time) == 4):
                past_nine1 = False
            if past_nine1 == True:
                start_time = "T" + str((int(start_time[0:2]) + 12)) + start_time[3:] + "00"
            else:
                start_time = "T" + str((int(start_time[0:1]) + 12)) + start_time[2:] + "00"
            if (len(end_time) == 5):
                past_nine2 = True
            elif(len(end_time) == 4):
                past_nine2 = False
            if end_time == True:
                end_time = "T" + str((int(end_time[0:2]) + 12)) + end_time[3:] + "00"
            else:
                end_time = "T" + str((int(end_time[0:1]) + 12)) + end_time[2:] + "00"

        if (" a.m." in detail):
            start_identifier = detail.find(" a.m.")
            start_time = detail[start_identifier-5:start_identifier]
            end_identifier = detail.find(" p.m.")

            if (detail[end_identifier - 5] == "–"):
                hyphen_present = True
                end_time = detail[end_identifier-4:end_identifier]
            else:
                hyphen_present = False
                end_time = detail[end_identifier-5:end_identifier]

            start_time = "T" + start_time[0:2] + start_time[3:] + "00"

            if hyphen_present:
                end_time = "T" + str((int(end_time[0:1])+12)) + end_time[2:] + "00"
            else:
                end_time = "T" + str((int(end_time[0:2]))+12) + end_time[3:] + "00"



        if "noon" in detail:
            start_time = "T120000"
            end_time = "T130000"


        day_number = date[4:]
        day_list = day_number.split("-")
        current_year = datetime.now().year
        month = date[:3]
        html_to_ics = {"Jan": "01","Feb":"02","Mar":"03","Apr":"04","May":"05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov":"11","Dec":"12"}
        time_start = str(current_year) + html_to_ics[month] + day_list[0] + start_time
        time_end = str(current_year) + html_to_ics[month] + (day_list[1] if len(day_list) == 2 else day_list[0]) + end_time

        time_start = str(current_year) + html_to_ics[month] + day_list[0] + start_time
        time_end = str(current_year) + html_to_ics[month] + (day_list[1] if len(day_list) == 2 else day_list[0]) + end_time



        with open("converted_cal_file.ics", "a") as f:
            f.write("""
        BEGIN:VEVENT
        DTSTART;TZID=America/New_York: """ + time_start + """
        DTEND;TZID=America/New_York: """ + time_end + """
        SUMMARY: """ + title + """
        DESCRIPTION: https://www.engr.psu.edu/events""" + link + """
        LOCATION:this is a test location
        END:VEVENT
        """)
    except IndexError:
        break

with open("converted_cal_file.ics", "a") as f:
    f.write("END:VCALENDAR")
