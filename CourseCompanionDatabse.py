import sqlite3

#Creating the Database for the CourseCompanion
sqliteConnection = sqlite3.connect('CourseCompanion.db')

cursor = sqliteConnection.cursor()

#Creating tables (Needs further discussion)
materials_table = ''' CREATE TABLE MATERIALS(
    MATERIAL_ID = INT NOT NULL,
    
    
)'''

suggestions_table = ''' CREATE TABLE SUGGESTIONS(
    
)
'''

reports_table = ''' CREATE TABLE REPORTS(
    
)
'''