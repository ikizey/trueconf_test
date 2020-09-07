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

    @classmethod
    def last_user_id(cls):
        """Return last user id."""
        return max(int(key) for key in cls.get_users().keys())

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
        if not JSONHandler.id_exists(id):
            return {"message": "not exists"}

        if not JSONHandler.is_passed_json_valid(request.json):
            return {"message": "use format: {'name': <name>}"}

        user = {"id": id}
        user.update(request.json)

        JSONHandler.update_user(user)

        return {"message": "updated"}

    def delete(self, id):
        """Delete user by id."""
        if not JSONHandler.id_exists(id):
            return {"message": "not exists"}

        JSONHandler.delete_user(id)

        return {"message": "deleted"}


class UserByName(Resource):
    def put(self):
        """Add user."""
        if not JSONHandler.is_passed_json_valid(request.json):
            return {"message": "use format: {'name': <name>}"}

        id = str(JSONHandler.last_user_id() + 1)
        user = {"id": id}
        user.update(request.json)

        JSONHandler.update_user(user)

        return user


api.add_resource(Users, "/")
api.add_resource(UserById, "/user/<id>")
api.add_resource(UserByName, "/users/add")

if __name__ == "__main__":
    app.run(debug=True)