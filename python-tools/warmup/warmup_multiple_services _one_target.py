import socket

IP = '192.168.56.104'
results = {}

# FTP check
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.settimeout(2)
if s.connect_ex((IP, 21)) == 0:
    try:
        s.recv(1024)
        s.send(b"USER anonymous\r\n")
        s.recv(1024)
        s.send(b"PASS anonymous\r\n")
        r = s.recv(1024).decode('utf-8').strip()
        results['ftp'] = "ALLOWED" if '230' in r else "DENIED"
    except:
        results['ftp'] = "ERROR"
else:
    results['ftp'] = "CLOSED"
s.close()


# Telnet check
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.settimeout(2)
if s.connect_ex((IP, 23)) == 0:
    try:
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        results['telnet'] = f"OPEN — {banner[:50]}"
    except:
        results['telnet'] = f"OPEN — no banner"
s.close()


# MySQL check
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.settimeout(2)
if s.connect_ex((IP, 3306)) == 0:
    results['mysql'] = 'OPEN'
else:
    results['mysql'] = 'CLOSED'
s.close()

print(f"""
=== Service Summary for {IP} ===
FTP anonymous login: {results['ftp']}
Telnet:              {results['telnet']}
MySQL port:          {results['mysql']}
""")
