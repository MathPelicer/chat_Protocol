class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_logged = "False"
        self.lobby = ""

    def getUser(self):
        user = {
            "name": self.username,
            "password": self.password,
            "is_logged": self.is_logged,
            "lobby": self.lobby
        }

        return user
