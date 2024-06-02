# CSV TO CALANDER

## Description

This project utilizes the Google Calendar API to push events onto the user's Google Calendar account from a CSV file. The user needs to provide the CSV file containing the events data, as well as the credentials for the API obtained from Google Cloud OAuth.

Refer to this for help : `https://developers.google.com/calendar/api/quickstart/python`

## Features

- Push events from a CSV file to Google Calendar
- Utilize Google Cloud OAuth for API authentication

## Prerequisites

Before running this project, make sure you have the following:

- Python 3.x installed
- Google Cloud project with Calendar API enabled
- Google Cloud OAuth credentials (client ID and client secret)

## Installation
### NOTE: This Project is a work in progress so the process to get it working is a bit complex for some.

1. Clone the repository on your System
2. Create a `venv` in Python and run `pip install -r requirements.txt`
3. After Creating a OAUTH Credential for the Desktop Application of Calander API save the `.json` in the project directory and name it `CS.json`
4. Run `app.py`
5. Authenticate the user for which you have created the test App. In simple terms login to the Google account you have made the API from.

DONE
