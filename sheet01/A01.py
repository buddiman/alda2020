# Christopher Höllriegl / Marvin Schmitt
# Mittwoch 14 Uhr (Lübbe)
# Blatt 1
# Aufgabe 1

from datetime import datetime

# Aufgabe 1a

tageProMonat = [31,28,31,30,31,30,31,31,30,31,30,31]    # notiz: in Zukunft Englisch oder Deutsch bei der Benennung
daysNames = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]

def friday13():
    print("Alle Möglichkeiten der Freitage die auf einen 13. fallen:\n\n")
    # normale Jahre
    print("Normale Jahre:")
    for first in range(7):      # 7 days
        day = first
        counter = 0
        for month in range(12):
            if day%7 == 6:      # if first of month is sunday then there is a friday the 13th
                counter += 1
            day += tageProMonat[month]
        print("Wenn der 01. Januar ein {} ist, dann gibt es {} Freitage die auf einen 13. fallen".format(
            daysNames[first], counter))

    # Schaltjahre
    print("Schaltjahre:")
    for first in range(7):  # 7 days
        day = first
        counter = 0
        for month in range(12):
            if day % 7 == 6:  # if first of month is sunday then there is a friday the 13th
                counter += 1
            if month == 1:
                day += tageProMonat[month] + 1
            else:
                day += tageProMonat[month]
        print("Wenn der 01. Januar ein {} ist, dann gibt es {} Freitage die auf einen 13. fallen".format(
            daysNames[first], counter))


# Aufgabe 1b
# we need the module datetime to get the date
def friday13thCount(day, month, year):
    date = datetime.now()
    counter = 0

    for a in range(year, date.year + 1):    # +1 because it's starting at zero I think; Year Counter
        for b in range(12):                 # month Counter
            if(a == year and (b + 1 < month)):  # goto loop start if the month is before the date
                continue
            if(a == date.year and (b + 1 == date.month)):    # break if next month would be in the future
                break
            if datetime(a, b + 1, 13).strftime("%A") == "Friday":   # check if the 13th. day is a friday
                counter += 1
    print("Seit dem {}.{}.{} gab es {} Freitage an einem 13.".format(day, month, year, counter))

if __name__ == "__main__":
    friday13()
    print("\n\n")
    friday13thCount(14, 10, 1993)
    friday13thCount(1, 1, 2020)     # expected 1