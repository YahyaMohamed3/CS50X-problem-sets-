from cs50 import get_int

while True:
    h = get_int("Height: ")
    if 0 < h < 9:
        break

row = 0
space = 0
column = 0

while row < h:
    row += 1
    space = 0  # Reset space count for each row
    while space < h - row:
        print(" ", end="")
        space += 1

    column = 0  # Reset column count for each row
    while column < row:
        print("#", end="")
        column += 1
    print("  ", end="")

    column = 0
    while column < row:
        print("#", end="")
        column += 1

    print()  # Move to the next line after completing each row
