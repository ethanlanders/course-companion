import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QFileDialog
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 

from section import MarkdownSection

# Function to wrap file analysis logic
def read_and_analyze_file():
    sections = []
    current_heading = None
    current_content = ""
    heading_level = 0 #keeping track of heading level

    # Open a file dialog for the user to select a  file. File type is restricted to *.md and  All files, All Files (*).
    # 'filepath' is assigned to the path of the selected file. 
    # QFileDialog.getOpenFileName returns a tuple with path and filetype the underscore ignores the the returned filetype
    filepath, _ = QFileDialog.getOpenFileName(filter="Markdown Files (*.md);;All Files (*)")
    
    # If a has been selected in the GUI...
    if filepath:
        
        '''
        Read an inputted Markdown file, then every time a header is detected in the file,
        create a Section instance (section.py class) and append that instance to the empty 
        list of Sections
        '''
        
        # Write to output...
        with open(filepath,'r', encoding='utf-8') as file:
            
            # Inputted Markdown named to "markdown_input"
            '''File read wasnt working here because .read() reads the entire file 
            into a single string and puts the pointer at the end of the file so it cannot then
            iterate over it. readlines () reads the file into a list of lines that can be iterated over.'''
            markdown_input = file.readlines()
            
         # For every line in the *markdown input...
        for line in markdown_input:

            # If the line starts with one hashtag, that line is a level one header
            # and we must assign the string following the hashtag to the variable
            # current_heading
            if line.startswith("#"):  # "#" broadens the search for all headers, whereas "# "searches for only top level headers
                #If there is a current heading, append the current section to the section list
                if current_heading is not None:
                    sections.append(MarkdownSection(current_heading, heading_level, current_content))
                    current_content = "" # Reset the content for the next section.
                # Count the number of "#" characters to determine the heading level.
                heading_level = line.count("#")
                ''' We have to strip the "#" and newline characters to get an accurate heading text block'''
                current_heading = line.strip("# \n")
            else:
                current_content += line if line.strip() != '' else '\n\n'


        # If on this line there is something assigned to current_heading (there is a header):
        """after all lines have been processed, then check if there is a section is added  
        Moved this outside of the main loop"""
        if current_heading is not None:
            #append the last section on the section list
            sections.append(MarkdownSection(current_heading, heading_level, current_content))
          
        report = "" # initializes the variable to build the report string

        # Output the identified section to the GUI
        for section in sections:
            report += str(section) #converts each section to a string and appends it to the report
        text.setText(report)

def save_report():
    filepath, _ = QFileDialog.getSaveFileName(filter="Text Files (*.txt);;All Files (*)")
    if filepath:  
        report = text.toPlainText()  # get text from the text widget
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(report) 