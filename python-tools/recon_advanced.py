import datetime
import socket

IP = "192.168.56.104"

services = {
    20: 'FTP-DATA',
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    111: 'RPC',
    135: 'MSRPC',
    139: 'NetBIOS',
    143: 'IMAP',
    443: 'HTTPS',
    445: 'SMB',
    512: 'rexec',
    513: 'rlogin',
    514: 'rsh',
    1099: 'Java-RMI',
    1524: 'Bindshell',
    2049: 'NFS',
    2121: 'FTP-ProFTPD',
    3306: 'MySQL',
    3389: 'RDP',
    5432: 'PostgreSQL',
    5900: 'VNC',
    6000: 'X11',
    6667: 'IRC',
    8009: 'AJP',
    8080: 'HTTP-ALT',
    8180: 'Tomcat',
    8443: 'HTTPS-ALT',
    9200: 'Elasticsearch',
    27017: 'MongoDB'
}
print(f"Scan started at: {datetime.datetime.now()}")
print(f"\nScanning {IP}...\n")
print(f"{'PORT':<10} {'SERVICE':<15} {'BANNER'}")
print("-" * 60)
 
for port in range(1,1025):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(2)
    result = s.connect_ex((IP,port))
    if result == 0:
        service = services.get(port,"unknowen")
        try:
            banner = s.recv(1024).decode('utf-8').strip()
        except:
            banner = "no banner"
        print(f"{port:<10} {service:<15} {banner}")
    s.close()