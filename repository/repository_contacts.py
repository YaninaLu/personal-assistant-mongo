"""
This module works with the contacts database.
"""

import datetime

from databases.models import Contact
from databases.redis_cache import cache
from verify_input import verify_birthday, verify_name, verify_email, verify_phone

DATE_FORMAT = "%d.%m.%Y"


def convert_bd(birthday):
    """
    Converts a birthdate string into a datetime object.
    Raises ValueError if the birthdate doesn't match the format.
    :return: date as datetime
    """
    try:
        birthday_date = datetime.datetime.strptime(birthday, DATE_FORMAT).date()
    except ValueError as exc:
        raise ValueError(f"{birthday} does not march format '%d.%m.%Y'") from exc
    return birthday_date


def add_contact(name, birthday, email, phone, address):
    """
    Adds a contact to the database.
    """
    try:
        if birthday:
            birthday = verify_birthday(convert_bd(birthday))

        Contact(
            name=verify_name(name),
            birthday=birthday,
            email=verify_email(email),
            phone=verify_phone(phone),
            address=address,
        ).save()

        return "A new contact was added successfully!"

    except Exception as err:
        raise err


def remove_contact(name):
    """
    Removes a contact from the database.
    """
    try:
        target_contact = Contact.objects.get(name=name)
        target_contact.delete()
        return "Contact was successfully deleted."
    except BaseException as err:
        return f"Something went wrong: {err}"


@cache
def search_contact(name, phone, email):
    """
    Searches and displays a contact by part of a name, phone, or email.
    """
    if name:
        result = Contact.objects.filter(name__icontains=name)
    elif phone:
        result = Contact.objects.filter(phone__icontains=phone)
    elif email:
        result = Contact.objects.filter(email__icontains=email)
    else:
        return "Can search contacts only by name, phone, or email."

    if len(result) > 0:
        res = []
        for contact in result:
            res.append(
                [
                    contact.name,
                    contact.phone,
                    contact.email,
                    contact.birthday,
                    contact.address,
                ]
            )
        return res
    return "Search wasn't successful."


def change_contact(attrs_to_update):
    """
    Changes contact's info.
    :param attrs_to_update: a dict of data to update
    """
    try:
        target_contact = Contact.objects.get(name=attrs_to_update.get("name"))
        for attr, value in attrs_to_update.items():
            if value:
                if attr == "birthday":
                    setattr(target_contact, attr, verify_birthday(convert_bd(value)))
                elif attr == "email":
                    setattr(target_contact, attr, verify_email(value))
                elif attr == "phone":
                    setattr(target_contact, attr, verify_phone(value))
                else:
                    setattr(target_contact, attr, value)
        target_contact.save()
        return "The contact was changed successfully."

    except BaseException as err:
        return f"Something went wrong: {err}"
