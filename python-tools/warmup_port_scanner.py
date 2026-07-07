import socket

IP = '192.168.56.101'

for port in range(20,101):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(1)

    result = s.connect_ex((IP,port))
    if result == 0:
        try:
            banner = s.recv(2048).decode('utf-8').strip()
        except:
            banner = 'no banner'
        print(f'port {port} open - {banner}')
    
    s.close()



