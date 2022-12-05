from models import Contact
from verify_input import verify_birthday, verify_name, verify_email, verify_phone
import datetime

from redis_cache import cache


DATE_FORMAT = "%d.%m.%Y"


def convert_bd(birthday):
    try:
        birthday_date = datetime.datetime.strptime(birthday, DATE_FORMAT).date()
    except ValueError:
        raise ValueError(f"{birthday} does not march format '%d.%m.%Y'")
    return birthday_date


def add_contact(name, birthday, email, phone, address):
    try:
        if birthday:
            birthday = verify_birthday(convert_bd(birthday))

        Contact(name=verify_name(name), birthday=birthday, email=verify_email(email), phone=verify_phone(phone),
                address=address).save()

        return "A new contact was added successfully!"

    except Exception as err:
        return f"Something went wrong: {err}"


def remove_contact(name):
    try:
        target_contact = Contact.objects.get(name=name)
        target_contact.delete()
        return "Contact was successfully deleted."
    except BaseException as err:
        return f"Something went wrong: {err}"


@cache
def search_contact(name, phone, email):
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
        for r in result:
            res.append([r.name, r.phone, r.email, r.birthday, r.address])
        return res
    else:
        return "Search wasn't successful."


def change_contact(attrs_to_update):
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
