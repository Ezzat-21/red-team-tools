import socket

IP = '192.168.56.104'

print(f"Scanning {IP}...\n")

for port in range(1,1025):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        result = s.connect_ex((IP, port))
        if result == 0:
            try:
                banner = s.recv(1024).decode('utf-8').strip()
            except (socket.timeout, UnicodeDecodeError):
                banner = 'No banner'
            print(f"Port {port} open - {banner}")
    except OSError as e:
        print(f"Port {port} error - {e}")
    finally:
        s.close()

print("\nDone.")
    