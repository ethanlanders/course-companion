class MarkdownSection:
    # Initialize instance of class
    def __init__(self, heading, heading_level, raw_content):
        self.heading = heading
        self.heading_level = heading_level
        self.raw_content = raw_content

    # Print string of an instance of the class
    def __str__(self):
        return f"Header: {self.heading},\nHeading Level: {self.heading_level},\nRaw Content: {self.raw_content}"

