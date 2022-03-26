from email import message
import socket
import threading
import json
from time import sleep

class Client:
    def __init__(self):
        self.pp_flag = False
        self.create_connection()
        self.client_server = None

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        while True:
            try:
                host = "127.0.0.1"
                port = 1244
                self.s.connect((host,port))
                
                break
            except:
                print("Couldn't connect to server")
        self.username = input('Enter username: ')
        self.s.send(self.username.encode())
        
        message_handler = threading.Thread(target=self.handle_messages,args=())
        message_handler.start()

        input_handler = threading.Thread(target=self.input_handler,args=())
        input_handler.start()
    

    def handle_messages(self):
        while True:
            if not self.pp_flag:
                message = self.s.recv(1204).decode()
                print(message)
                self.pp_flag = (message.startswith("/pp") or self.pp_flag)
                if message.startswith("/pp"):
                    self.start_pp_chat(message)
            else:
                if not self.pp_thread.is_alive():
                    self.leave_pp()


    def start_pp_chat(self, message):
        tokens = message.split()[1:]
        port_self = int(tokens[0])
        hostname = tokens[1]
        port = int(tokens[2])
        #HUHUHUHUII
        self.client_server = Server_Client(hostname,port_self)
        self.pp_thread = threading.Thread(target=self.client_server.start, name="Thread-Server")
        self.pp_thread.start()
        self.server_socket = self.s
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect((hostname, port))

    def input_handler(self):
        while True:
            message = input()
            if self.pp_flag:
                if message.startswith('/leave'):
                    self.s.send(('/leave').encode())
                    self.leave_pp()
                else:
                    self.s.send((self.username + ': ' + message).encode())   
            else:
                self.s.send(message.encode())
    
    def leave_pp(self):
        self.pp_flag = False
        self.s = self.server_socket
        print('Peer-To-Peer verlassen')
        message_handler = threading.Thread(target=self.handle_messages,args=())
        message_handler.start()

client = Client()

class Server_Client():

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
       
        
    def start(self):
        self.server.listen(1)
        client_connection, address = self.server.accept()
        while True:
            data = client_connection.recv(1024)
            if data:
                message = data.decode()
                if message.startswith('/leave'):
                    break
                else:
                    print(message)