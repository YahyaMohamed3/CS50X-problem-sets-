# More pythonic way of doing it
from cs50 import get_string

# Prompt user for text
text = get_string("Text: ")

# Count letters, words, and sentences
letters = sum(char.isalpha() for char in text)
words = len(text.split())
sentences = text.count('.') + text.count('!') + text.count('?')

l = letters / words * 100
s = sentences / words * 100

# Calculate Grade level
index = round(0.0588 * l - 0.296 * s - 15.8)

# Print out Grade level
if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
