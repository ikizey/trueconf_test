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

    @classmethod
    def _write_users(cls, data):
        """Write all data to json."""
        with open(cls.json, "w") as usersJSON:
            json.dump(data, usersJSON)

    @classmethod
    def update_user(cls, user):
        """Update data."""
        users = cls.get_users()
        users[user["id"]] = user
        cls._write_users(users)

    @classmethod
    def delete_user(cls, id):
        """Update data."""
        users = cls.get_users()
        del users[id]
        cls._write_users(users)

    @staticmethod
    def is_passed_json_valid(json):
        """Check if passed json is valid."""
        try:
            name = json["name"]
        except:
            return False
        return True if name and len(json) == 1 else False

    @classmethod
    def id_exists(cls, id):
        """Check if id is present."""
        return id in cls.get_users()


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
        """Update user data."""
        if JSONHandler.id_exists(id):
            return {"message": "not exists"}

        if not JSONHandler.is_passed_json_valid(request.json):
            return {"message": "use format: {'name': <name>}"}

        user = {"id": id}
        user.update(request.json)

        JSONHandler.update_user(user)

        return {"message": "updated"}

    def delete(self, id):
        if JSONHandler.id_exists(id):
            return {"message": "not exists"}

        JSONHandler.delete_user(id)

        return {"message": "deleted"}

    def _update_users(self, users):
        with open("users_db.json", "w") as jsonFile:
            json.dump(users, jsonFile)


class UserByName(Resource):
    def put(self):
        json = request.json
        print(json.keys())
        return self._add_user(json)

    def _get_max_id(self):
        return max(int(key) for key in Users().get().keys())

    def _add_user(self, json):
        if not JSONHandler.is_passed_json_valid(json):
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