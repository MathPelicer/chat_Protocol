from model.Lobby import Lobby
import json

class lobbyDatabase():
    def __init__(self):
        pass

    def loadAllLobby(self):
        with open("lobby.json", 'r', encoding="utf-8") as file:
            lobby_info = json.load(file)
            return lobby_info
    
    def loadAllLobbyInstances(self):
        list_of_lobbies = []
        with open("lobby.json", 'r', encoding="utf-8") as file:
            lobby_info = json.load(file)
            for lobby in lobby_info:
                print(lobby)
                list_of_lobbies.append(Lobby(lobby['name']))
            
        return list_of_lobbies

    def searchForlobby_name(self, lobby_name):
        print(f"Searching for {lobby_name} in the database")

        lobby_info = self.loadAllLobby()

        for lobby in lobby_info:
            if lobby["name"] == lobby_name:
                print(f"lobby found")
                return Lobby(lobby["name"])

        return False

    def createNewlobby(self, new_lobby):
        print("Saving a new lobby...")

        new_lobby = new_lobby.get_lobby()
        print(f"New lobby => {new_lobby}")
        try:

            lobby_info = self.loadAllLobby()
            lobby_info.append(new_lobby)
            
            with open("lobby.json", 'w', encoding="utf-8") as file:
                data = json.dumps(lobby_info, indent=4)
                file.write(data)

            print("New lobby registered")
        except:
            print("Something happened")

    