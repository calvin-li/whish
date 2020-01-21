import unittest
from sqlalchemy import exc as sqlalchemy_exc
import Hello
from pathlib import Path


class DataBaseTests(unittest.TestCase):
    def test_db_connection(self):
        db_file_path = Path('db/chinook.db')     # from https://www.sqlitetutorial.net/sqlite-sample-database/
        conn = Hello.create_connection(db_file_path)
        self.assertNotEqual(conn, None, "failed connection test")

        # testing the connection with a query. In a larger project this could be its own test with a spoofed connection
        test_query = "SELECT * FROM media_types"

        expected_data = [
            {'MediaTypeId': 1, 'Name': 'MPEG audio file'},
            {'MediaTypeId': 2, 'Name': 'Protected AAC audio file'},
            {'MediaTypeId': 3, 'Name': 'Protected MPEG-4 video file'},
            {'MediaTypeId': 4, 'Name': 'Purchased AAC audio file'},
            {'MediaTypeId': 5, 'Name': 'AAC audio file'}
        ]
        data = Hello.execute_sql(conn, test_query)
        self.assertListEqual(data, expected_data, "failed query test")

        # testing non-query statements. if this fails might have to manually clean up db
        Hello.execute_sql(conn, "insert into media_types values(0, 'test')")
        Hello.execute_sql(conn, "delete from media_types where MediaTypeId=0;")

    def test_foreign_key_check(self):
        db_file_path = Path('db/whish.db')     # from https://www.sqlitetutorial.net/sqlite-sample-database/
        conn = Hello.create_connection(db_file_path)

        test_query = "insert into wishlist (user_id, isbn) values(-1, 'fake_isbn')"
        try:
            conn.execute(test_query)
        except sqlalchemy_exc.IntegrityError as e:
            self.assertEqual(e.args, ('(sqlite3.IntegrityError) FOREIGN KEY constraint failed',))


if __name__ == '__main__':
    unittest.main()
