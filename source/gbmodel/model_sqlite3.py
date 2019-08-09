"""
A simple recipebook flask app.
ata is stored in a SQLite database that looks something like the following:

+------------+------------------+------------+----------------+
| Name       | Email            | signed_on  | message        |
+============+==================+============+----------------+
| John Doe   | jdoe@example.com | 2012-05-28 | Hello world    |
+------------+------------------+------------+----------------+

This can be created with the following SQL (see bottom of this file):

    create table recipebook (title text, author text, signed_on date, prep_time text, ingredients text);

"""
from datetime import date
from .Model import Model
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
        cursor.close()
        return True
