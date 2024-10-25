#include <cs50.h>
#include <stdio.h>

int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);

int main(void)
{
    // Prompt the user for change owed, in cents
    int cents;
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    // how many quarters you should give the customer
    int quarters = calculate_quarters(cents);

    // Subtract the value from cents~
    cents = cents - (quarters * 25);

    // how many dimes you should give the customer
    int dimes = calculate_dimes(cents);

    // Subtract the value  rom cents
    cents = cents - (dimes * 10);

    //  how many nickels you should give the customer
    int nickels = calculate_nickels(cents);

    // Subtract the value from cents
    cents = cents - (nickels * 5);

    // Calculate how many pennies
    int pennies = calculate_pennies(cents);

    // Print the total number of coins needed
    printf("%d\n", quarters + dimes + nickels + pennies);
}

int calculate_quarters(int cents)
{
    // Calculate how many quarters you should give the customer
    int quarters = 0;
    while (cents >= 25)
    {
        quarters++;
        cents = cents - 25;
    }
    return quarters;
}

int calculate_dimes(int cents)
{
    // Calculate how many dimes you should give the customer
    int dimes = 0;
    while (cents >= 10)
    {
        dimes++;
        cents = cents - 10;
    }
    return dimes;
}

int calculate_nickels(int cents)
{
    // Calculate how many nickels you should give the customer
    int nickels = 0;
    while (cents >= 5)
    {
        nickels++;
        cents = cents - 5;
    }
    return nickels;
}

int calculate_pennies(int cents)
{
    // Calculate how many pennies you should give the customer
    return cents;
}
