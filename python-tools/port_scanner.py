import socket

IP = '192.168.56.101'


print("Scanning target...")

for port in range(1,1025):

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(1)

    result = s.connect_ex((IP,port))

    if result == 0:
        print(f"port {port} is open")
    s.close()   

print("Scan completed.")
