from pathlib import Path

from flask import Flask
from flask_jsonpify import jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy import engine
from sqlalchemy import event


# noinspection PyUnusedLocal
@event.listens_for(engine.Engine, "connect")
def set_sqlite_pragma(db_connection, connection_record):
    cursor = db_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# relative paths only, for portability
def create_connection(db_file):
    conn_string = "sqlite:///" + str(Path.joinpath(Path(__file__).parent.absolute(), db_file))
    try:
        connection = create_engine(conn_string)
        connection.execute("pragma foreign_keys=ON")
    except Exception as e:
        print(e)
        raise
    return connection


def execute_sql(conn2, query):
    try:
        query = conn2.execute(query)
    except Exception as e:
        print(e)
        raise
    if query.cursor is not None:
        data = query.cursor.fetchall()
        return [dict(zip(query.keys(), i)) for i in data]


class Users(Resource):
    @staticmethod
    def get():
        data = execute_sql(App.connection, "SELECT * FROM users")
        return jsonify(data)


class Books(Resource):
    @staticmethod
    def get():
        data = execute_sql(App.connection, "SELECT * FROM books")
        return jsonify(data)


class App:
    connection = None

    @staticmethod
    def setup(database):
        App.connection = create_connection(database)
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(Users, '/users')
        api.add_resource(Books, '/books')
        return app


if __name__ == '__main__':
    App.setup('db/whish.db').run(port='6639')
