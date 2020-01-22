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

    def test_put_wishlist(self):
        response = self.app.put('/users/bad/wishlist')
        self.assertEqual(response.status_code, 400)

        user_id = 0
        bad_format = {'no_column': []}
        response = self.app.put(f'/users/{user_id}/wishlist', json=bad_format)
        self.assertEqual(response.status_code, 400)

        patch_wishlist_data = {'wishlist': []}
        response = self.app.put(f'/users/{user_id}/wishlist', json=patch_wishlist_data)
        self.assertEqual(response.status_code, 204)

        response = self.app.get(f'/users/{user_id}/wishlist')
        expected_json = []
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_json, response.json)

        patch_wishlist_data['wishlist'] = ['0-385-08506-0']
        response = self.app.put(f'/users/{user_id}/wishlist', json=patch_wishlist_data)
        self.assertEqual(response.status_code, 204)
        response = self.app.get(f'/users/{user_id}/wishlist')
        expected_json = ['0-385-08506-0']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_json, response.json)

        patch_wishlist_data['wishlist'] = ['test']
        response = self.app.put(f'/users/{user_id}/wishlist', json=patch_wishlist_data)
        self.assertEqual(response.status_code, 400)

        patch_wishlist_data['wishlist'] = ['0-385-08506-0', '0-385-08506-0']
        response = self.app.put(f'/users/{user_id}/wishlist', json=patch_wishlist_data)
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
