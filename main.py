from flask import (Flask, jsonify)
import names
import random
from typing import Any

from service import Connection


app = Flask(__name__)
conn: Connection = Connection()
conn.create_tables()

@app.route('/', methods=['GET'])
def main_page():
    return jsonify({
        "name" : "Toliban",
        "lastname" : "Brick"
    })

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    users = conn.get_user()
    data: list[dict] = []
    for i in users:
        data.append({
            'id' : i[0],
            'name' : i[1],
            'login' : i[2],
            'password' : i[3]
        })

    return jsonify(data)

@app.route('/api/v1/users/<int:id>', methods=['GET'])
def get_user(id):
    users = conn.get_user()
    data: list[dict] = []
    for i in users:
        data.append({
            'id' : i[0],
            'name' : i[1],
            'login' : i[2],
            'password' : i[3]
        })

    return jsonify(data[id-1])


@app.route('/gen-users', methods=['GET'])
def second_page():
    TOTAL_USERS = 200
    email_patterns = [
        'gmail.com', 'mail.com', 'yandex.com', 'kahoo.com', 'bk.ru', 'inbox.com', 'yahoo.com', 'microsoft.com', 'ok.ru'
    ]
    if len(conn.get_user()) >= TOTAL_USERS:
        return jsonify({
            'result' : 'too many users'
        })
    for i in range(TOTAL_USERS):
        name = names.get_first_name()
        conn.create_user(
            name=name, 
            login='{0}@{1}'.format(name, random.choice(email_patterns)), 
            password='qwerty')
    return jsonify({
        'result' : 'Users is create'
    })

if __name__ == '__main__':
    app.run(port=8090, debug=True)