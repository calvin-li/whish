from pathlib import Path

from flask import Flask, request
from flask_jsonpify import jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy import engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError


# noinspection PyUnusedLocal
@event.listens_for(engine.Engine, "connect")
def set_sqlite_pragma(db_connection, connection_record):
    cursor = db_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# relative paths only, for portability
def create_connection(db_file):
    conn_string = "sqlite:///" + get_abs_path(db_file)
    try:
        connection = create_engine(conn_string)
        connection.execute("pragma foreign_keys=ON")
    except Exception as e:
        print(e)
        raise
    return connection


def get_abs_path(file):
    return str(Path.joinpath(Path(__file__).parent.absolute(), file))


def execute_sql(query):
    try:
        query = Server.connection.execute(query)
    except Exception as e:
        print(e)
        raise
    if query.cursor is not None:
        data = query.cursor.fetchall()
        return [dict(zip(query.keys(), i)) for i in data]


def get_wishlists():
    raw_data = execute_sql("select * from wishlist order by user_id, isbn")
    wishlists = {}
    for row in raw_data:
        user_id = row['user_id']
        if user_id not in wishlists:
            wishlists[user_id] = []
        wishlists[user_id].append(row['isbn'])
    return wishlists


def get_wishlist(user_id):
    raw_data = execute_sql(f"select * from wishlist where user_id={user_id}")
    wishlist = []
    for row in raw_data:
        if row['user_id'] == int(user_id):
            wishlist.append(row['isbn'])
    return wishlist


class Users(Resource):
    @staticmethod
    def get():
        data = execute_sql("SELECT * FROM users")
        wishlists = get_wishlists()
        for user_id in wishlists.keys():
            wishlist = wishlists[user_id]
            user = [x for x in data if x['id'] == user_id][0]
            user['wishlist'] = wishlist
        return jsonify(data)

    @staticmethod
    def post():
        max_id = execute_sql("select id from users order by id desc")[0]['id']
        json = request.json
        if json is None:
            return 'Syntax error', 400
        try:
            values = f"values(" \
                     f"{max_id+1}," \
                     f"'{json['first_name']}'," \
                     f"'{json['last_name']}'," \
                     f"'{json['email']}'," \
                     f"'{json['password']}')"
            execute_sql(f"insert into users {values}")
            return 'Ok', 201
        except KeyError:
            return 'Semantic error', 400
        except IntegrityError as e:
            if '(sqlite3.IntegrityError) UNIQUE constraint failed' in e.args[0]:
                return 'Email conflict', 400
            else:
                raise


class User(Resource):
    @staticmethod
    def get(user_id):
        try:
            user_id = int(user_id)
            user = execute_sql(f"SELECT * FROM users where id={user_id}")[0]
            wishlist = get_wishlist(user_id)
            user['wishlist'] = wishlist
            return jsonify(user)
        except ValueError:
            return 'Bad ID format', 400

    @staticmethod
    def delete(user_id):
        try:
            user_id = int(user_id)
            execute_sql(f"delete from users where id={user_id}")
            return 'Ok', 204
        except ValueError:
            return 'Bad ID format', 400


class Books(Resource):
    @staticmethod
    def get():
        data = execute_sql("SELECT * FROM books")
        return jsonify(data)

    @staticmethod
    def post():
        json = request.json
        if json is None:
            return 'Syntax error', 400
        try:
            values = f"values(" \
                     f"'{json['isbn']}'," \
                     f"'{json['title']}'," \
                     f"'{json['author']}'," \
                     f"'{json['publish_date']}')"
            execute_sql(f"insert into books {values}")
            return 'Ok', 201
        except KeyError:
            return 'Semantic error', 400
        except IntegrityError as e:
            if '(sqlite3.IntegrityError) UNIQUE constraint failed' in e.args[0]:
                return 'Book already in system', 400
            else:
                raise


class Book(Resource):
    @staticmethod
    def get(isbn):
        data = execute_sql(f"SELECT * FROM books where isbn = '{isbn}'")[0]
        return jsonify(data)

    @staticmethod
    def delete(isbn):
        execute_sql(f"delete from books where isbn='{isbn}'")
        return 'Ok', 204


class Wishlist(Resource):
    @staticmethod
    def get(user_id):
        try:
            user_id = int(user_id)
            wishlist = get_wishlist(user_id)
            return jsonify(wishlist)
        except ValueError:
            return 'Bad ID format', 400

    @staticmethod
    def post(user_id):
        json = request.json
        if json is None:
            return 'Syntax error', 400
        try:
            values = f"values(" \
                     f"'{user_id}'," \
                     f"'{json['isbn']}')"
            execute_sql(f"insert into wishlist {values}")
            return 'Ok', 201
        except KeyError:
            return 'Semantic error', 400
        except IntegrityError as e:
            if '(sqlite3.IntegrityError) UNIQUE constraint failed' in e.args[0]:
                return 'Book already in wishlist', 400
            elif '(sqlite3.IntegrityError) FOREIGN KEY constraint failed' in e.args[0]:
                return 'User ID or ISBN does not exist', 400
            else:
                raise


class WishlistBook(Resource):
    @staticmethod
    def delete(user_id, isbn):
        try:
            user_id = int(user_id)
            execute_sql(f"delete from wishlist where user_id={user_id} and isbn='{isbn}'")
            return 'Ok', 204
        except ValueError:
            return 'Bad ID format', 400


class Server:
    connection = None

    @staticmethod
    def setup(database):
        Server.connection = create_connection(database)
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(Users, '/users')
        api.add_resource(User, '/users/<user_id>')
        api.add_resource(Wishlist, '/users/<user_id>/wishlist')
        api.add_resource(WishlistBook, '/users/<user_id>/wishlist/<isbn>')
        api.add_resource(Books, '/books')
        api.add_resource(Book, '/books/<isbn>')
        return app


if __name__ == '__main__':
    Server.setup('db/whish.db').run(port='6639')
