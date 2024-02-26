import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QFileDialog, QMessageBox
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import re

from section import MarkdownSection

def print_to_terminal():
    sections = []
    current_heading = None
    current_content = ""

    # Write to output...
    with open("test-markdown.md",'r', encoding='utf-8') as file:
        
        # Inputted Markdown named to "markdown_input"
        markdown_input = file.read()
        
        # For every line in the input file...
        for line in file:

            # If the line starts with one hashtag, that line is a level one header
            # and we must assign the string following the hashtag to the variable
            # current_heading
            if line.startswith("# "):
                # section = MarkdownSection(current_heading, 1, current_content)
                # sections.append(section)
                current_heading = line.strip("# \n")
                print("Current Heading:  " + current_heading)

            # If the line does not start with one hashtag, everything that follows will be assiged to
            # the variable current_content (the raw content under the header)
            else:
                current_content += line + '\n'

            # If on this line there is something assigned to current_heading (there is a header):
            if current_heading is not None:
                # Create an instance of the identified section
                section = MarkdownSection(current_heading, 1, current_content)
                # Append it to the list of Sections
                sections.append(section)

        # Output the identified section to the GUI
        for section in sections:
            text.setText(f"{section}")