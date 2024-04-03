from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 

class GUI(QWidget):
    def __init__(self):
        super().__init__() #calls the parent parent class constructor, QWidget
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Markdown Analyzer')  # Title
        self.setGeometry(100, 100, 800, 600)  # Window size and position(x, y, width, height)

        # Creates a main vertical layout
        main_layout = QVBoxLayout()

        # Adding label to the widget
        label = QLabel('Analysis Report')
        main_layout.addWidget(label)

        # Adds the text area to display reports
        self.text = QTextEdit()  # Allows for multi-line input or display
        main_layout.addWidget(self.text)

        # Adds a horizontal layout to the vertical layout for the buttons
        button_layout = QHBoxLayout()

        # Creates a button to select a file
        self.select_button = QPushButton('Select and Analyze File')
        # Adds button to layout
        button_layout.addWidget(self.select_button)

        self.save_button = QPushButton('Save Report')
        button_layout.addWidget(self.save_button)

        # Add the QHBoxLayout which contains the buttons to the main vertical layout
        main_layout.addLayout(button_layout)

        # Sets the main layout
        self.setLayout(main_layout)

    def styles(self, select_button, save_button, text):
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
        self.setStyleSheet("""
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
