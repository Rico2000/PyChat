import socket
import threading
import json
from time import sleep
import sys


class Client:
    def __init__(self):
        self.pp_flag = False
        self.create_connection()
        self.client_server = None
        self.start()

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        while True:
            try:
                self.hostname = input('Enter hostname: ')
                self.server_port = int(input('Enter port: '))
                self.s.connect((self.hostname, self.server_port))
                break
            except Exception as e:
                print(e)
                print("Couldn't connect to server")
        self.username = input('Enter username: ')
        self.s.send(self.username.encode())

        message_handler = threading.Thread(
            target=self.handle_messages, args=())
        message_handler.start()

        input_handler = threading.Thread(target=self.input_handler, args=())
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
        args = message.split()[1:]
        port_self = int(args[0])
        hostname_peer = args[1]
        port_peer = int(args[2])
        self.client_server = Server_Client(self.hostname, port_self)
        self.pp_thread = threading.Thread(
            target=self.client_server.start, name="Thread-Server")
        self.pp_thread.start()
        self.server_socket = self.s
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((hostname_peer, port_peer))

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
        message_handler = threading.Thread(
            target=self.handle_messages, args=())
        message_handler.start()


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


if __name__ == "__main__":
    Client()
