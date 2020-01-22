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

    def test_post_book(self):
        bad_format = {'isbn': '978-0-385-60441-3'}
        response = self.app.post('/books', json=bad_format)
        self.assertEqual(response.status_code, 400)

        new_book_data = {
            'isbn': '978-0-385-60441-3',
            'title': 'The Book of Dust',
            'author': 'Philip Pullman',
            'publish_date': "2017-10-19"
        }
        response = self.app.post('/books', json=new_book_data)
        self.assertEqual(response.status_code, 201)

        response = self.app.get('/books/978-0-385-60441-3')
        expected_json = {
            'author': 'Philip Pullman',
            'isbn': '978-0-385-60441-3',
            'publish_date': '2017-10-19',
            'title': 'The Book of Dust'
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_json, response.json)

        response = self.app.post('/books', json=new_book_data)
        self.assertEqual(response.status_code, 400)

    def test_del_book(self):
        response = self.app.delete("/books/wrong-isbn")
        self.assertEqual(response.status_code, 204)

        response = self.app.delete("/books/0-385-08515-X")
        self.assertEqual(response.status_code, 204)
        response = self.app.get('/books')
        self.assertEqual(response.status_code, 200)
        expected_json = [
            {'author': 'Roger Zelazny', 'isbn': '978-0-380-01430-9', 'publish_date': '1970-06-01',
             'title': 'Nine Princes in Amber'},
            {'author': 'Roger Zelazny', 'isbn': '0-385-08506-0', 'publish_date': '1972-01-01',
             'title': 'The Guns of Avalon'}
        ]
        self.assertListEqual(expected_json, response.json)

    def test_post_wishlist_book(self):
        user_id = 2
        bad_format = {'user_id': user_id}
        response = self.app.post(f'/users/{user_id}/wishlist', json=bad_format)
        self.assertEqual(response.status_code, 400)

        new_wishlist_book = {'isbn': '0-385-08506-0'}
        response = self.app.post(f'/users/{user_id}/wishlist', json=new_wishlist_book)
        self.assertEqual(response.status_code, 201)

        response = self.app.get(f'/users/{user_id}/wishlist')
        expected_json = ['0-385-08506-0']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_json, response.json)

        response = self.app.post(f'/users/{user_id}/wishlist', json=new_wishlist_book)
        self.assertEqual(response.status_code, 400)

        user_id = 9999
        response = self.app.post(f'/users/{user_id}/wishlist', json=new_wishlist_book)
        self.assertEqual(response.status_code, 400)

    def test_del_book_wishlist(self):
        response = self.app.delete('/users/0/wishlist/wrong-isbn')
        self.assertEqual(response.status_code, 204)

        response = self.app.delete('/users/0/wishlist/0-385-08506-0')
        self.assertEqual(response.status_code, 204)
        response = self.app.get('/users/0')
        self.assertEqual(response.status_code, 200)
        expected_json = {
            'email': 'calvin@gmail.com', 'first_name': 'calvin', 'id': 0, 'last_name': 'li',
            'password': '$2y$12$Hz18rfdSInA55llCXSgEj./Qg.P.xERDTiUIrDkNfYTDmzwxzEQ2C',
            'wishlist': ['978-0-380-01430-9']
        }
        self.assertEqual(expected_json, response.json)


if __name__ == '__main__':
    unittest.main()
