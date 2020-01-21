import unittest
import Hello


class MyTestCase(unittest.TestCase):
    def test_db_connection(self):
        # from https://www.sqlitetutorial.net/sqlite-sample-database/
        db_file_path = 'C:\\Users\\clvn1\\PycharmProjects\\whish\\chinook.db'
        conn = Hello.create_connection(db_file_path)
        self.assertNotEqual(conn, None, "failed connection test")

        # testing the connection with a query. In a larger project this could be its own test with a spoofed connection
        test_query = "SELECT * FROM media_types"
        expected_data = [
            (1, 'MPEG audio file'),
            (2, 'Protected AAC audio file'),
            (3, 'Protected MPEG-4 video file'),
            (4, 'Purchased AAC audio file'),
            (5, 'AAC audio file')
        ]
        data = Hello.execute_query(conn, test_query)
        self.assertListEqual(data, expected_data, "failed query test")


if __name__ == '__main__':
    unittest.main()
