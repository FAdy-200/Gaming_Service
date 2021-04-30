import socket
import time
addr = '127.0.0.1'
port = int(input())
addPair = (addr, port)
sadd = ("127.0.0.1", 56969)
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ClientSocket.bind(addPair)
ClientSocket.connect(sadd)
# ClientSocket.send(b"fady:alomar\nasd")
print("c")
# while True:
ClientSocket.send(input().encode())
time.sleep(0.075)
data = ClientSocket.recv(1024)
print(data)
if data == b"close":
    print("asdaoshpdioasidj")
    ClientSocket.close()
    exit()
