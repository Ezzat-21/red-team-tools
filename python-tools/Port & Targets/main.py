import socket


PORT = 80

with open('Port & Targets/targets.txt', 'r') as f:
    for line in f:
        ip = line.strip()
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip,PORT))
        if result == 0:
            print(f"{ip} — port {PORT} is open")
        else: 
            print(f"{ip} — port {PORT} is closed")
        s.close()