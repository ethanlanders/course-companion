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
        self.header_total = 1
        

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
    
    def add_subsection(self, subsection):
        self.subsections.append(subsection)
        self.header_total += 1
        
    # Count the number of bold words
    def bold_count(self): 
        bold_pattern = r'\*\*([^\*]+)\*\*'
        bold_matches = re.findall(bold_pattern, self.raw_content)
        bold_num = sum(len(word.split()) for word in bold_matches)
        return bold_num
        
        
    # Count the total number of headers
    def header_count(self):
        header_pattern = r'^#+\s.*'
        header_num = re.findall(header_pattern, self.raw_content, flags=re.MULTILINE)
        return len(header_num)
    
    def italic_count(self): 
        # Regular expression to find italic markdown syntax
        italic_pattern = r'\*([^*]+)\*'
        # Find all matches of italic syntax in the markdown text
        italic_matches = re.findall(italic_pattern, self.raw_content)
        # Count the number of italic occurrences
        num_italics = len(italic_matches)
        return num_italics
    
    def block_quote_count(self):
        #Set up the regex fora block quote @auth ZE
        quote_pattern=r'^>+\s.*'
        #Find all block quotes and count them @auth ZE
        quotes_num = re.findall(quote_pattern,self.raw_content, flags=re.MULTILINE)   
        #return the number of block quotes.@auth ZE
        return len(quotes_num)
   
    def list_count(self):
        # Regular expression to find list markdown syntax
        list_pattern = r'^(\s*)(\*|\+|-|\d+\.)\s+'
        # Splitting content into lines to apply the pattern
        lines = self.raw_content.split('\n')
        
        lists=[]
        current_list = 0
        lists = []
        # Count the number of list occurrences, and tracking list length
        for line in lines:
                if re.match(list_pattern, line):
                    if current_list == 0:
                        current_list = 1
                    else:
                        current_list += 1         
                else:
                    if current_list > 0:
                        # If  current line not in a list add its length to the lists 
                        # reset the current list length
                        lists.append(current_list)
                      
                        current_list = 0
         
        
    
        # Additional check to see if the last list in the document was counted
        if current_list > 0:
            lists.append(current_list)
        num_lists=len(lists)
            
        return num_lists, lists

    # Function to determine if a link is internal or external
    def is_internal_link(self, link):
        return not link.startswith("http") # Check if the link does not start with "http"

    # Function to extract and analyze hyperlinks
    def analyze_hyperlinks(self):
        internal_links = []
        external_links = []

        hyperlink_pattern = r'\[.*?\]\((.*?)\)'

        links = re.findall(hyperlink_pattern, self.raw_content)

        for link in links:
            if self.is_internal_link(link):
                internal_links.append(link)
            else:
                external_links.append(link)

        return internal_links, external_links
    
    # Print string of an instance of the class
    def __str__(self):
        num_lists, list_lengths = self.list_count()
        tab = '    ' * (self.heading_level - 1) #this adds an indent for each level subsection to create an         
        
        # Analyze hyperlinks
        internal_links, external_links = self.analyze_hyperlinks()
        
        section_str = (f"{tab}Heading Level {self.heading_level} Title: {self.heading}\n"
                       f"{tab}* Words: {self.word_count()}\n"
                       f"{tab}* Bold Words: {self.bold_count()}\n"
                       f"{tab}* Sentences: {self.sentence_count()}\n"
                       f"{tab}* Paragraphs: {self.paragraph_count()}\n"
                       f"{tab}* Italics: {self.italic_count()}\n"
                       f"{tab}* Inline Code Blocks: {self.inline_code_count()}\n"
                       f"{tab}* Block Quotes: {self.block_quote_count()}\n"
                       f"{tab}* Internal Links: {'None' if not internal_links else internal_links}\n"    
                       f"{tab}* External Links: {'None' if not external_links else external_links}\n"
                       f"{tab}* Lists: {num_lists}\n")
                       
    
        # Get the lengths of individual lists
        for i, length in enumerate(list_lengths, start=1):
            section_str += f"{tab}   - Length of List {i}: {length}\n"

        # f"Internal Links in '{self.heading}': {self.internal_links}\n"
        # f"External Links in '{self.heading}': {self.external_links}\n"

        return section_str