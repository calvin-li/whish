import shutil
import unittest
import os

import App

test_domain = "http://localhost:6639/"


class TestsApiRead(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls):
        shutil.copyfile(App.get_abs_path('db/test_base.db'), App.get_abs_path('db/test.db'))
        TestsApiRead.app = App.Server.setup('db/test.db').test_client()
        TestsApiRead.app.testing = True

    @classmethod
    def tearDownClass(cls):
        os.remove(App.get_abs_path('db/test.db'))

    def test_get_books(self):
        response = TestsApiRead.app.get('/books')
        expected_json = [
            {'author': 'Roger Zelazny', 'isbn': '978-0-380-01430-9', 'publish_date': '1970-06-01',
             'title': 'Nine Princes in Amber'},
            {'author': 'Roger Zelazny', 'isbn': '0-385-08506-0', 'publish_date': '1972-01-01',
             'title': 'The Guns of Avalon'},
            {'author': 'Roger Zelazny', 'isbn': '0-385-08515-X', 'publish_date': '1975-02-01',
             'title': 'Sign of the Unicorn'}
        ]
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(expected_json, response.json)

    def test_get_book(self):
        response = TestsApiRead.app.get('/books/978-0-380-01430-9')
        expected_json = {
            'author': 'Roger Zelazny', 'isbn': '978-0-380-01430-9', 'publish_date': '1970-06-01',
            'title': 'Nine Princes in Amber'
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_json, response.json)

    def test_get_users(self):
        response = TestsApiRead.app.get('/users')
        expected_json = [
            {'email': 'calvin@gmail.com', 'first_name': 'calvin', 'id': 0, 'last_name': 'li',
             'password': '$2y$12$Hz18rfdSInA55llCXSgEj./Qg.P.xERDTiUIrDkNfYTDmzwxzEQ2C',
             'wishlist': ['0-385-08506-0', '978-0-380-01430-9']},
            {'email': 'testusera@gmail.com', 'first_name': 'testuser', 'id': 1, 'last_name': 'a',
             'password': '$2y$12$8lSGo1QAbTL5muXpgNxpyu/luQlEvPkrqyybqb0iTvEUYAhWvPZfK',
             'wishlist': ['978-0-380-01430-9']},
            {'email': 'testuserb@gmail.com', 'first_name': 'testuser', 'id': 2, 'last_name': 'b',
             'password': '$2y$12$Ll9RpMmJi/qVZXKUKUvfTezta2KbUcQsXBMPXJEdBSVJIw7.Fv3UC'}
        ]
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(expected_json, response.json)

    def test_get_user(self):
        response = TestsApiRead.app.get('/users/bad-id')
        self.assertEqual(response.status_code, 400)

        response = TestsApiRead.app.get('/users/0')
        expected_json = {
            'email': 'calvin@gmail.com', 'first_name': 'calvin', 'id': 0, 'last_name': 'li',
            'password': '$2y$12$Hz18rfdSInA55llCXSgEj./Qg.P.xERDTiUIrDkNfYTDmzwxzEQ2C',
            'wishlist': ['0-385-08506-0', '978-0-380-01430-9']}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_json, response.json)

    def test_get_wishlist(self):
        response = TestsApiRead.app.get('/users/0/wishlist')
        expected_json = ['0-385-08506-0', '978-0-380-01430-9']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_json, response.json)


if __name__ == '__main__':
    unittest.main()
