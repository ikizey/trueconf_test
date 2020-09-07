from flask import Flask, request
from flask_restful import Api, Resource

from jsonhandler import JsonHandler

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        """Return list of users."""
        return JsonHandler.get_users()


class UserById(Resource):
    def get(self, id):
        """Get user by id."""
        users = JsonHandler.get_users()
        return users.get(id, {"message": "not exists"})

    def post(self, id):
        """Update user data."""
        if not JsonHandler.id_exists(id):
            return {"message": "not exists"}

        if not JsonHandler.is_passed_json_valid(request.json):
            return {"message": "use format: {'name': <name>}"}

        user = {"id": id}
        user.update(request.json)

        JsonHandler.update_user(user)

        return {"message": "updated"}

    def delete(self, id):
        """Delete user by id."""
        if not JsonHandler.id_exists(id):
            return {"message": "not exists"}

        JsonHandler.delete_user(id)

        return {"message": "deleted"}


class UserByName(Resource):
    def put(self):
        """Add user."""
        if not JsonHandler.is_passed_json_valid(request.json):
            return {"message": "use format: {'name': <name>}"}

        id = str(JsonHandler.last_user_id() + 1)
        user = {"id": id}
        user.update(request.json)

        JsonHandler.update_user(user)

        return user


api.add_resource(Users, "/")
api.add_resource(UserById, "/user/<id>")
api.add_resource(UserByName, "/users/add")

if __name__ == "__main__":
    app.run(debug=True)
