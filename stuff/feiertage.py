#!/usr/bin/env python3
"""
Feiertags Modul for Notifications
"""

from datetime import date, datetime, time, timedelta


def get_osterstonntag(year):
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


def is_weekend(_year):
    """
    Check if today is in weekend
    """
    now = datetime.today().date()
    if now.weekday() > 4:
        return now
    return False

checks = {
  'ostersonntag': get_osterstonntag,
  'karfreitag': lambda year: get_osterstonntag(year) - timedelta(days=2),
  'ostermontag': lambda year: get_osterstonntag(year) + timedelta(days=1),
  'christi_himmelfahrt': lambda year: get_osterstonntag(year) + timedelta(days=39),
  'pfingstsonntag': lambda year: get_osterstonntag(year) + timedelta(days=49),
  'pfingstmontag': lambda year: get_osterstonntag(year) + timedelta(days=50),
  'fronleichnam': lambda year: get_osterstonntag(year) + timedelta(days=60),
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
  'weekend': is_weekend
}


def check_date(date_to_check, debug=False):
    """
    Check the given Date
    """
    for check_name, checkfunc in checks.items():
        year = date_to_check.year
        feast_date = checkfunc(year)
        if debug:
            print(f"{feast_date}: {check_name}")
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


def check_for_night():
    """
    Check if it is currently
    night
    """
    now_time = datetime.now().time()
    if now_time >= time(19,00) or now_time <= time(7,00):
        return True
    return False


if __name__ == "__main__":
    print("- Fake Check a Date and Print all Days:")
    test_date = date(2024, 12, 24)
    print(f"  Test date: {test_date}, Result: {check_date(test_date, debug=True)}")
    print("- Check current Time:")
    print(f"  Is it night: {check_for_night()}")
    print("- Check current Date:")
    print(f"  Currently Feiertag: {check_today()}")
