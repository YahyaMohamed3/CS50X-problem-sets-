#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//  command-line argument
int main(int argc, string argv[])
{
    // amke sure there is one command-line argument
    if (argc != 2)
    {
        printf("Usage : ./substitution key\n");
        return 1;
    }
    // Confirm that the consists only of letters
    string key = (argv[1]);

    for (int i = 0; i < strlen(key); i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Only letters are valid\n");
            return 1;
        }
    }
    // Check that input is 26 letters
    if (strlen(key) != 26)
    {
        printf("Enter 26 letters\n");
        return 1;
    }
    // Check that letters dont repeat
    for (int i = 0; i < strlen(key); i++)
    {
        for (int k = i + 1; k < strlen(key); k++)
        {
            if (toupper(key[i]) == toupper(key[k]))
            {
                printf("Letters must not repeat\n");
                return 1;
            }
        }
    }
    // Prompt user for plaintext
    string pt = get_string("Plaintext: ");
    printf("\n");
    printf("ciphertext: ");
    // Convert all lowercase to uppercase
    for (int i = 0; i < strlen(key); i++)
    {
        if (islower(key[i]))
        {
            key[i] -= 32;
        }
    }
    //Cipher Plaintext
    for (int i = 0; i < strlen(pt); i++)
    {

        if (isupper(pt[i]))
        {
            int letters = pt[i] - 65;
            printf("%c", key[letters]);
        }
        else if (islower(pt[i]))
        {
            int letters = pt[i] - 97;
            printf("%c", key[letters] + 32);
        }
        else
        {
            printf("%c", pt[i]);
        }
    }
    printf("\n");
}
