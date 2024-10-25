#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

// Prototype
int calculate_score(string w);

int main(void)
{
    // prompt players for input
    string w1 = get_string("player1: ");
    string w2 = get_string("player2: ");

    // calculate the score of each player
    int s1 = calculate_score(w1);
    int s2 = calculate_score(w2);

    // print out winner
    if (s1 > s2)
    {
        printf("Player 1 wins!\n ");
    }
    else if (s2 > s1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie\n");
    }
}

int calculate_score(string w)
{
    // keep track of score
    int s = 0;

    // Calculate score for each character
    for (int i = 0, n = strlen(w); i < n; i++)
    {
        if (isupper(w[i]))
        {
            s += points[w[i] - 'A'];
        }
        else if (islower(w[i]))
        {
            s += points[w[i] - 'a'];
        }
    }
    return s;
}
