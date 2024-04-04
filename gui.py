from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 

class GUI(QWidget):
    def __init__(self):
        super().__init__() #calls the parent parent class constructor, QWidget
        self.initUI()
        self.styles()

    def initUI(self):
        self.setWindowTitle('Markdown Analyzer')  # Title
        self.setGeometry(100, 100, 800, 600)  # Window size and position(x, y, width, height)

        # Creates a main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)  # Set uniform margins
        main_layout.setSpacing(10)  # Set spacing between widgets


        # Adding label to the widget
        label = QLabel('Analysis Report')
        main_layout.addWidget(label)

        # Adds the text area to display reports
        self.text = QTextEdit()  # Allows for multi-line input or display
        main_layout.addWidget(self.text)

        # Adds a horizontal layout to the vertical layout for the buttons
        button_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)  # Reduces default margins for buttons
        button_layout.setSpacing(10)  # Set custom spacing

         # Initialize and add buttons with alignment
        self.initButtons(button_layout)

        # Add the QHBoxLayout which contains the buttons to the main vertical layout
        main_layout.addLayout(button_layout)

        # Sets the main layout
        self.setLayout(main_layout)
   

    def initButtons(self, layout):
        # Creates buttons and adds them to layout
        self.select_button = QPushButton('Select and Analyze File')
        layout.addWidget(self.select_button, alignment=Qt.AlignCenter)

        self.save_button = QPushButton('Save Report')
        layout.addWidget(self.save_button, alignment=Qt.AlignCenter)

        self.history_button = QPushButton('View Report History')
        layout.addWidget(self.history_button, alignment=Qt.AlignCenter)


    def styles(self):
        self.setStyleSheet("""
        QWidget {
            background-color: #454545;
            color: #cccccc;
            font-size: 16px;
            font-weight: 800;
        }
        QPushButton {
            background-color: #2d6198;
            color: white;
            font-size: 16px;
            height: 40px;
            width: 250px;
            border-radius: 3px;
        }
        QPushButton:pressed {
            background-color: #3675b6;
        }
        QTextEdit {
            background-color: #1e1e1e;
            color: #FFFFFF;
            font-size: 14px;
        }
        
        """)


