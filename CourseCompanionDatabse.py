import sqlite3

#Creating the Database for the CourseCompanion
sqliteConnection = sqlite3.connect('CourseCompanion.db')

cursor = sqliteConnection.cursor()
