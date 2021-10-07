class Lobby():
    def __init__(self, name):
        self.name = name
        self.users = []

    def get_lobby(self):
        lobby = {
            "name": self.name,
            "users": self.users
        }

        return lobby

    def add_user(self, user):
        self.users.append(user)

    