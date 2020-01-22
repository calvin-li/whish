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

    def test_patch_book(self):
        isbn = '0-385-08506-0'
        bad_format = {'no_column': 'test'}
        response = self.app.patch(f'/books/{isbn}', json=bad_format)
        self.assertEqual(response.status_code, 400)

        patch_book_data = {
            'author': 'new author',
            'publish_date': '1970-01-01',
        }
        response = self.app.patch(f'/books/{isbn}', json=patch_book_data)
        self.assertEqual(response.status_code, 204)

        response = self.app.get(f'/books/{isbn}')
        expected_json = {
            'author': 'new author',
            'isbn': '0-385-08506-0',
            'publish_date': '1970-01-01',
            'title': 'The Guns of Avalon'
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_json, response.json)

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


if __name__ == '__main__':
    unittest.main()
