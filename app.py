from datetime import datetime
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import pytz
import os
from datetime import datetime, timedelta
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


kolkata = pytz.timezone('Asia/Kolkata')
now = datetime.now(kolkata)  
if now.isoweekday() < 7:  # If today is not Sunday
    current_week_start = now - timedelta(days=now.isoweekday() - 1)
else:  # If today is Sunday
    current_week_start = now+timedelta(days=1)


day_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4}


calander_path = './timeTable.csv'
data = pd.read_csv(calander_path)


def create_event(summary, location, description, start_time, end_time):
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 5},
            ],
        },
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }
    return event

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('CS.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        
    try:
        # Build the service object
        service = build('calendar', 'v3', credentials=creds)
        
        
        for index, row in data.iterrows():
            day = row['Day']
            time_range = row['Time']
            subject = row['Subject']
            location = row['Location']
            instructor = row['Instructor']
            
            # Split the time range to get start and end times
            start_time_str, end_time_str = time_range.split('-')
            start_time = datetime.strptime(start_time_str, '%H:%M')
            end_time = datetime.strptime(end_time_str, '%H:%M')
            
            # Adjust the start_time and end_time to match the current week's corresponding day in 'Asia/Kolkata' timezone
            # Split the time range to get start and end times
            start_time_str, end_time_str = time_range.split('-')
            start_hour, start_minute = map(int, start_time_str.split(':'))
            end_hour, end_minute = map(int, end_time_str.split(':'))

            # Create start_time and end_time with the correct date and timezone
            start_time = kolkata.localize(datetime(year=current_week_start.year, month=current_week_start.month, day=current_week_start.day + day_map[day], hour=start_hour, minute=start_minute))
            end_time = kolkata.localize(datetime(year=current_week_start.year, month=current_week_start.month, day=current_week_start.day + day_map[day], hour=end_hour, minute=end_minute))

            # Create the event
            event = create_event(subject, location, instructor, start_time, end_time)
            
            # Add the event to the Google Calendar
            event = service.events().insert(calendarId='primary', body=event).execute()
            print(f"Event created: {event.get('htmlLink')}")
        
        print("All events created successfully.")
        
        
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()