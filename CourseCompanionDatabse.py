from datetime import datetime
import sqlite3

#Creating the Database for the CourseCompanion
sqliteConnection = sqlite3.connect('CourseCompanion.db')

cursor = sqliteConnection.cursor()

#Creating tables (Needs further discussion)

materials_table = ''' CREATE TABLE MATERIALS(
    Material_id INT NOT NULL,
    Course_name CHAR(50) NOT NULL,
    Source_File,
    Normalized_File, 
    Date_last_analyzed datetime
)'''

suggestions_table = ''' CREATE TABLE SUGGESTIONS(
    suggestions_id INT NOT NULL,
    entry_id INT NOT NULL,
    suggesgtion_type
)
'''

reports_table = ''' CREATE TABLE REPORTS(
    report_id INT NOT NULL,
    Course_Name CHAR(50) NOT NULL,
    entry_id INT,
)
'''