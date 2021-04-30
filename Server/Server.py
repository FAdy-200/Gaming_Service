import socket
import selectors


class server:
    def __init__(self):
        self.__hostName = socket.gethostname()
        self.__ipAddress = socket.gethostbyname(self.__hostName)
        self.__port = 56969
        self.__addr = (self.__ipAddress, self.__port)
        self.__Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__Socket.bind(self.__addr)
        self.__Socket.setblocking(False)
        self.__Socket.listen()
        self.__sel = selectors.DefaultSelector()
        self.__sel.register(self.__Socket, selectors.EVENT_READ, data=None)
        self.__users = dict()
        print(self.__addr)

    def __first_Time_Connection_Handler(self, sock):
        conn, addr = sock.accept()
        print('accepted connection from', addr)
        conn.setblocking(False)
        data = [addr]
        self.__sel.register(conn, selectors.EVENT_READ, data=data)

    def __login(self, sock, msg):
        loginData = msg.split(b":")
        userName = loginData[0]
        password = loginData[1]
        toSend = b"wrong user name or password"
        if self.__users.get(userName):
            if self.__users[userName] == password:
                toSend = b"you are logged in"

        sock.send(toSend)

    def __signup(self, sock, msg):
        signupData = msg.split(b":")
        userName = signupData[0]
        password = signupData[1]
        if self.__users.get(userName):
            sock.send(b"user name already exists")
        else:
            self.__users[userName] = password
            sock.send(b"successfully signed in")

    def __normal_Connection_handler(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            msg = sock.recv(1024)
            if msg:
                print(f"msg received from{data[0]}")
                print(msg)
                if msg[:3] == b"L09":
                    self.__login(sock, msg[3:])
                elif msg[:3] == b"S19":
                    self.__signup(sock, msg[3:])
                else:
                    sock.send(b"Unknown Command")
                data.append(msg)

    def main(self):
        while True:
            connections = self.__sel.select(False)
            for key, mask in connections:
                if key.data is None:
                    self.__first_Time_Connection_Handler(key.fileobj)
                else:
                    self.__normal_Connection_handler(key, mask)


myServer = server()
myServer.main()
