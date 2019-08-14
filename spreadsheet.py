# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START sheets_quickstart]
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import psycopg2

conn = psycopg2.connect("dbname=zuul host=db.cecs.pdx.edu user=zuul")
cur = conn.cursor()

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1sJVkSBFtpXju13O0CohM0a8T812aq4hldeXddg0NbKE'
SAMPLE_RANGE_NAME = 'ZUUL_May-17-2019!A2:D'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    print(values)

    cur.execute("delete from recipe")

    if not values:
        print('No data found.')
    else:
        for row in values:
            item_name, price, *the_rest = row
            try:
                aliases = [alias.strip()
                           for alias
                           in the_rest[1].split(',')
                           if alias.strip() != '']
            except IndexError:
                aliases = []
            price = float(price.replace('$',''))
            item_name = item_name.strip()
            cur.execute('''insert into items (name, price)
            values (%s, %s)
            on conflict (name) do nothing''', (item_name, price))
            for alias in aliases:
                cur.execute('''
                insert into alias (name, equivalent)
                values (%s, %s)
                on conflict (equivalent) do nothing''', (item_name, alias))
            print(item_name, price, aliases)
            conn.commit()
            # Print columns A and E, which correspond to indices 0 and 4.

if __name__ == '__main__':
    main()
# [END sheets_quickstart]

