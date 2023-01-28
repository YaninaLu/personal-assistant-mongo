"""
This module tests contacts functionality.
"""

import datetime

from mongoengine import DoesNotExist

from tests_set_up import TestClassMethods
from databases.models import Contact
from repository.repository_contacts import (
    add_contact,
    remove_contact,
    search_contact,
    change_contact,
)


class TestContactsMethods(TestClassMethods):
    """
    Tests for methods that manage contacts.
    """

    def test_add(self):
        """
        Tests adding contacts.
        """
        name = "Joe"
        birthday = "12.02.1999"
        email = "joe@gmail.com"
        phone = "+380956754455"
        address = "Joe's St., 15"
        result = add_contact(name, birthday, email, phone, address)
        assert result == "A new contact was added successfully!"
        new_contact = Contact.objects().first()
        assert new_contact.name == "Joe"
        assert new_contact.birthday == datetime.datetime(1999, 2, 12)
        assert new_contact.email == "joe@gmail.com"
        assert new_contact.phone == "+380956754455"
        assert new_contact.address == "Joe's St., 15"

    def test_input_err_name(self):
        """
        Tests input name error.
        """
        wrong_name = "J"
        self.assertRaises(
            ValueError,
            add_contact,
            name=wrong_name,
            birthday=None,
            email=None,
            phone=None,
            address=None,
        )

    def test_input_err_birthday(self):
        """
        Tests input birthday error.
        """
        name = "Joe"
        wrong_birthday_format = "12/02/1999"
        self.assertRaises(
            ValueError,
            add_contact,
            name=name,
            birthday=wrong_birthday_format,
            email=None,
            phone=None,
            address=None,
        )
        birthday_in_future = "12.02.2024"
        self.assertRaises(
            ValueError,
            add_contact,
            name=name,
            birthday=birthday_in_future,
            email=None,
            phone=None,
            address=None,
        )

    def test_input_err_email(self):
        """
        Tests input email error.
        """
        name = "Joe"
        birthday = "12.02.1999"
        wrong_email_format = "_joe@gmail.com"
        self.assertRaises(
            ValueError,
            add_contact,
            name=name,
            birthday=birthday,
            email=wrong_email_format,
            phone=None,
            address=None,
        )

    def test_input_err_phone(self):
        """
        Tests input phone error.
        """
        name = "Joe"
        birthday = "12.02.1999"
        email = "joe@gmail.com"
        wrong_phone_format = "+38095675445577"
        self.assertRaises(
            ValueError,
            add_contact,
            name=name,
            birthday=birthday,
            email=email,
            phone=wrong_phone_format,
            address=None,
        )

    def test_remove(self):
        """
        Tests removing contacts.
        """
        name = "Joe"
        birthday = "12.02.1999"
        email = "joe@gmail.com"
        phone = "+380956754455"
        address = "Joe's St., 15"
        add_contact(name, birthday, email, phone, address)
        result = remove_contact(name)
        assert result == "Contact was successfully deleted."
        self.assertRaises(DoesNotExist, Contact.objects.get, name=name)

    def test_show(self):
        """
        Tests searching contacts.
        """
        name = "Joe"
        birthday = "12.02.1999"
        email = "joe@gmail.com"
        phone = "+380956754455"
        address = "Joe's St., 15"
        add_contact(name, birthday, email, phone, address)
        result = search_contact(name="oe", phone=None, email=None)
        assert result == [[name, phone, email, datetime.datetime(1999, 2, 12), address]]
        result = search_contact(name=None, phone="80", email=None)
        assert result == [[name, phone, email, datetime.datetime(1999, 2, 12), address]]
        result = search_contact(name=None, phone=None, email="gmail")
        assert result == [[name, phone, email, datetime.datetime(1999, 2, 12), address]]
        result = search_contact(name="Mary", phone=None, email=None)
        assert result == "Search wasn't successful."
        result = search_contact(name=None, phone=None, email=None)
        assert result == "Can search contacts only by name, phone, or email."

    def test_change(self):
        """
        Tests changing contacts.
        """
        name = "Joe"
        birthday = "12.02.1999"
        email = "joe@gmail.com"
        phone = "+380956754455"
        address = "Joe's St., 15"
        add_contact(name, birthday, email, phone, address)
        attrs_to_update = {
            "name": name,
            "birthday": "15.02.1999",
            "email": "joeM@gmail.com",
            "phone": "0987776655",
            "address": "Some St.",
        }
        result = change_contact(attrs_to_update)
        assert result == "The contact was changed successfully."
        changed_contact = Contact.objects().first()
        assert changed_contact.birthday == datetime.datetime(1999, 2, 15)
        assert changed_contact.email == "joeM@gmail.com"
        assert changed_contact.phone == "0987776655"
        assert changed_contact.address == "Some St."
