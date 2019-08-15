# Copyright 2019 Terry Tower
#

from __future__ import print_function
import datetime
from .Model import Model
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sqlite3


DB_FILE = 'entries.db'    # file for our Database

# If scope needs to be modified, delete token.pickle to create new credentials.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1697OQJ3lvEL4T69jwE_qJK-5E_RZUEtyHIZg5ldOHqk'
SAMPLE_RANGE_NAME = 'Sheet1!A2:E'

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
        Gets all rows from the google spreadsheet
        Each row contains: title, author, preperation time, date, ingredients
        :return: List of dictonary containing all rows of database
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        # cursor.execute("SELECT * FROM recipebook")
        # return cursor.fetchall()


        #    def insert(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        '''
        The file token.pickle stores the user's access and refresh tokens, and
        is created automatically when authorization is completed the first 
        time.
        '''

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        # This is the autorization popup from Quick
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save credentials for next time 
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        
        #start over with empty db
        cursor.execute("delete from recipebook")
        
        response = []
        if not values:
            print('No data found.')
        else:
            for title, author, date, prep_time, ingredients in values:
                params = {'title':title, 
                        'author':author, 
                        'date':datetime.date.today(), 
                        'prep_time':prep_time, 
                        'ingredients':ingredients}
                # These are all strings 
                connection = sqlite3.connect(DB_FILE)
                cursor.execute("insert into recipebook (title, author, signed_on, prep_time, ingredients) VALUES (:title, :author, :date, :prep_time, :ingredients)", params)
                print(title, author, date, prep_time, ingredients)
                connection.commit()
                response.append({title: title, 
                    author: author, 
                    date: date, 
                    prep_time: prep_time, 
                    ingredients: ingredients})
        return response


    if __name__ == '__main__':
        main()
