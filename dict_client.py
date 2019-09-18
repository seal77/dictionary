import socket
import os
import sys

class Client:
    def __init__(self):
        self.tcpclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpclient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        pass

    def log_menu(self):
        print("Words Dict System\n\n1. sign in\n2. sign up\n3. exit\n")
        temp = input(">>")
        if temp == 1:
            pass
        elif

    def main_menu(self):
        pass

def main():
    client = Client()
    client.log_menu()

if __name__ == '__main__':
    main()