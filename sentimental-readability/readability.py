from cs50 import get_string

# Prompt user for text
t = get_string("Text: ")

# Count letters, words, and sentences
letters = 0
words = 1
sentence = 0
i = 0

lnth = len(t)

# iderrate over the whole text
while i < lnth:
    if t[i].isalpha():  # check if letter is alphbetical if it is add 1 to the letter counter
        letters += 1
    elif t[i] == ' ':  # count words
        words += 1
    elif t[i] == '.' or t[i] == '!' or t[i] == '?':  # count sentences
        sentence += 1
    i += 1

l = letters / words * 100
s = sentence / words * 100

# Calculate Grade level
index = round(0.0588 * l - 0.296 * s - 15.8)

# Print out Grade level
if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
