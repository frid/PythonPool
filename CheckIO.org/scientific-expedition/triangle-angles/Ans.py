from math import acos, degrees
def checkio(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        return [0, 0, 0]
    find_angle = lambda s1, s2, so: int(round(
        degrees(acos((s1 ** 2 + s2 ** 2 - so ** 2) / (2 * s1 * s2))), 0))
    return sorted([find_angle(a, b, c), find_angle(a, c, b), find_angle(b, c, a)])
if __name__ == '__main__':
    assert checkio(4, 4, 4) == [60, 60, 60], "All sides are equal"
    assert checkio(3, 4, 5) == [37, 53, 90], "Egyptian triangle"
    assert checkio(2, 2, 5) == [0, 0, 0], "It's can not be a triangle"

