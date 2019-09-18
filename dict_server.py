import socket
import os
import sys
import pymysql
import select

class Server:
    def __init__(self):
        self.address = ("localhost", 80)
        self.connection = 'host="localhost", port=3306, user="seal", password="1234", database="dict", charset="utf8"'
        self.tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.rlist = [self.tcpserver]
        self.wlist = []
        self.xlist = []
        try:
            self.conn = pymysql.connect(self.connection)
            self.cursor = self.conn.cursor()
            self.tcpserver.bind(self.address)
            self.tcpserver.listen(10)
        except Exception as e:
            exit(e)

    def log(self, str):
        pass

    def server_for(self, c):
        flag = ""
        data = c.recv(1024)
        if not data or data[3:]:
            return
        flag = data[0:2]
        message = data[3:]
        if flag == "SU":#sign up
            pass
        elif flag == "SI":#sign in
            pass
        elif flag == "CH":#check history
            pass
        elif flag == "FW":#find word
            pass
        elif flag == "LO":#log out
            pass
        elif flag == "FW":#find word
            pass
        elif flag == "FW":#find word
            pass
        elif flag == "FW":#find word
            pass

    def server_forever(self):
        while True:
            rs, ws, xs = select.select(self.rlist, self.wlist, self.xlist) #阻塞
            for r in rs:
                if r is self.tcpserver:
                    c, addr = r.accept()
                    self.log(addr)
                    self.rlist.append(c)
                elif r in rs:
                    self.server_for(r)

                elif r in ws:
                    pass

def main():
    server = Server()
    server.server_forever()

if __name__ == '__main__':
    main()