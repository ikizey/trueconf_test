import json
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        return self._read_users_json()

    def _read_users_json(self):
        with open("users_db.json", "r") as usersJSON:
            return json.load(usersJSON)


class User(Resource):
    def get(self, id):
        return self._get_user_from_json(id)

    def _get_user_from_json(self, id):
        with open("users_db.json", "r") as usersJSON:
            users = json.load(usersJSON)
            return users.get(id, {"message": "not exists"})


api.add_resource(Users, "/")
api.add_resource(User, "/user/<id>")

if __name__ == "__main__":
    app.run(debug=True)