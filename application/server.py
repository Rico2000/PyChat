from email import message
import sys
import os
import socket 
from _thread import *

class Server:
    def __init__(self):
        self.socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ip = "127.0.0.1"
        self.port = 1244
        self.socket.bind((self.ip,self.port))
        self.socket.listen(100)
        self.list_of_clients = []
        self.usernames = {}
        while True:
            
            connection, address = self.socket.accept()
            username = connection.recv(1024).decode()

            print('New connection. Username: '+str(username))
           

            self.list_of_clients.append(connection)
            self.usernames[connection] = username

            start_new_thread(self.handle_clients,(connection,address)) 

        conn.close()
        self.socket.close()
        
    def handle_clients(self,connection, address):
        connection.send("Willkommen im Chat".encode())
        while True:
            try: 
                message = connection.recv(1024)
                if message:
                    self.broadcast(message, connection)
                else:
                    self.remove(connection)
            except:
                continue

    def broadcast(self,message, connection):
        for clients in self.list_of_clients:
            if clients!=connection:
                try:
                    clients.send(message)
                except:
                    clients.close()
                    self.remove(clients) 

    def remove(self,connection):
        if connection in self.list_of_clients:
            self.list_of_clients.remove(connection)

server = Server()
    

