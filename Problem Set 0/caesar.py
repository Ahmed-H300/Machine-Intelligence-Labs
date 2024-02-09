from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file,read_word_list

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()
    def decipher(word,i):
        deciphered = ''
        base = ord('a')
        for letter in word:
            # deciphered += chr((ord(letter) - i - 97) % 26 + 97)
            deciphered += chr(((ord(letter) - base) - i) % 26 + base)
        return deciphered
        
    dictionarySet = set(dictionary)
    shift = 0
    maxWords = 0
    decipheredText = ''
    cipherList = ciphered.split(' ')
    
    for i in range(26):
        deciphered = ''
        words = 0
        for word in cipherList:
            decipheredWord = decipher(word, i)
            deciphered += (decipheredWord  + ' ')
            if decipheredWord in dictionarySet:
                words += 1
        if words > maxWords:
            decipheredText = deciphered
            maxWords = words
            shift = i

    return (decipheredText[:-1], shift, len(cipherList) - maxWords)








