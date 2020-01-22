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

    def test_post_user(self):
        bad_format = {'first_name': 'testuser'}
        response = self.app.post('/users', json=bad_format)
        self.assertEqual(response.status_code, 400)

        new_user_data = {
            'first_name': 'testuser',
            'last_name': 'u',
            'email': 'testuseru@gmail.com',
            'password': "$2y$12$5wKzo5qkMKeRQ9BA3/gK/u6B5MRi5DsI1KVyDDLRtevWwTUGBIKz."
        }
        response = self.app.post('/users', json=new_user_data)
        self.assertEqual(response.status_code, 201)

        response = self.app.get('/users/3')
        expected_json = {
            'email': 'testuseru@gmail.com', 'first_name': 'testuser', 'id': 3, 'last_name': 'u',
            'password': '$2y$12$5wKzo5qkMKeRQ9BA3/gK/u6B5MRi5DsI1KVyDDLRtevWwTUGBIKz.', 'wishlist': []
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_json, response.json)

        response = self.app.post('/users', json=new_user_data)
        self.assertEqual(response.status_code, 400)

    def test_patch_user(self):
        user_id = 'error'
        response = self.app.patch(f'/users/{user_id}')
        self.assertEqual(response.status_code, 400)

        user_id = 1
        bad_format = {'no_column': 'test'}
        response = self.app.patch(f'/users/{user_id}', json=bad_format)
        self.assertEqual(response.status_code, 400)

        patch_user_data = {
            'first_name': 'new first name',
            'last_name': 'new last name',
        }
        response = self.app.patch(f'/users/{user_id}', json=patch_user_data)
        self.assertEqual(response.status_code, 204)

        response = self.app.get(f'/users/{user_id}')
        expected_json = {
            'email': 'testusera@gmail.com',
            'first_name': 'new first name',
            'id': 1,
            'last_name': 'new last name',
            'password': '$2y$12$8lSGo1QAbTL5muXpgNxpyu/luQlEvPkrqyybqb0iTvEUYAhWvPZfK',
            'wishlist': ['978-0-380-01430-9']
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_json, response.json)

    def test_del_user(self):
        response = self.app.delete('/users/bad_id')
        self.assertEqual(response.status_code, 400)
        response = self.app.delete('/users/9999')
        self.assertEqual(response.status_code, 204)

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
