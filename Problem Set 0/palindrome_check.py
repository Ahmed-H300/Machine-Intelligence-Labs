import utils

def palindrome_check(string: str) -> bool:
    '''
    This function takes string and returns where a string is a palindrome or not
    A palindrome is a string that does not change if read from left to right or from right to left
    Assume that empty strings are palindromes
    '''
    #DONE: ADD YOUR CODE HERE
    # utils.NotImplemented()
    i, j = 0, len(string) - 1
    while i < j:
        if string[i] != string[j]:
            return False
        i, j = i + 1, j - 1

    return True
