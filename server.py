from socket import *
import os
import sys
import codecs
import glob

def Server():
    #archive_path_list = getListOfFiles(PATH)
    #get_archive_path_list(path_list_file)
    #print(f"LIST OF PATHS => {archive_path_list}")

    HOST = ''
    PORT = 9000

    server_socket = socket(AF_INET, SOCK_STREAM)
    orig = (HOST, PORT)
    server_socket.bind(orig)
    server_socket.listen(1)

    try:
        while(1):
            (connectionSocket, addr) = server_socket.accept()
            #pid = os.fork()

            #if pid == 0:
            while True:
                print("Cliente {} conectado ao servidor".format(addr))

                request = connectionSocket.recv(1024).decode()
                print(request)

                connectionSocket.sendall(request.encode())

                #connectionSocket.close()
            #else:
            #    connectionSocket.close()

    except KeyboardInterrupt:
        print("\n Shutting down... \n")
    except Exception as exc:
        print("Error: \n")
        print(exc)

print("Access http://localhost:9000")
Server()