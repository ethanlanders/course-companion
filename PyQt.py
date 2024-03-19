import sys
import re # Import the regular expression module

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QFileDialog
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 

from section import MarkdownSection

# Function to filter backslashes from Markdown input
def filter_backslash_lines(markdown_input):
    filtered_lines = []

    for line in markdown_input:
        if not line.startswith("\\"):
            filtered_lines.append(line)
        
    return filtered_lines

# Function to determine if a link is internal or external
def is_internal_link(link):
    return not link.startswith("http") # Check if the link does not start with "http"

# Function to extract and analyze hyperlinks
def analyze_hyperlinks(content):
    internal_links = []
    external_links = []

    hyperlink_pattern = r'\[.*?\]\((.*?)\)'

    links = re.findall(hyperlink_pattern, content)

    for link in links:
        if is_internal_link(link):
            internal_links.append(link)
        else:
            external_links.append(link)

    return internal_links, external_links

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
            
        # Filter out lines starting with a backslash
        filtered_input = filter_backslash_lines(markdown_input)

         # For every line in the *markdown input...
        for line in filtered_input:

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

        with open(filepath, 'w', encoding='utf-8') as f:
            for section in sections:
                internal_links, external_links = analyze_hyperlinks(section.raw_content)
                f.write("Internal Links in '{section.heading}': {internal_links}")
                f.write("External Links in '{section.heading}': {external_links}")

        # Output the identified section to the GUI
        report = "" # initializes the variable to build the report string
        for section in sections:
            report += str(section) # Converts each section to a string and appends it to the report
        text.setText(report)

def save_report():
    filepath, _ = QFileDialog.getSaveFileName(filter="Text Files (*.txt);;All Files (*)")
    if filepath:  
        report = text.toPlainText()  # Get text from the text widget
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report) 

def styles():
    # CSS styles for interface
    select_button.setStyleSheet("""
        QPushButton {
            background-color: #2d6198; 
            color: white; 
            font-size: 16px; 
            height: 40px; 
            border-radius: 3px 
        }
        QPushButton:pressed {
            background-color: #3675b6;
            
        }
    """)
    text.setStyleSheet("""
        QTextEdit {
            background-color: #1e1e1e; 
            color: #FFFFFF;
            font-size: 14px;
            
        }
                        
                            
                            """)
    window.setStyleSheet("""
        QWidget {
            background-color: #454545; 
            color: #cccccc;
            font-size: 16px;
            font-weight: 800;
        }
                        
                            
                            """)
    save_button.setStyleSheet("""
        QPushButton {
            background-color: #2d6198; 
            color: white; 
            font-size: 16px; 
            height: 40px; 
            border-radius: 3px 
        }
        QPushButton:pressed {
            background-color: #3675b6;
            
        }
    """)
#this initializes the GUI
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Markdown Analyzer') #title
window.setGeometry(100, 100, 800, 600)# This sets the window size and position(x, y, width, height)

#creates a main vertical layout
main_layout = QVBoxLayout()

#adding lavel to the widget
label = QLabel('Analysis Report')
main_layout.addWidget(label)

#adds the text area to display reports
text = QTextEdit() #allows for multi-line input or display
main_layout.addWidget(text)

# adds a horizontal layout to the vertical layout for the buttons
button_layout = QHBoxLayout()


#creates an button to select a file
select_button = QPushButton('Select and Analyze File')
#assignes the the read function to the button
select_button.clicked.connect(read_and_analyze_file)
#adds button to layout
button_layout.addWidget(select_button)

save_button = QPushButton('Save Report')
save_button.clicked.connect(save_report)
button_layout.addWidget(save_button)

# Add the QHBoxLayout which contains the buttons to the main vertical layout
main_layout.addLayout(button_layout)

# Setup button styles defined earlier
styles()

#sets the main layout
window.setLayout(main_layout)
window.show()

sys.exit(app.exec_())