"""
This is a command line interface for the assistant.
"""

import argparse

parser = argparse.ArgumentParser(description="Personal Assistant")


def set_args():
    """
    Sets command line arguments.
    """
    parser.add_argument(
        "--action", "-a", help="Commands: add, remove, search, change", required=True
    )
    parser.add_argument("--target", "-t", help="Targets: contact, note", required=True)

    group_contacts = parser.add_argument_group(
        "contacts", "arguments to work with contacts"
    )
    group_contacts.add_argument("--name")
    group_contacts.add_argument("--birthday")
    group_contacts.add_argument("--email")
    group_contacts.add_argument("--phone")
    group_contacts.add_argument("--address")

    group_notes = parser.add_argument_group("notes", "arguments to work with notes")
    group_notes.add_argument("--title")
    group_notes.add_argument("--text")
    group_notes.add_argument("--tags", nargs="+")


def parse_args():
    """
    Parses command line arguments.
    """
    args = vars(parser.parse_args())
    action = args.get("action")
    target = args.get("target")

    return action, target, args
