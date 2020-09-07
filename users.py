import json
import pathlib
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


api.add_resource(Users, "/")

if __name__ == "__main__":
    app.run(debug=True)