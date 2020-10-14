import uuid
import csv
from datetime import datetime
from flask import Flask, jsonify, request

from models import User

app = Flask(__name__)

operations_list = []

@app.route('/datetimenow', methods=['GET'])
def get_datetimenow():
    now = datetime.now()
    formatted_datetime = datetime.strftime(
        now, '%Y-%m-%d %H:%M:%S'
    )

    return jsonify({'datetime_now': formatted_datetime}), 200


@app.route('/inverter', methods=['POST'])
def text_inverter():
    data = request.get_json()
    inverted_text = data.get('text')[::-1]

    return jsonify(inverted_text), 200


@app.route('/operations', methods=['POST'])
def make_operation():
    # add, sub, mul, div
    data = request.get_json()

    number_1 = int(data.get('number_1'))
    number_2 = int(data.get('number_2'))
    operator = data.get('operator')
    now = datetime.now()

    if operator == 'add':
        result = number_1 + number_2
    elif operator == 'sub':
        result = number_1 - number_2
    elif operator == 'mul':
        result = number_1 * number_2
    elif operator == 'div':
        result = number_1 / number_2
    else:
        return jsonify({'msg': 'Invalid operator'})

    operation = {
        'id': uuid.uuid4(),
        'number_1': number_1, 'number_2': number_2,
        'operator': operator, 'result': result,
        'timestamp': now
    }

    operations_list.append(operation)

    return jsonify({'operation': operation}), 201


@app.route('/operations', methods=['GET'])
def list_operations():
    return jsonify(operations_list), 200

## USERS ##
@app.route('/users', methods=['GET'])
def get_all_users():
    users_list = []

    with open('users.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        # line_count = 0
        for row in csv_reader:
            users_list.append(User(**row).serialize())
            # user = User(
            #     id=row['id'],
            #     name=row['name'],
            #     birth_date=row['birth_date'],
            #     gender=row['gender']
            # )
            # users_list.append(user.serialize())

        return jsonify(users_list), 200


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(**data)

    with open('users.csv', 'a') as csv_file:
        fieldnames = ['id', 'name', 'birth_date', 'gender', 'cep']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        writer.writerow(user.serialize())

    return jsonify(user.serialize()), 201


@app.route('/users/<id>', methods=['PATCH'])
def update_user(id):
    users_list = []
    data = request.get_json()
    _user = None

    with open('users.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        # line_count = 0
        for row in csv_reader:
            users_list.append(User(**row))

    for user in users_list:
        if user.id == id:
            user.name = data.get('name', user.name)
            user.birth_date = data.get('birth_date', user.birth_date)
            user.gender = data.get('gender', user.gender)
            _user = user
    with open('users.csv', 'w') as csv_file:
        fieldnames = ['id', 'name', 'birth_date', 'gender']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for user in users_list:
            writer.writerow(user.serialize())

    return jsonify(_user.serialize()), 200


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    users_list = []

    with open('users.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            users_list.append(User(**row))

    for user in users_list:
        if user.id == id:
            users_list.remove(user)

    with open('users.csv', 'w') as csv_file:
        fieldnames = ['id', 'name', 'birth_date', 'gender']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for user in users_list:
            writer.writerow(user.serialize())

    return jsonify(), 204


@app.route('/users/<id>')
def get_user_by_id(id):
    with open('users.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            if row['id'] == id:
                return jsonify(User(**row).serialize(detail=True))


if __name__ == '__main__':
    app.run(debug=True)
