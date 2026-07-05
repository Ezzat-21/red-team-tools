import socket

IP = '192.168.56.101'

print(f"Scanning {IP}...\n")

for port in range(1,1025):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((IP,port))

    if result == 0:
        try:
            banner = s.recv(1024).decode('utf-8').strip()
        except:
            banner = 'No banner'
        
        print(f"Port {port} open - {banner}")
    
    s.close()

print("\nDone.")
    