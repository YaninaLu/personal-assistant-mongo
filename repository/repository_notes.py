"""
This module works with the notes database.
"""

from databases.models import Note, Tag
from databases.redis_cache import cache


def add_note(title, text, tags):
    """
    Adds a note to the database.
    :param tags: a list of tags
    """
    try:
        tag_list = add_tags(tags)
        Note(title=title, text=text, tags=tag_list).save()
        return "The note was created successfully!"

    except Exception as err:
        return f"Something went wrong: {err}"


def remove_note(title):
    """
    Removes a note from the database.
    """
    try:
        target_note = Note.objects.get(title=title)
        target_note.delete()
        return "Note was successfully deleted."
    except BaseException as err:
        return f"Something went wrong: {err}"


@cache
def search_note(title, text, tag):
    """
    Searches and displays a note by title, text, or tags.
    :param tag: a list that consists of one tag
    """
    if title:
        result = Note.objects.filter(title__icontains=title)
    elif text:
        result = Note.objects.filter(text__icontains=text)
    elif tag:
        result = Note.objects.filter(tags__match={"name": tag[0]})
    else:
        return "Can search contacts only by title, text, or tags."

    if len(result) > 0:
        res = []
        for note in result:
            res.append([note.title, note.text, [tag.name for tag in note.tags]])
        return res
    return "Search wasn't successful."


def change_note(title, text, tags):
    """
    Changes note's content.
    """
    try:
        target_note = Note.objects.get(title=title)
        tag_list = add_tags(tags)
        setattr(target_note, "text", text)
        setattr(target_note, "tags", tag_list)
        target_note.save()
        return "The note was changed successfully."

    except BaseException as err:
        return f"Something went wrong: {err}"


def add_tags(tags):
    """
    Creates a list of Tag objects.
    :param tags: a list of tags
    :return: a list of Tag objects
    """
    tag_list = []
    for tag in tags:
        tag = Tag(name=tag)
        tag_list.append(tag)
    return tag_list
