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
    
    def inline_code_count(self):
        # Regular expression to find inline code blocks
        code_pattern = r'`[^`]+`'
        return len(re.findall(code_pattern, self.raw_content))
    
    def itemized_lists(self):
        lines = self.raw_content.split('\n')
        lists = []
        current_list = 0  #current list's length

        for line in lines:
            # Looking for a list start marker
            if re.match(r'^(\s*)(\*|\+|-|\d+\.)\s+', line):
                if current_list == 0:
                    #initialize new listlength as 1
                    current_list = 1
                else:
                    # Increment the current list's length
                    current_list += 1
            else:
                if current_list > 0:
                    # If  current line not in a list add its length to the lists 
                    # reset the current list length
                    lists.append(current_list)
                    current_list = 0
        
        #check for open list
        if current_list > 0:
            lists.append(current_list)
        
    
        return len(lists), lists

            
    # Print string of an instance of the class
    def __str__(self):
        num_lists, list_lengths = self.itemized_lists()
        tab = '    ' * (self.heading_level - 1) #this adds an indent for each level subsection to create an         
        section_str = (f"{tab}Heading Level {self.heading_level} Title: {self.heading}\n"
                       f"{tab}* Words: {self.word_count()}\n"
                       f"{tab}* Sentences: {self.sentence_count()}\n"
                       f"{tab}* Paragraphs: {self.paragraph_count()}\n"
                       f"{tab}* Inline Code Blocks: {self.inline_code_count()}\n"
                       f"{tab}* Itemized Lists: {num_lists}\n")
        # get the lengths of individual lists
        for i, length in enumerate(list_lengths, start=1):
            section_str += f"{tab}    Length of List {i}: {length}\n"


        return section_str
