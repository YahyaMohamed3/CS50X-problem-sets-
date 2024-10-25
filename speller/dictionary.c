// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Variables
unsigned int word_count;
unsigned int hash_value;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // use hash to get a hash value
    hash_value = hash(word);

    // point cursor to the first node
    node *cursor = table[hash_value];

    // go through linked list
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned long total = 0;
    for (int i = 0, l = strlen(word); i < l; i++)
    {
        total += tolower(word[i]);
    }
    return total % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO

    // open dictionary
    FILE *source = fopen(dictionary, "r");

    // if it cant be opened return NULL
    if (source == NULL)
    {
        printf("Unable to open %s\n", dictionary);
        return false;
    }
    // declare variable called word to store the word at
    char word[LENGTH + 1];

    // Scan words until we reach the end of the file
    while (fscanf(source, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));

        // if cant allocate memory return false
        if (n == NULL)
        {
            return false;
        }

        // copy word from dic into node
        strcpy(n->word, word);
        hash_value = hash(word);
        n->next = table[hash_value];
        table[hash_value] = n;
        word_count++;
    }
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Return size of dictionary
    if (word_count > 0)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        // set cursor to the start of the linked list
        node *cursor = table[i];
        while (cursor)
        {
            // create temp
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
        if (cursor == NULL)
        {
            return true;
        }
    }
    return false;
}
