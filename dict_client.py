import socket
import os
import sys
import time
import getpass

class Client:
    def __init__(self):
        self.tcpclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpclient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.nowload_username = ""
        self.address = ("localhost", 80)
        self.tcpclient.connect(self.address)

    def send_to_server(self, message):
        self.tcpclient.send(message.encode())
        return self.tcpclient.recv(1024).decode()

    def log_menu(self):
        os.system("cls")
        print("Words Dict System\n\n1. sign in\n2. sign up\n3. exit\n")
        temp = input(">>")
        if temp == "1":
            t = 0
            username = input("name: ")
            password = getpass.getpass("pass: ")
            result = self.send_to_server("SI "+username+"#"+password)#YE / NO
            if result == "YE":
                print("sign in successful,prepare to loading main menu")
                while t:
                    print(".", end=" ")
                    sys.stdout.flush()
                    time.sleep(1)
                    t -= 1
                self.main_menu(username)
            else:
                print(result, "wrong username or password, please input again")
                time.sleep(2)
                self.log_menu()
        elif temp == "2":
            username = input("input your name: ")
            password = getpass.getpass("input your pass: ")
            repass = getpass.getpass("input pass again: ")
            t = 0
            if repass == password:
                result = self.send_to_server("SU " + username + "#" + password)  # yes / have user
                if result == "YE":#yes
                    print("sign up successful. auto sign in,prepare to loading main menu", end=" ")
                    while t:
                        print(".", end=" ")
                        sys.stdout.flush()
                        time.sleep(1)
                        t -= 1
                    self.main_menu(username)
                elif result == "HU":#have user
                    print("user is exist, please input again")
                    time.sleep(2)
            else:
                print("repass != pass")
            self.log_menu()
        elif temp == "3":
            return  # exit
        else:
            self.log_menu()

    def main_menu(self, username):
        os.system("cls")
        print("Main System\n\n1. find words\n2. check history\n3. log out\n")
        temp = input(">>")
        if temp == "1":
            word = input("input word: ")
            result = self.send_to_server("FW " + username + " " + word)
            if result[0:2] == "OK":#find ok
                print(word,  ": ",result[3:])
            elif result.split(" ")[0] == "NF":#not find word
                print("word not found")
            input("press any key to continue..")
            self.main_menu(username)
        elif temp == "2":
            result = self.send_to_server("CH " + username)#check history
            # print(result)
            if result[0:2] == "OK":  # find history ok
                result = result[3:]
                print("    word             time\n")
                for record in result.split("$"):
                    if record:
                        print("  %-16s  %s"%(record.split("#")[0], record.split("#")[1]))
            else:  # not find word
                print("history not found\n")
            input("press any key to continue..")
            self.main_menu(username)
        elif temp == "3":
            self.send_to_server("LO")#log out
            # self.tcpclient.close()
            # self.tcpclient.connect(self.address)
            self.log_menu()
        else:
            self.main_menu(username)

def main():
    client = Client()
    client.log_menu()

if __name__ == '__main__':
    main()