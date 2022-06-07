import unittest
from unittest.mock import MagicMock
from unittest.mock import patch


class DatabaseTest(unittest.TestCase):

    @patch('db.database.Database')
    def setUp(self, mock_db):
        self.db = mock_db()
        self.name = 'testName'
        self.content = 'testContent'
        self.login = 'testLogin'
        self.password = 'testPassword'

    def test_insert_data_for_search(self):
        self.db.insert_data_for_search = MagicMock()
        self.db.insert_data_for_search(self.name, self.content)
        self.db.insert_data_for_search.assert_called_once()

    def test_delete_data(self):
        self.db.delete_data = MagicMock()
        self.db.delete_data()
        self.db.delete_data.assert_called_once()

    def test_get_all_data(self):
        self.db.delete_data = MagicMock()
        self.db.delete_data()
        self.db.delete_data.assert_called_once()

    def test_add_user(self):
        self.db.add_user = MagicMock()
        self.db.add_user(self.name, self.login, self.password)
        self.db.add_user.assert_called_once()

    def test_get_user_by_login(self):
        self.db.get_user_by_login = MagicMock()
        self.db.get_user_by_login(self.login)
        self.db.get_user_by_login.assert_called_once()

    def test_rollback(self):
        self.db.rollback = MagicMock()
        self.db.rollback()
        self.db.rollback.assert_called_once()

    def test_count_rows(self):
        self.db.count_rows = MagicMock()
        self.db.count_rows()
        self.db.count_rows.assert_called_once()

    def test_get_all_sentences(self):
        self.db.get_all_sentences = MagicMock()
        self.db.get_all_sentences([])
        self.db.get_all_sentences.assert_called_once()

    def test_result_to_dict(self):
        self.db.result_to_dict = MagicMock()
        self.db.result_to_dict([])
        self.db.result_to_dict.assert_called_once()
