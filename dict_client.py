import socket
import os
import sys
import time

class Client:
    def __init__(self):
        self.tcpclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpclient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.nowload_username = ""

    def send_to_server(self, message):
        self.tcpclient.send(message.encode())
        return self.tcpclient.recv(1024).decode()

    def log_menu(self):
        os.system("cls")
        print("Words Dict System\n\n1. sign in\n2. sign up\n3. exit\n")
        temp = input(">>")
        if temp == 1:
            t = 3
            username = input("name: ")
            password = input("pass: ")
            result = self.send_to_server("SI "+username+"#"+password)#YE / NO
            if result == "YE":
                print("sign in successful,prepare to loading main menu")
                while t:
                    print(".")
                    time.sleep(1)
                    t -= 1
                self.main_menu(username)
            elif result == "NO":
                print("wrong username or password, please input again")
                time.sleep(2)
        elif temp == 2:
            pass
        else:
            return#exit

    def main_menu(self):
        pass

def main():
    client = Client()
    client.log_menu()

if __name__ == '__main__':
    main()