from flask import Flask, jsonify, Blueprint, request
import uuid
from datetime import datetime
from http import HTTPStatus
import requests


class User:
    def __init__(self, name, birth_date, gender):
        self._id = str(uuid.uuid4())
        self._name = name
        self._birth_date = birth_date
        self._gender = gender

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = value

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        self._gender = value

    def serialize(self):
        return {
            'id': self._id,
            'name': self._name,
            'birth_date': self._birth_date,
            'gender': self._gender
        }


app = Flask(__name__)


@app.route('/users', methods=['GET'])
def get_users():
    gender = request.args.get('gender')
    users_list = [user.serialize() for user in users]

    if gender:
        users_list = [
            user.serialize() for user in users if user.gender == gender
        ]

    return jsonify(users_list), HTTPStatus.OK


@app.route('/users/<id>', methods=['GET'])
def get_user_by_id(id):
    for user in users:
        if id == user.id:
            return jsonify(user.serialize()), HTTPStatus.OK

    return jsonify(), HTTPStatus.NOT_FOUND


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    name = data.get('name', 'Anônimo')
    birth_date = data.get('birth_date')
    birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    gender = data.get('gender')

    user = User(name, birth_date, gender)
    users.append(user)

    return jsonify(user.serialize()), HTTPStatus.OK


@app.route('/users/<id>', methods=['PATCH'])
def update_user(id):
    data = request.get_json()

    name = data.get('name')
    birth_date = data.get('birth_date')

    actual_user = None

    for user in users:
        if user.id == id:
            actual_user = user

    if name:
        actual_user.name = name
    if birth_date:
        actual_user.birth_date = datetime.strptime(birth_date, '%Y-%m-%d')

    return jsonify(actual_user.serialize()), HTTPStatus.OK


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    for user in users:
        if user.id == id:
            users.remove(user)
            return jsonify(), HTTPStatus.NO_CONTENT

    return jsonify(), HTTPStatus.NOT_FOUND

@app.route('/<name>')
@app.route('/index')
def index(name):
    return f"Hello, {name}."


# int, float, path
@app.route('/square/<int:number>')
def square(number):
    # return f'{number * number}'
    return jsonify(number * number)


@app.route('/onedollar/<currency>', methods=['GET'])
def get_one_dolar(currency):
    url = 'https://api.exchangeratesapi.io/latest?base=USD'
    response_data = requests.get(url).json()

    value = response_data.get('rates').get(currency)
    value = float("{:.2f}".format(value))

    return jsonify(value), HTTPStatus.OK


if __name__ == '__main__':
    app.run(debug=True)


