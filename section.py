"""
* We will probably want to create a count of the number of sub headers contained within the primary header
  (7 level 2 headers contained in this level one header)
* 
"""
import re
class MarkdownSection:
    # Initialize instance of class
    def __init__(self, heading, heading_level, raw_content):
        self.heading = heading
        self.heading_level = heading_level
        self.raw_content = raw_content
        self.subsections = []  # List to hold subsections
        

        

    def word_count(self):
        return len(self.raw_content.split())

    def sentence_count(self):
        #adding additional punctuations to better count sentences, with whitespace following or new line character
        sentence_pattern = r'[.!?](\s+|$)'
        #condition prevent counting new lines as sentences
        return len(re.findall(sentence_pattern, self.raw_content)) if self.raw_content.strip() else 0

    def paragraph_count(self):
        # condition checks to see if p is empty after stripping new line characters, to avoid counting empty paragraph returns
        paragraphs = [p for p in self.raw_content.split('\n\n') if p.strip()]
        return len(paragraphs)
    
    
    def add_subsection(self, subsection):
        self.subsections.append(subsection)
        
        
    # Print string of an instance of the class
    def __str__(self):
        tab = '    ' * (self.heading_level - 1) #this adds an indent for each level subsection to create an         
        section_str = (f"{tab}Heading Level {self.heading_level} Title: {self.heading}\n"
                       f"{tab}* Words: {self.word_count()}\n"
                       f"{tab}* Sentences: {self.sentence_count()}\n"
                       f"{tab}* Paragraphs: {self.paragraph_count()}\n\n"
        )
        return section_str
        # return f"Header: {self.heading},\nHeading Level: {self.heading_level},\nRaw Content: {self.raw_content}"