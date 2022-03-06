from datetime import date
from datetime import datetime
from datetime import timedelta


def biweek_end_date(start):
    return start + timedelta(days = 13)

def biweek_next_number(first, now):
    return 1 + biweek_number(first, now)

def biweek_number(first, now):
    timediff = now - first
    return 1 + (timediff.days // 14)

def biweek_start_date(first, biweek_number):
    timediff = timedelta (days = 14 * (biweek_number - 1))
    return (first + timediff).date()

def week_end_date(start):
    return start + timedelta (days = 6)

def week_next_number(first, now):
    return 1 + week_number(first, now)

def week_number(start_date, end_date):
    timediff = end_date - start_date
    return 1 + (timediff.days // 7)

def week_start_date(start_date, week_number):
    timediff = timedelta(days = 7 * (week_number - 1))
    return (start_date + timediff).date()

