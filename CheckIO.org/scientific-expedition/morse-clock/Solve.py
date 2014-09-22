def checkio(time_string):
    time_string = ['{0:02d}'.format(int(tmpStr)) for tmpStr in time_string.split(':')]

    ResultStr = ''
    # Hour
    digitInTenStr = '{0:02b}'.format(int(time_string[0][0])).replace('0', '.').replace('1', '-') + ' '
    ResultStr += digitInTenStr
    digitInOneStr = '{0:04b}'.format(int(time_string[0][1])).replace('0', '.').replace('1', '-') + ' '
    ResultStr += digitInOneStr
    ResultStr += ': '

    # Mins
    digitInTenStr = '{0:03b}'.format(int(time_string[1][0])).replace('0', '.').replace('1', '-') + ' '
    ResultStr += digitInTenStr
    digitInOneStr = '{0:04b}'.format(int(time_string[1][1])).replace('0', '.').replace('1', '-') + ' '
    ResultStr += digitInOneStr
    ResultStr += ': '

    # Secs
    digitInTenStr = '{0:03b}'.format(int(time_string[2][0])).replace('0', '.').replace('1', '-') + ' '
    ResultStr += digitInTenStr
    digitInOneStr = '{0:04b}'.format(int(time_string[2][1])).replace('0', '.').replace('1', '-')
    ResultStr += digitInOneStr

    #replace this for solution
    return ResultStr

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio("10:37:49") == ".- .... : .-- .--- : -.. -..-", "First Test"
    assert checkio("21:34:56") == "-. ...- : .-- .-.. : -.- .--.", "Second Test"
    assert checkio("00:1:02") == ".. .... : ... ...- : ... ..-.", "Third Test"
    assert checkio("23:59:59") == "-. ..-- : -.- -..- : -.- -..-", "Fourth Test"


