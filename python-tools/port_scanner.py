import socket
import sys

IP = '192.168.56.104'
start = int(sys.argv[1])
end = int(sys.argv[2])

print(f"Scanning {IP} ports {start}-{end}...")

for port in range(start, end):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    result = s.connect_ex((IP, port))
    if result == 0:
        print(f"port {port} is open")
    s.close()

print("Scan completed.")