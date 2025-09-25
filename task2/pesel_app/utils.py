"""Pesel app utils."""
# Standard Library
from datetime import datetime


def get_century_and_month(month):
    """Return the century and real month for a given PESEL month code."""
    century_offsets = {
        80: 1800,
        0: 1900,
        20: 2000,
    }

    for offset, century in century_offsets.items():
        if offset < month <= offset + 12:
            real_month = month - offset
            return century, real_month

    return None, None


def decode_pesel(pesel):
    """Decode a PESEL number into birth date and gender, or return None if invalid."""
    if len(pesel) != 11 or not pesel.isdigit():
        return None

    year = int(pesel[0:2])
    month = int(pesel[2:4])
    day = int(pesel[4:6])

    century, real_month = get_century_and_month(month)
    if century is None:
        return None

    full_year = century + year

    try:
        birth_date = datetime(full_year, real_month, day).date()
    except ValueError:
        return None

    gender_digit = int(pesel[9])
    gender = 'Kobieta' if gender_digit % 2 == 0 else 'Mężczyzna'

    return {
        'birth_date': birth_date.strftime('%Y-%m-%d'),
        'gender': gender
    }
