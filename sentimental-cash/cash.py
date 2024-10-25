from cs50 import get_float

while True:
    change = get_float("Change: ")
    if change > 0:
        break

change = round(change * 100)

total_coins = 0

# Calculate number of quarters
while change >= 25:
    total_coins += 1
    change -= 25

# Calculate number of dimes
while change >= 10:
    total_coins += 1
    change -= 10

# Calculate number of nickels
while change >= 5:
    total_coins += 1
    change -= 5

# Calculate number of penneis
while change >= 1:
    change -= 1
    total_coins += 1

print(total_coins)
