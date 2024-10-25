#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// just one command-line argument
int main(int argc, string argv[])
{
    // Make sure every character in argv[1] is a digit
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int i = 0, l = strlen(argv[1]); i < l; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf(" ./caesar key\n");
            return 1;
        }
    }
    // change argv from a string to an int

    int key = atoi(argv[1]);

    // prompt user for plaintext(t)

    string t = get_string("Plaintext: ");

    printf("Ciphertext: ");

    for (int i = 0, lnth = strlen(t); i < lnth; i++)
    {
        if (isupper(t[i]))
        {
            printf("%c", (t[i] - 65 + key) % 26 + 65);
        }
        else if (islower(t[i]))
        {
            printf("%c", (t[i] - 97 + key) % 26 + 97);
        }
        else if (ispunct(t[i]) || isblank(t[i]))
        {
            printf("%c", t[i]);
        }
    }
    printf("\n");
}
