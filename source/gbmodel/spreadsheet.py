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
# Based on code from Sage Imel

# [START sheets_quickstart]
from __future__ import print_function
from datetime import date
from .Model import Model
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sqlite3


DB_FILE = 'entries.db'    # file for our Database

class model(Model):
    def __init__(self):
        # Make sure our database exists
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("select count(rowid) from recipebook")
        except sqlite3.OperationalError:
            cursor.execute("create table recipebook (title text, author text, signed_on date, prep_time text, ingredients text)")
        cursor.close()

    def select(self):
        """
        Gets all rows from the database
        Each row contains: title, author, preperation time, date, ingredients
        :return: List of lists containing all rows of database
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM recipebook")
        return cursor.fetchall()

    def insert(self, title, author, prep_time, ingredients):
        """
        Inserts entry into database
        :param title: String
        :param author: String
        :param prep_time: String
        :param ingredients: String
        :return: True
        :raises: Database errors on connection and insertion
        """
        params = {'title':title, 'author':author, 'date':date.today(), 'prep_time':prep_time, 'ingredients':ingredients}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("insert into recipebook (title, author, signed_on, prep_time, ingredients) VALUES (:title, :author, :date, :prep_time, :ingredients)", params)
        connection.commit()







# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1697OQJ3lvEL4T69jwE_qJK-5E_RZUEtyHIZg5ldOHqk'
SAMPLE_RANGE_NAME = 'Sheet1!A2:E'

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

    cursor.execute("delete from entries.db")

    if not values:
        print('No data found.')
    else:
        for row in values:
            title, author, date, prep_time, ingrediants
            try:
                alias = [alias.strip()
                           for alias
                           in the_rest[1].split(',')
                           if alias.strip() != '']
            except IndexError:
                aliases = []
            item_name = item_name.strip()
            params = {'title':title, 
                    'author':author, 
                    'date':date.today(), 
                    'prep_time':prep_time, 
                    'ingredients':ingredients}
            
            connection = sqlite3.connect(DB_FILE)
            cursor.execute("insert into recipebook (title, author, signed_on, prep_time, ingredients) VALUES (:title, :author, :date, :prep_time, :ingredients)", params)
            print(title, author, date, prep_time, ingrediants)
            connection.commit()
            # Print columns A and E, which correspond to indices 0 to 4.

if __name__ == '__main__':
    main()
# [END sheets_quickstart]

