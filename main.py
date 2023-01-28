"""
This is an entry point of the application.
"""

from cli import set_args, parse_args

from repository.repository_contacts import (
    add_contact,
    remove_contact,
    search_contact,
    change_contact,
)
from repository.repository_notes import add_note, remove_note, search_note, change_note


def main():
    """
    Main flow of the application.
    """
    set_args()
    action, target, args = parse_args()

    if target == "contact":
        return work_with_contacts(args, action)
    if target == "note":
        return work_with_notes(args, action)
    return "Unknown target."


def work_with_contacts(args, action):
    """
    Calls functions that work with contacts.
    """
    name = args.get("name")
    birthday = args.get("birthday")
    email = args.get("email")
    phone = args.get("phone")
    address = args.get("address")

    match action:
        case "add":
            return add_contact(name, birthday, email, phone, address)
        case "remove":
            return remove_contact(name)
        case "search":
            return search_contact(name, phone, email)
        case "change":
            attrs_to_update = {
                "name": name,
                "birthday": birthday,
                "email": email,
                "phone": phone,
                "address": address,
            }
            return change_contact(attrs_to_update)
        case _:
            print("Unknown command")


def work_with_notes(args, action):
    """
    Calls functions that work with notes.
    """
    title = args.get("title")
    text = args.get("text")
    tags = args.get("tags")

    match action:
        case "add":
            return add_note(title, text, tags)
        case "remove":
            return remove_note(title)
        case "search":
            return search_note(title, text, tags)
        case "change":
            return change_note(title, text, tags)
        case _:
            return "Unknown command"


if __name__ == "__main__":
    print(main())
