from models import Note, Tag
from redis_cache import cache


def add_note(title, text, tags):
    try:
        tag_list = add_tags(tags)
        Note(title=title, text=text, tags=tag_list).save()
        return "The note was created successfully!"

    except Exception as err:
        return f"Something went wrong: {err}"


def remove_note(title):
    try:
        target_note = Note.objects.get(title=title)
        target_note.delete()
        return "Note was successfully deleted."
    except BaseException as err:
        return f"Something went wrong: {err}"


@cache
def search_note(title, text, tag):
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
        for r in result:
            res.append([r.title, r.text, [tag.name for tag in r.tags]])
        return res
    else:
        return "Search wasn't successful."


def change_note(title, text, tags):
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
    tag_list = []
    for tag in tags:
        tag = Tag(name=tag)
        tag_list.append(tag)
    return tag_list
