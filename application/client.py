import socket
import threading

class Client:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        while True:
            try:
                host = input('Enter host name:')
                port = int(input('Enter port:'))
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
            print(self.s.recv(1204).decode())

    def input_handler(self):
        while True:
            self.s.send(input().encode())

client = Client()