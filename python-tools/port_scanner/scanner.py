import socket
import datetime
import sys

IP = sys.argv[1]
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"/home/kali/red-team-tools/python-tools/port_scanner/scan_{timestamp}.txt"

with open(filename, 'w') as f:
    f.write(f"Scan started: {timestamp}\n")
    f.write(f"Target: {IP}\n")
for port in range(1,1025):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((IP,port))
    if result == 0:
        try:
            banner = s.recv(1024).decode('utf-8').strip()
        except:
            banner = 'no banner'
        print(f"Port {port} open - {banner}")
        with open(filename , 'a') as f:
            f.write(f"Port {port} open - {banner}\n")
    s.close()
    

        