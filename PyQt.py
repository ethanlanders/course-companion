import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QFileDialog, QMessageBox
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import re

from section import MarkdownSection

#function to wrap file analysis logic
def read_and_analyze_file():
    sections = []
    current_heading = None
    current_content = ""

    # Open a file dialog for the user to select a  file. File type is restricted to *.md and  All files, All Files (*).
    # 'filepath' is assigned to the path of the selected file. 
    # QFileDialog.getOpenFileName returns a tuple with path and filetype the underscore ignores the the returned filetype
    filepath, _ = QFileDialog.getOpenFileName(filter="Markdown Files (*.md);;All Files (*)")
    if filepath:
        
        '''
        Read an inputted Markdown file, then every time a header is detected in the file,
        create a Section instance (section.py class) and append that instance to the empty 
        list of Sections
        '''
        
        with open(filepath,'r', encoding='utf-8') as file:
            markdown_input = file.read()
            
            for line in file:
                if line.startswith("# "):
                    # section = MarkdownSection(current_heading, 1, current_content)
                    # sections.append(section)
                    current_heading = line.strip("# \n")
                else:
                    current_content += line + '\n'

                if current_heading is not None:
                    section = MarkdownSection(current_heading, 1, current_content)
                    sections.append(section)

            for section in sections:
                text.setText(f"{section}")



        # Count how many words there are in input
        words = markdown_input.split()
        word_count = len(words)

        # Count how many sentences there are in input
        sentences = markdown_input.split('.')
        sentence_count = len(sentences)
        
        # Count how many paragraphs there are in input
        paragraphs = markdown_input.split('\n\n')
        paragraph_count = len(paragraphs)

        # Regular expression to find headers
        header_pattern = r'^#+\s.*'

        # Find all headers 
        headers = len(re.findall(header_pattern, markdown_input, re.MULTILINE))

        # Display the report
        report = f"Words: {word_count}, \nSentences: {sentence_count}, \nParagraphs: {paragraph_count},\nHeaders: {headers}"
        text.setText(report) # displays the report in text 
        
def save_report():
    filepath, _ = QFileDialog.getSaveFileName(filter="Text Files (*.txt);;All Files (*)")
    if filepath:  
        report = text.toPlainText()  # get text from the text widget
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(report) 
      
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
            color: #c5947c;
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

# The buttons defaulted to vertical alignment, 
# I wanted them to be side by side, 
# so this adds a horizontal layout for the buttons
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
