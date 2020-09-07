import json
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class JSONHandler:
    """Handle json DB file."""

    json = "users_db.json"

    @classmethod
    def get_users(cls):
        """Get all data from json."""
        with open(cls.json, "r") as usersJSON:
            return json.load(usersJSON)


class Users(Resource):
    def get(self):
        """Return list of users."""
        return JSONHandler.get_users()


class UserById(Resource):
    def get(self, id):
        """Get user by id."""
        users = JSONHandler.get_users()
        return users.get(id, {"message": "not exists"})

    def post(self, id):
        return self._update_user(id)

    def _update_user(self, id):
        json = request.json
        if not self._is_update_json_valid(json):
            return {"message": "use format: {'name': <name>}"}
        user = {"id": id}
        user.update(json)
        users = self._get_users()
        users[id] = user
        self._update_users(users)
        return {"message": "updated"}

    def _is_update_json_valid(self, json):
        return True if list(json.keys()) == ['name'] else False

    def delete(self, id):
        return self._delete_user_from_json(id)

    def _delete_user_from_json(self, id):
        users = self._get_users()
        if not id in users:
            return {"message": "not exists"}
        del users[id]
        self._update_users(users)
        return {"message": "deleted"}

    def _get_users(self):
        return Users().get()

    def _update_users(self, users):
        with open("users_db.json", "w") as jsonFile:
            json.dump(users, jsonFile)


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

        id = str(self._get_max_id() + 1)
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