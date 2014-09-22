from math import acos, pi
def checkio(a, b, c):
    # Convert to float
    a = float(a)
    b = float(b)
    c = float(c)
    # Check triangle
    TriLen = sorted([a, b, c])
    if TriLen[0] + TriLen[1] <= TriLen[2]:
        return [0, 0, 0]
    # Calculate
    Rad2Deg=180/pi
    Alpha = int(round(acos((b**2 + c**2 - a**2)/(2*b*c))*Rad2Deg))
    Beta  = int(round(acos((a**2 + c**2 - b**2)/(2*a*c))*Rad2Deg))
    Gamma = int(round(acos((a**2 + b**2 - c**2)/(2*a*b))*Rad2Deg))

    return sorted([Alpha, Beta, Gamma])


#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio(4, 4, 4) == [60, 60, 60], "All sides are equal"
    assert checkio(3, 4, 5) == [37, 53, 90], "Egyptian triangle"
    assert checkio(2, 2, 5) == [0, 0, 0], "It's can not be a triangle"

