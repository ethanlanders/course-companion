# Read in Markdown file
with open("test-markdown.md", encoding = 'utf-8') as f:
    markdown_input = f.read()
    
    # Verify if input was read correctly
    print(markdown_input)

# Count how many words there are in input
words = markdown_input.split()
word_count = len(words)

# Count how many sentences there are in input
sentences = markdown_input.split('.')
sentence_count = len(sentences)

# Count how many paragraphs there are in input
paragraphs = markdown_input.split("\n")
paragraph_count = len(paragraphs)

if len(words)>100:
    with open("output.txt", "w") as file1:
        file1.write("TOO LONG")