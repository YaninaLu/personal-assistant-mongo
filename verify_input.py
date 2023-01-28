"""
This module contains functions that verify user's input.
"""

import datetime
from re import match


def verify_name(name):
    """
    Verifies contact's name.
    """
    if len(name) < 2 or len(name) > 30:
        raise ValueError("Name must be between 2 and 30 characters.")
    return name


def verify_phone(phone):
    """
    Verifies contact's phone.
    """
    if phone:
        if not match(r"(\+?\d{12}|\d{10})$", phone):
            raise ValueError("Invalid phone format. Try +123456789012 or 1234567890.")
    return phone


def verify_birthday(birthday):
    """
    Verify contact's birthday.
    """
    if birthday > datetime.datetime.now().date():
        raise ValueError("Birthday can't be in future.")
    return birthday


def verify_email(email):
    """
    Verifies contact's email.
    """
    if email:
        if not match(r"[a-zA-Z][a-zA-Z_.0-9]+@[a-zA-Z_]+?\.[a-zA-Z]{2,}", email):
            raise ValueError("Invalid email.")
    return email
