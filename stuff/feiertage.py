#!/usr/bin/env python3
"""
Feiertags Modul for Notifications
"""

from datetime import date, datetime

def is_ostern(year):
    """
    Retun Date of Estern in Germany
    """
    #pylint: disable=invalid-name
    A = year%19
    K = year//100
    M = 15+(3*K+3)//4-(8*K+13)//25
    D = (19*A+M)%30
    S = 2-(3*K+3)//4
    R = D//29+(D//28-D//29)*(A//11)
    OG = 21+D+R
    SZ = 7-(year+year//4+S)%7
    OE = 7-(OG-SZ)%7
    OS = OG+OE

    if OS>31:
        return date(year, 4, OS-31)
    return date(year, 3, OS)

checks = {
  'ostern': is_ostern,
  'neujahr': lambda year: date(year, 1, 1),
  'dreikoenig': lambda year: date(year, 1, 6),
  'tagderarbeit': lambda year: date(year, 5, 1),
  'mariahimmel': lambda year: date(year, 8, 15),
  'tagdereinheit': lambda year: date(year, 10, 3),
  'allerheiligen': lambda year: date(year, 11, 1),
  'heiligabend': lambda year: date(year, 12, 24),
  'erstweih': lambda year: date(year, 12, 25),
  'zweitweih': lambda year: date(year, 12, 26),
  'silvester': lambda year: date(year, 12, 31),
}


def check_date(date_to_check):
    """
    Check the given Date
    """
    for check_name, checkfunc in checks.items():
        year = date_to_check.year
        feast_date = checkfunc(year)
        if feast_date == date_to_check:
            print(f"It's {check_name}")
            return True
    return False



def check_today():
    """
    Check if current day is a Feiertag
    """

    now = datetime.now()
    date_to_check = now.date()
    return check_date(date_to_check)


if __name__ == "__main__":
    print("Fake Check a Date:")
    test_date = date(2024, 12, 24)
    check_date(test_date)
