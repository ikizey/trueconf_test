import json
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        return self._read_users_json()

    def _read_users_json(self):
        with open("users_db.json", "r") as usersJSON:
            return json.load(usersJSON)


class UserById(Resource):
    def get(self, id):
        return self._get_user_from_json(id)

    def _get_user_from_json(self, id):
        with open("users_db.json", "r") as usersJSON:
            users = json.load(usersJSON)
            return users.get(id, {"message": "not exists"})


class UserByName(Resource):
    def put(self):
        json = request.json
        print(json.keys())
        return self._add_user(json)

    def _is_valid(self, post_json):
        return True if list(post_json.keys()) == ['name'] else False

    def _get_max_id(self):
        return max(int(key) for key in Users().get().keys())

    def _add_user(self, json):
        if not self._is_valid(json):
            return {"message": "use format: {'name': <name>}"}

        id = self._get_max_id() + 1
        user = {"id": id}
        user.update(json)
        print(id, user, json)
        self._add_user_to_json_db(user, id)

        return user

    def _add_user_to_json_db(self, user, id):
        with open("users_db.json", "r+") as jsonFile:
            data = json.load(jsonFile)

            data[id] = user

            jsonFile.seek(0)
            json.dump(data, jsonFile)
            jsonFile.truncate()


api.add_resource(Users, "/")
api.add_resource(UserById, "/user/<id>")
api.add_resource(UserByName, "/users/add")

if __name__ == "__main__":
    app.run(debug=True)