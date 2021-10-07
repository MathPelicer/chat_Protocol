from model.User import User
import json

class UserDatabase():
    def __init__(self):
        pass

    def loadAllUsers(self):
        with open("users.json", 'r', encoding="utf-8") as file:
            users_info = json.load(file)
            return users_info

    def saveNewUser(self, new_user):
        print("Saving a new user...")

        new_user = new_user.getUser()
        print(f"New user => {new_user}")
        try:

            users_info = self.loadAllUsers()
            users_info.append(new_user)
            
            with open("users.json", 'w', encoding="utf-8") as file:
                data = json.dumps(users_info, indent=4)
                file.write(data)

            print("New user registered")
        except:
            print("Something happened")

    def searchForUsername(self, username):
        print(f"Searching for {username} in the database")

        users_info = self.loadAllUsers()

        for user in users_info:
            if user["name"] == username:
                print(f"User found")
                return user

        return False

    def updateLoginState(self, username):
        users_data = self.loadAllUsers()

        for user in users_data:
            if user["name"] == username and user["is_logged"] == "False":
                user["is_logged"] = "True"
            elif user["name"] == username and user["is_logged"] == "True":
                user["is_logged"] = "False"
                self.updateLobby(username, "")
                

        with open("users.json", 'w', encoding="utf-8") as file:
                data = json.dumps(users_data, indent=4)
                file.write(data)

    def updateLobby(self, username, lobby_name):
        users_data = self.loadAllUsers()

        for user in users_data:
            if user["name"] == username and user["is_logged"] == "False":
                return False
            elif user["name"] == username and user["is_logged"] == "True":
                user["lobby"] = lobby_name

        with open("users.json", 'w', encoding="utf-8") as file:
                data = json.dumps(users_data, indent=4)
                file.write(data)