import string as str
TO_MORSE = str.maketrans('01', '.-')

def to_morse(number, bits):
    """Return number in binary-Morse as a string with the given number of bits."""
    return "{0:0{1}b}".format(number, bits).translate(TO_MORSE)

def to_code(field):
    """Return a space-delimited string of binary-Morse digits."""
    tens, ones = divmod(int(field), 10)
    return "{} {}".format(to_morse(tens, 3), to_morse(ones, 4))

def checkio(data):
    """Return a string representing the time in a Morse code-like form."""
    return ' : '.join(map(to_code, data.split(':')))[1:] # Strip leading .

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio("10:37:49") == ".- .... : .-- .--- : -.. -..-", "First Test"
    assert checkio("21:34:56") == "-. ...- : .-- .-.. : -.- .--.", "Second Test"
    assert checkio("00:1:02") == ".. .... : ... ...- : ... ..-.", "Third Test"
    assert checkio("23:59:59") == "-. ..-- : -.- -..- : -.- -..-", "Fourth Test"


