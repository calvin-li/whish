from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
import sqlite3
from pathlib import Path


# relative paths only, for portability
def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(Path.joinpath(Path(__file__).parent.absolute(), db_file))
    except sqlite3.Error as e:
        print(e)
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


class Employees(Resource):
    @staticmethod
    def get():
        conn = create_connection(db_file_path)
        data = execute_query(conn, "SELECT * FROM employees")
        return {'employees': [i[0] for i in data]}


class Tracks(Resource):
    @staticmethod
    def get(self):
        conn = create_connection(db_file_path)
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class EmployeesName(Resource):
    @staticmethod
    def get(self, employee_id):
        conn = create_connection(db_file_path)
        query = conn.execute("select * from employees where EmployeeId =%d " % int(employee_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


if __name__ == '__main__':
    db_file_path = 'db/chinook.db'
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Employees, '/employees')
    api.add_resource(Tracks, '/tracks')
    api.add_resource(EmployeesName, '/employees/<employee_id>')
    app.run(port='5002')
