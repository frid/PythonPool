from datetime import date
from datetime import timedelta


def checkio(from_date, to_date):
    """
        Count the days of rest
    """
    DiffDay = (to_date - from_date).days + 1
    NoRestDay = 0
    for DayShift in range(DiffDay):
        Shift = timedelta(days=DayShift)
        if (from_date + Shift).weekday() > 4:
            NoRestDay+=1
    return NoRestDay

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio(date(2013, 9, 18), date(2013, 9, 23)) == 2, "1st example"
    assert checkio(date(2013, 1, 1), date(2013, 2, 1)) == 8, "2nd example"
    assert checkio(date(2013, 2, 2), date(2013, 2, 3)) == 2, "3rd example"
