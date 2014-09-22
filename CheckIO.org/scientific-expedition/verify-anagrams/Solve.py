def verify_anagrams(first_word, second_word):
    first_word = first_word.lower()
    first_word = first_word.replace(' ', '') # remove space
    second_word = second_word.lower()
    second_word = second_word.replace(' ', '') # remove space
    for char in first_word:
        ind = second_word.find(char)
        if ind != -1:
            second_word = second_word[0:ind] + second_word[ind+1:]
        else:
            return False
    if len(second_word) != 0:
        return False
    else:
        return True
    

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert isinstance(verify_anagrams("a", 'z'), bool), "Boolean!"
    assert verify_anagrams("Programming", "Gram Ring Mop") == True, "Gram of code"
    assert verify_anagrams("Hello", "Ole Oh") == False, "Hello! Ole Oh!"
    assert verify_anagrams("Kyoto", "Tokyo") == True, "The global warming crisis of 3002"


