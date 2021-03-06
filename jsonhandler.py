import json
from pathlib import Path


class JsonHandler:
    """Handle json DB file."""

    json = "users_db.json"

    @classmethod
    def create_file(cls):
        """Create json file, if not exists."""
        if not Path(cls.json).is_file():
            file = open(cls.json, "w")
            file.close()

    @classmethod
    def get_users(cls):
        """Get all data from json."""
        with open(cls.json, "r") as usersJSON:
            try:
                users = json.load(usersJSON)
            except ValueError:
                return json.loads("{}")
            else:
                return users

    @classmethod
    def _write_users(cls, data):
        """Write all data to json."""
        with open(cls.json, "w") as usersJSON:
            json.dump(data, usersJSON)

    @classmethod
    def update_user(cls, user):
        """Add/update user data."""
        users = cls.get_users()
        users[user["id"]] = user
        cls._write_users(users)

    @classmethod
    def delete_user(cls, id):
        """Delete user data."""
        users = cls.get_users()
        del users[id]
        cls._write_users(users)

    @classmethod
    def last_user_id(cls):
        """Return last user id."""
        users = cls.get_users()
        if users:
            return max(int(key) for key in users.keys())
        else:
            return 0

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
