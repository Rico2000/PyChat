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
        self.rooms = {
        }
        self.command_dict = {
            'lr': [self.list_rooms, 0],
            'join': [self.join_room, 1],
            'leave': [self.leave_room, 0],
            'penis': [self.leave_room, 0]
        }
        while True:
            
            connection, address = self.socket.accept()
            username = connection.recv(1024).decode()

            print('New connection. Username: '+str(username))
           

            self.list_of_clients.append(connection)
            self.usernames[connection] = username
            self.rooms[connection] = 'lobby'

            start_new_thread(self.handle_clients,(connection,address)) 

        conn.close()
        self.socket.close()
        
    def handle_clients(self,connection, address):
        connection.send("Willkommen im Chat".encode())
        connection.send("Commands: \n /lr - List rooms \n /join - Join Room \n /leave - Leave room".encode())
        while True:
            try: 
                message = connection.recv(1024).decode()
                if message:
                    if str(message).startswith('/'):
                        self.handle_command(message, connection)
                    else:
                        username = self.usernames[connection]
                        self.broadcast(username + ': ' + message, connection)
                else:
                    self.remove(connection)
            except Exception as e:

                print(e)
                continue

    def handle_command(self, message, connection):
        tokens = message.split()
        command = tokens[0][1:]
        args = tokens[1:]

        if not command in self.command_dict:
            print('Command not found')
        else:
            cmd = self.command_dict[command]
            if len(args) != cmd[1]:
                print('Wrong number of arguments')
            elif len(args) == 0:
                cmd[0](connection)
            else:
                cmd[0](connection, args)
    
    def list_rooms(self, connection):
        rooms_list = ' '.join([r for r in set(self.rooms.values())])
        connection.send(rooms_list.encode())

    def join_room(self, connection, args):
        self.rooms[connection] = args[0]
        connection.send((f'Welcome in Room {args[0]}').encode())


    def leave_room(self, connection):
        self.rooms[connection] = 'lobby'
        connection.send((f'Welcome in the Lobby').encode())



    def broadcast(self, message, connection):
        for client in self.list_of_clients:
            if client!=connection and self.rooms[connection] == self.rooms[client]:
                try:
                    client.send(message.encode())
                except:
                    client.close()
                    self.remove(clients) 

    def remove(self,connection):
        if connection in self.list_of_clients:
            self.list_of_clients.remove(connection)

server = Server()
    

