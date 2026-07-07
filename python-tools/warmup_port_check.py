import socket

IP = '192.168.56.101'
PORT = 9999

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.settimeout(1)

result = s.connect_ex((IP,PORT))

if result == 0:
    print(f"port {PORT} is open ")
else:
    print(f"port {PORT} is closed ")

s.close()
    
