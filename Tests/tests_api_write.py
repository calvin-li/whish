import shutil
import unittest
import os

import App

test_domain = "http://localhost:6639/"


class TestsApiWrite(unittest.TestCase):
    def setUp(self):
        shutil.copyfile(App.get_abs_path('db/test_base.db'), App.get_abs_path('db/test.db'))
        self.app = App.Server.setup('db/test.db').test_client()
        self.app.testing = True

    def tearDown(self):
        os.remove(App.get_abs_path('db/test.db'))

    def test_del_users(self):
        response = self.app.delete('/users/2')
        self.assertEqual(response.status_code, 204)
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        expected_json = [
            {'email': 'calvin@gmail.com', 'first_name': 'calvin', 'id': 0, 'last_name': 'li',
             'password': '$2y$12$Hz18rfdSInA55llCXSgEj./Qg.P.xERDTiUIrDkNfYTDmzwxzEQ2C',
             'wishlist': ['0-385-08506-0', '978-0-380-01430-9']},
            {'email': 'testusera@gmail.com', 'first_name': 'testuser', 'id': 1, 'last_name': 'a',
             'password': '$2y$12$8lSGo1QAbTL5muXpgNxpyu/luQlEvPkrqyybqb0iTvEUYAhWvPZfK',
             'wishlist': ['978-0-380-01430-9']}
        ]
        self.assertListEqual(expected_json, response.json)


if __name__ == '__main__':
    unittest.main()
