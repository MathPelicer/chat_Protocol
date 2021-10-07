from Lobbydatabase import lobbyDatabase
import socket
import _thread
import re
from model.User import User
from model.Lobby import Lobby
from UserDatabase import UserDatabase

host = '0.0.0.0'
port = 8080

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = ""
        self.connections = []
        self.user_data_list = []

    def create_and_bind_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(100)

    def new_connection(self):
        conn, addr = self.sock.accept()
        self.connections.append(conn)
        print(f'{addr[0]} connected')
        return conn, addr

    def sendMessageToLobby(self, message, user, conn, lobby_name):
        if len(self.connections) > 1:
            for users in self.connections:
                if users != conn:
                    if user["lobby"] == lobby_name: 
                        if message == "/leave":
                            user["lobby"] = ""
                            users.send(f"{user['name']} left the lobby\n".encode())    
                            conn.send("You left the lobby\n".encode())

                        elif message == "/list":
                            conn.send(f"\nUsers in this lobby:\n\n".encode())
                            for i in range(len(self.user_data_list)):
                                print(self.user_data_list[i])
                                if self.user_data_list[i]['lobby'] == lobby_name:
                                    conn.send(f"{self.user_data_list[i]['name']}\n".encode())
                        
                        elif message == "/help":
                            conn.send("Lobby commands...\n\n".encode())
                            conn.send("/list - list users that are in the same lobby as you\n/leave - to leave the server you're currently in".encode())
                        else:
                            print(users)
                            users.send(f"{user['name']}: {message}\n".encode())
        else:
            if message == "/leave":
                user["lobby"] = ""
                conn.send("You left the lobby\n\n".encode())
            elif message == "/list":
                conn.send(f"There's nobody here besides you :c\n\n".encode())
                   


    def run(self, conn, addr):
        conn.send("==========================================\n".encode())
        conn.send("welcome to chat room!\n\n".encode())
        conn.send("/register - register a new user\n/login - login into an existing account\n/join_lobby - join an existing lobby\n/create_lobby - create a new lobby\n/list_lobby - list all the existing lobbies\n/logout - logout from your current account\n/help - list available commands\n\n".encode())

        user_database = UserDatabase()
        lobby_database = lobbyDatabase()

        
        lobby_list = lobby_database.loadAllLobbyInstances()
        user = ''

        while True:
            msg = conn.recv(2048).decode()
            msg = re.sub(r'\r\n', '', msg)
            
            # registra um novo usuario 
            if msg == "/register":
                conn.send("Lets register your account\n\n".encode())
                conn.send("Enter a username for your account: ".encode())

                name = conn.recv(2048).decode()
                name = re.sub(r'\r\n', '', name)

                usernameData = user_database.searchForUsername(name)

                if usernameData == False:

                    conn.send(f"\n\nOkay {name} now whats the password you want to use?\n".encode())
                    conn.send(f"Password: ".encode())

                    psw = conn.recv(2048).decode()
                    psw = re.sub(r'\r\n', '', psw)

                    conn.send(f"\n\nPlease {name} confirm your password\n".encode())
                    conn.send(f"Confirm password: ".encode())

                    psw_conf = conn.recv(2048).decode()
                    psw_conf = re.sub(r'\r\n', '', psw_conf)

                    if psw != psw_conf:
                        conn.send(f"Your password does not match\n".encode())
                        conn.send(f"Try /register again\n\n".encode())
                    else:
                        new_user = User(name, psw)
                        resp = user_database.saveNewUser(new_user)
                
                else:
                    conn.send(f"There's already an account registered with this nickname\n\n".encode())


            # realiza login
            elif msg == "/login":
                print(user)
                if user == '' or user["is_logged"] == "False":
                    conn.send("Lets log you in\n\n".encode())
                    conn.send("Enter your username: ".encode())

                    username = conn.recv(2048).decode()
                    username = re.sub(r'\r\n', '', username)

                    user = user_database.searchForUsername(username)

                    if user == False:
                        conn.send("Theres no user with this name in our database.\n".encode())    
                        conn.send("You can create a new one using '/register'.\n\n".encode()) 

                    if user["is_logged"] == "True":
                        conn.send("You're already logged in\n\n".encode())   
                    else:
                        conn.send("Enter your password: ".encode())

                        psw = conn.recv(2048).decode()
                        psw = re.sub(r'\r\n', '', psw)

                        if psw == user["password"]:
                            conn.send("Login successfully!\n\n".encode())
                            user_database.updateLoginState(username)
                            user["is_logged"] = "True"
                            self.user_data_list.append(user)
                        else:
                            conn.send("Wrong password!\n\n".encode())
                else:
                    conn.send(f"You're already logged in as {user['name']}\n\n".encode())

            # realiza logout
            elif msg == "/logout":
                if user != '' and user["is_logged"] == "True":
                    conn.send("Lets log you out\n\n".encode())
                    
                    user_database.updateLoginState(user["name"])
                    user["is_logged"] = "False"

                    #for i in range(len(self.connections)):
                    #    if self.connections[i] == conn:
                    #        self.connections.pop(i)
                    
                    user = ""

                    conn.send("Logged out... Good bye my friend\n\n".encode())
                else:
                    conn.send("You're not logged in any account.\n\n".encode())

            # cria uma nova sala
            elif msg == "/create_lobby":
                if user != '' and user["is_logged"] == "True":
                    conn.send("Lets create a new lobby\n\n".encode())
                    conn.send("First give you lobby a name:".encode())

                    lobby_name = conn.recv(2048).decode()
                    lobby_name = re.sub(r'\r\n', '', lobby_name)

                    lobby = Lobby(lobby_name)
                    new_lobby = lobby_database.createNewlobby(lobby) 
                    lobby_list.append(lobby)
                else:
                    conn.send("You must first be logged in to create a new lobby\n\n".encode())
            
            elif msg == "/list_lobby":
                if user != '' and user["is_logged"] == "True":

                    lobby_data = lobby_database.loadAllLobby()
                    for lobby in lobby_data:
                        conn.send(f"-> {lobby['name']}\n".encode())
                else:
                    conn.send("\nYou must first be logged in to see the lobbies available\n\n".encode())
                    
            # entra em uma sala ja existente
            elif msg == "/join_lobby":
                if user != '' and user["is_logged"] == "True":
                    conn.send("Lets join a lobby\n".encode())
                    conn.send("Which lobby do you want to enter?\n\n".encode())

                    lobby_data = lobby_database.loadAllLobby()
                    for lobby in lobby_data:
                        conn.send(f"-> {lobby['name']}\n".encode())

                    conn.send("\nEnter the lobby name you want to be in: ".encode())

                    lobby_name = conn.recv(2048).decode()
                    lobby_name = re.sub(r'\r\n', '', lobby_name)

                    if lobby != False:
                        user["lobby"] = lobby_name

                        for i in range(len(self.user_data_list)):
                            if self.user_data_list[i]['name'] == user['name']:
                                self.user_data_list[i]['lobby'] = lobby_name

                        conn.send(f'\u001B[2J'.encode())
                        conn.send(f"============================================\n\n".encode())
                        conn.send(f"Welcome to {lobby_name}\n\n".encode())

                        while True:
                            message = conn.recv(2048).decode()
                            message = re.sub(r'\r\n', '', message)

                            if message:
                                self.sendMessageToLobby(message, user, conn, lobby_name)

                                if message == "/leave":
                                    conn.send(f"You're back to the main menu\n\n".encode())
                                    break

                    
                else:
                    conn.send("You must first be logged in to create a new lobby\n\n".encode())
            
            elif msg == "/help":
                conn.send("/register - register a new user\n/login - login into an existing account\n/join_lobby - join an existing lobby\n/create_lobby - create a new lobby\n/list_lobby - list all the existing lobbies\n/logout - logout from your current account\n/help - list available commands\n\n".encode())

            else:
                conn.send("Enter a valid command.\n\n".encode())
                conn.send("/register - register a new user\n/login - login into an existing account\n/join_lobby - join an existing lobby\n/create_lobby - create a new lobby\n/list_lobby - list all the existing lobbies\n/logout - logout from your current account\n/help - list available commands\n\n".encode())
            # more comands


server = Server(host, port)
server.create_and_bind_socket()

while True:
    conn, addr = server.new_connection()
    _thread.start_new_thread(server.run, (conn, addr))

