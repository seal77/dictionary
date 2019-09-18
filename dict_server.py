import socket
import os
import sys
import pymysql
import select
import time
import hashlib


class Server:
    def __init__(self):
        # self.hash = hashlib.md5()
        self.address = ("localhost", 80)
        self.connection = 'host="localhost", port=3306, user="seal", password="1234", database="dict", charset="utf8"'
        self.tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.rlist = [self.tcpserver]
        self.wlist = []
        self.xlist = []
        self.f = ""
        self.select_up = "SELECT COUNT(*) FROM user WHERE username=%s AND password=%s;"
        self.insert_up = "INSERT INTO user(username, password) VALUES(%s, %s);"
        self.check_username = "SELECT COUNT(*) FROM user WHERE username=%s;"
        self.select_history = "SELECT word,`time` FROM history WHERE uid in(SELECT id FROM user WHERE username=%s) ORDER BY `time` DESC LIMIT 10;"
        self.select_word = "SELECT word,mean FROM words WHERE word=%s;"
        self.insert_history = "INSERT INTO history(uid, word) VALUES((SELECT id FROM user WHERE username=%s LIMIT 1), %s);"
        # other sql
        try:
            self.conn = pymysql.connect(host="localhost", port=3306, user="seal", password="1234", database="dict",
                                        charset="utf8")
            self.cursor = self.conn.cursor()
            self.tcpserver.bind(self.address)
            self.tcpserver.listen(10)
            self.f = open("log.txt", "a")
        except Exception as e:
            exit(e)

    def log(self, string):
        print(string)
        self.f.write("[INFO] [" + time.ctime() + "] " + string + "\n")
        self.f.flush()

    def server_for(self, c):
        flag = ""
        data = c.recv(1024).decode()
        if not data:
            self.rlist.remove(c)
            c.close()
        if not data or not data[3:]:
            c.send(b"ERROR")
            return
        flag = data[0:2]
        message = data[3:]
        # print(flag, message)
        if flag == "SU":  # sign up
            info = message.split("#")
            username = info[0]
            password = info[1]
            self.cursor.execute(self.check_username, [username])
            hash = hashlib.md5()
            if int(self.cursor.fetchone()[0]) < 1:
                hash.update(password.encode())
                self.cursor.execute(self.insert_up, [username, hash.hexdigest()])
                self.conn.commit()
                c.send(b"YE")
            else:
                c.send(b"HU")
        elif flag == "SI":  # sign in
            info = message.split("#")
            username = info[0]
            password = info[1]
            # print(username, password)
            hash = hashlib.md5()
            hash.update(password.encode())
            self.cursor.execute(self.select_up, [username, hash.hexdigest()])
            if int(self.cursor.fetchone()[0]) > 0:
                c.send(b"YE")
            else:
                c.send(b"NO")
        elif flag == "CH":  # check history
            # message = message.split(" ", 1)
            username = message
            # print(username)
            self.cursor.execute(self.select_history, [username])
            result = self.cursor.fetchall()
            # print(result)
            answer = "OK "
            # print(result)
            for record in result:
                answer += record[0]+"#"+str(record[1])+"$"
            answer.rstrip("$")
            # print(answer)
            c.send(answer.encode())
        elif flag == "FW":  # find word
            message = message.split(" ")
            username = message[0]
            word = message[1]
            # print(username, word)
            self.cursor.execute(self.select_word, [word])
            result = self.cursor.fetchone()
            if result:
                ans = "OK " + result[1]
                # print([username, word])
                self.cursor.execute(self.insert_history, [username, word])
                self.conn.commit()
                c.send(ans.encode())
            else:
                c.send(b"NF")
        elif flag == "LO":  # log out
            # self.rlist.remove(c)
            # c.close()
            pass

    def server_forever(self):
        self.log("Server listen at localhost:80")
        while True:
            try:
                rs, ws, xs = select.select(self.rlist, self.wlist, self.xlist)  # 阻塞
                for r in rs:
                    if r is self.tcpserver:
                        c, addr = r.accept()
                        self.log("connect from" + str(addr))
                        self.rlist.append(c)
                    elif r in rs:
                        self.server_for(r)
                    elif r in ws:
                        pass
            except KeyboardInterrupt:
                exit("exit server")
            except Exception as e:
                pass
                # print(e)
                # self.log(e)


def main():
    server = Server()
    server.server_forever()


if __name__ == '__main__':
    main()
