import shutil
import unittest
import os

import Hello

test_domain = "http://localhost:6639/"


class ApiTests(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls):
        shutil.copyfile(Hello.get_abs_path('db/test_base.db'), Hello.get_abs_path('db/test.db'))
        ApiTests.app = Hello.App.setup('db/test.db').test_client()
        ApiTests.app.testing = True

    @classmethod
    def tearDownClass(cls):
        os.remove(Hello.get_abs_path('db/test.db'))

    def test_get_books(self):
        response = ApiTests.app.get('/books')
        expected_json = [
            {'author': 'Roger Zelazny', 'isbn': '978-0-380-01430-9', 'publish_date': '1970-06-01',
             'title': 'Nine Princes in Amber'},
            {'author': 'Roger Zelazny', 'isbn': '0-385-08506-0', 'publish_date': '1972-01-01',
             'title': 'The Guns of Avalon'}
        ]
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(expected_json, response.json)

    def test_get_users(self):
        response = ApiTests.app.get('/users')
        expected_json = [
            {'email': 'calvin@gmail.com', 'first_name': 'calvin', 'id': 0, 'last_name': 'li',
             'password': '$2y$12$Hz18rfdSInA55llCXSgEj./Qg.P.xERDTiUIrDkNfYTDmzwxzEQ2C',
             'wishlist': ['0-385-08506-0', '978-0-380-01430-9']},
            {'email': 'testusera@gmail.com', 'first_name': 'testuser', 'id': 1, 'last_name': 'a',
             'password': '$2y$12$8lSGo1QAbTL5muXpgNxpyu/luQlEvPkrqyybqb0iTvEUYAhWvPZfK',
             'wishlist': ['978-0-380-01430-9']}
        ]
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(expected_json, response.json)


if __name__ == '__main__':
    unittest.main()
