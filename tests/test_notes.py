"""
This module tests notes functionality.
"""

from mongoengine import DoesNotExist

from tests_set_up import TestClassMethods
from databases.models import Note
from repository.repository_notes import add_note, remove_note, search_note, change_note


class TestNotesMethods(TestClassMethods):
    """
    Tests for methods that manage notes.
    """

    def test_add(self):
        """
        Tests adding notes.
        """
        title = "Test Note"
        text = "You have to test your application"
        tags = ["work", "programming", "tasks"]
        result = add_note(title=title, text=text, tags=tags)
        assert result == "The note was created successfully!"
        new_note = Note.objects().first()
        assert new_note.title == "Test Note"
        assert new_note.text == "You have to test your application"
        assert [tag.name for tag in new_note.tags] == ["work", "programming", "tasks"]

    def test_remove(self):
        """
        Tests removing notes.
        """
        title = "Test Note"
        text = "You have to test your application"
        tags = ["work", "programming", "tasks"]
        add_note(title=title, text=text, tags=tags)
        result = remove_note(title)
        assert result == "Note was successfully deleted."
        self.assertRaises(DoesNotExist, Note.objects.get, title=title)

    def test_show(self):
        """
        Tests searching notes.
        """
        title = "Test Note"
        text = "You have to test your application"
        tags = ["work", "programming", "tasks"]
        add_note(title=title, text=text, tags=tags)
        result = search_note(title="est", text=None, tag=None)
        assert result == [[title, text, tags]]
        result = search_note(title=None, text="your", tag=None)
        assert result == [[title, text, tags]]
        result = search_note(title=None, text=None, tag=["work"])
        assert result == [[title, text, tags]]
        result = search_note(title="Bla", text=None, tag=None)
        assert result == "Search wasn't successful."
        result = search_note(title=None, text=None, tag=None)
        assert result == "Can search contacts only by title, text, or tags."

    def test_change(self):
        """
        Tests changing notes.
        """
        title = "Test Note"
        text = "You have to test your application"
        tags = ["work", "programming", "tasks"]
        add_note(title=title, text=text, tags=tags)
        new_text = "Changed text"
        new_tags = ["cat", "home"]
        result = change_note(title=title, text=new_text, tags=new_tags)
        assert result == "The note was changed successfully."
        changed_note = Note.objects().first()
        assert changed_note.title == title
        assert changed_note.text == new_text
        assert [tag.name for tag in changed_note.tags] == new_tags
