from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
import sqlite3


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


db_file_path = 'C:\\Users\\clvn1\\PycharmProjects\\whish\\chinook.db'

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


api.add_resource(Employees, '/employees')
api.add_resource(Tracks, '/tracks')
api.add_resource(EmployeesName, '/employees/<employee_id>')

if __name__ == '__main__':
    app.run(port='5002')
