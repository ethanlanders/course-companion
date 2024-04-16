import re
from determine_language import CodeLanguageIdentifier


class MarkdownSection:
    """
    Represents a section of Markdown text with various methods to analyze its content.
    """

    def __init__(self, heading, heading_level, raw_content):
        """
        Initialzes an instance of the MarkdownSection class.

        Args:
            heading (str): The heading/title of the Markdown section.
            heading_level (int): The level of the heading (e.g. 1 for top-level, 2 for sub-section, ...)
            raw_content (str): The raw Markdown content of the section.
        """
        self.heading = heading
        self.heading_level = heading_level
        self.raw_content = raw_content
        self.subsections = [] # List to hold subsections
        self.header_total = 1 # Total number of headers in the section.
        
    def word_count(self):
        """Counts the number of words in the raw content."""
        return len(self.raw_content.split())

    def sentence_count(self):
        """Counts the number of sentences in the raw content."""
        sentence_pattern = r'[.!?](\s+|$)'
        return len(re.findall(sentence_pattern, self.raw_content)) if self.raw_content.strip() else 0

    def paragraph_count(self):
        """Counts the number of paragraphs in the raw content."""
        
        # Condition checks to see if p is empty after stripping new line characters to avoid counting empty paragraph returns
        paragraphs = [p for p in self.raw_content.split('\n\n') if p.strip()]
        return len(paragraphs)
    
    def inline_code_count(self):
        """Counts the number of inline code blocks in the raw content."""
        code_pattern = r'`[^`]+`'
        return len(re.findall(code_pattern, self.raw_content))
    
    def add_subsection(self, subsection):
        """Adds a subsection to the current section."""
        self.subsections.append(subsection)
        self.header_total += 1
        
    def bold_count(self): 
        """Counts the total number of bold words in the raw content."""
        bold_pattern = r'\*\*([^\*]+)\*\*'
        bold_matches = re.findall(bold_pattern, self.raw_content)
        bold_num = sum(len(word.split()) for word in bold_matches)
        return bold_num
        
    def header_count(self):
        """Counts the number of headers in the raw content."""
        header_pattern = r'^#+\s.*'
        header_num = re.findall(header_pattern, self.raw_content, flags=re.MULTILINE)
        return len(header_num)
    
    def italic_count(self): 
        """Counts the nubmer of italicized words in the raw content"""

        # Regular expression to find italic markdown syntax
        italic_pattern = r'\*([^*]+)\*'
        # Find all matches of italic syntax in the markdown text
        italic_matches = re.findall(italic_pattern, self.raw_content)
        # Count the number of italic occurrences
        num_italics = len(italic_matches)
        return num_italics
    
    def block_quote_count(self):
        """Counts the number of block quotes in the raw content."""
        # Set up the regex for a block quote.   @auth ZE
        quote_pattern=r'^>+\s.*'
        # Find all block quotes and count them. @auth ZE
        quotes_num = re.findall(quote_pattern,self.raw_content, flags=re.MULTILINE)   
        # Return the number of block quotes.    @auth ZE
        return len(quotes_num)
   
    def list_count(self):
        """Counts the number of lists in the raw content."""

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
                        # If current line not in a list add its length to the lists 
                        # reset the current list length
                        lists.append(current_list)
                      
                        current_list = 0
         
        # Additional check to see if the last list in the document was counted
        if current_list > 0:
            lists.append(current_list)
        num_lists=len(lists)
            
        return num_lists, lists

    def is_internal_link(self, link):
        """Determines if a link is internal or external"""
        return not link.startswith("http") # Check if the link does not start with "http"

    def analyze_hyperlinks(self):
        """Extracts and analyzes hyperlinks in the raw content."""
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

    def analyze_code_blocks(self):
        code_identifier = CodeLanguageIdentifier()
        code_blocks = re.findall(r'```(.*?)```', self.raw_content, re.DOTALL)
        code_languages = []

        for block in code_blocks:
            clean_block = block.strip()
            identified_language = code_identifier.identify_language(clean_block)
            code_languages.append(identified_language)

        return code_blocks, code_languages

    def __str__(self):
        """Generates/prints a string representation of the MarkdownSection object/instance."""
        num_lists, list_lengths = self.list_count()
        tab = '    ' * (self.heading_level - 1)  # This adds an indent for each level subsection to create an
        
        # Analyze hyperlinks
        internal_links, external_links = self.analyze_hyperlinks()
        code_blocks, code_languages = self.analyze_code_blocks()
        section_str = (
            (f"{tab}Heading Level {self.heading_level} Title: {self.heading}\n") + \
            (f"{tab}* Words: {self.word_count()}\n" if self.word_count() > 0 else "") + \
            (f"{tab}* Bold Words: {self.bold_count()}\n" if self.bold_count() > 0 else "") + \
            (f"{tab}* Sentences: {self.sentence_count()}\n" if self.sentence_count() > 0 else "") + \
            (f"{tab}* Paragraphs: {self.paragraph_count()}\n" if self.paragraph_count() > 0 else "") + \
            (f"{tab}* Italics: {self.italic_count()}\n" if self.italic_count() > 0 else "") + \
            (f"{tab}* Inline Code Blocks: {self.inline_code_count()}\n" if self.inline_code_count() > 0 else "") + \
            (f"{tab}* Block Quotes: {self.block_quote_count()}\n" if self.block_quote_count() > 0 else "") + \
            (f"{tab}* Internal Links: {internal_links}\n" if internal_links else "") + \
            (f"{tab}* External Links: {external_links}\n" if external_links else "") + \
            (f"{tab}* Lists: {num_lists}\n" if num_lists > 0 else ""))
        
        # adding individual list length
        for i, length in enumerate(list_lengths, start=1):
            section_str += f"{tab}   - Length of List {i}: {length}\n"
        
        section_str += (f"{tab}* Code Blocks: {len(code_blocks)}\n" if len(code_blocks) > 0 else "")
        
        # adding code block languages
        for i, language in enumerate(code_languages, start=1):
            section_str += f"{tab}   - Code Block {i}: Language - {language}\n"

        # Print flag to user if there are more hyperlinks than words in section
        if (len(internal_links) + len(external_links)) > self.word_count():
            section_str += f"{tab}* There are too many hyperlinks in your input document, considering removing some.\n"
        
        if self.word_count() > 0:
            italics_words_ratio = self.italic_count()/self.word_count()
            bold_words_ratio = self.bold_count()/self.word_count()

            # Print flag to user if italics/word ratio is over 50%
            if italics_words_ratio > 0.08:
                section_str += f"{tab}* There are too many italicized words in this section.\n"

            # Print flag to user if bold_words/total_word ratio is over 50%
            if bold_words_ratio > 0.08:
                section_str += f"{tab}* There are too many bolded words in this section.\n"

        return section_str