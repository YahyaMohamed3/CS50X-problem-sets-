#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    // Prompt the user for some text
    string t = get_string("Text: ");

    // Count the number of letters, words, and sentences in the text

    int letters = 0;
    int words = 1;
    int sentence = 0;

    // Get length of string

    for (int i = 0, lnth = strlen(t); i < lnth; i++)

    // dont count spaces and commas as letters

    {
        if (isalpha(t[i]))
        {
            letters++;
        }

        else if (t[i] == ' ')
        {
            words++;
        }

        else if (t[i] == '.' || t[i] == '!' || t[i] == '?')
        {
            sentence++;
        }
    }
    // Compute the Coleman-Liau index

    float l = (float) letters / (float) words * 100;
    float s = (float) sentence / (float) words * 100;

    int index = round(0.0588 * l - 0.296 * s - 15.8);

    // Print Grade level
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }

    else if (index > 16)
    {
        printf("Grade 16+\n");
    }

    else
    {
        printf("Grade %i\n", index);
    }
}
