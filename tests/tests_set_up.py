"""
This module sets up the testing environment.
"""

import unittest

from mongoengine import connect
from mongoengine.connection import disconnect


class TestClassMethods(unittest.TestCase):
    """
    Parent class for test classes.
    """

    def setUp(self) -> None:
        """
        Sets up connection to the database.
        """
        disconnect(alias="default")
        self.connection_to_db = connect(db="testdata", host="localhost", port=27017)

    def tearDown(self) -> None:
        """
        Cleans and shuts the database.
        """
        self.connection_to_db.drop_database("testdata")
        self.connection_to_db.close()
