"""
* We will probably want to create a count of the number of sub headers contained within the primary header
  (7 level 2 headers contained in this level one header)
* 
"""

class MarkdownSection:
    # Initialize instance of class
    def __init__(self, heading, heading_level, raw_content):
        self.heading = heading
        self.heading_level = heading_level
        self.raw_content = raw_content

    def word_count(self):
        return len(self.raw_content.split())

    def sentence_count(self):
        return len(self.raw_content.split('.'))

    def paragraph_count(self):
        return len(self.raw_content.strip().split('\n\n'))

    # Print string of an instance of the class
    def __str__(self):
        return (f"Level {self.heading_level} Header: {self.heading}\n"
                f"Words: {self.word_count()}\n"
                f"Sentences: {self.sentence_count()}\n"
                f"Paragraphs: {self.paragraph_count()}\n\n")

        # return f"Header: {self.heading},\nHeading Level: {self.heading_level},\nRaw Content: {self.raw_content}"