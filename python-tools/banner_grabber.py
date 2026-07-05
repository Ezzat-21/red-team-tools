import socket

IP = '192.168.56.101'
PORT = 80

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.settimeout(1)
s.connect_ex((IP,PORT))
try:
    data = s.recv(1024).decode('utf-8')
    print(f"Banner: {data}")
except:
    print("No banner received")
s.close()
