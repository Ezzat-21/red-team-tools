import socket
import argparse
import datetime

TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

parser = argparse.ArgumentParser(description='Port Scanner')
parser.add_argument("-t", "--target", required=True)
parser.add_argument("-s", "--start", type=int, default=1)
parser.add_argument("-e", "--end", type=int, default=1025)
parser.add_argument("-T", "--timeout", type=float, default=0.1)
parser.add_argument("-o", "--output",default=None)
args = parser.parse_args()

services = {
    21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
    53: 'DNS', 80: 'HTTP', 111: 'RPC', 139: 'NetBIOS',
    443: 'HTTPS', 445: 'SMB', 512: 'rexec', 513: 'rlogin',
    514: 'rsh', 1099: 'Java-RMI', 1524: 'Bindshell',
    2049: 'NFS', 3306: 'MySQL', 5432: 'PostgreSQL',
    5900: 'VNC', 6667: 'IRC', 8180: 'Tomcat'
}

try:
    socket.inet_aton(args.target)
except socket.error:
    print("Please enter a valid IP Address")
    exit(1)

if args.output is None:
    args.output = f"/home/kali/red-team-tools/python-tools/scan_{args.target}_{TIMESTAMP}.txt"

print(f"Scanning {args.target} ports {args.start}-{args.end}...")

with open(args.output, "w") as f:
    f.write(f"Scan of {args.target} — {TIMESTAMP}\n\n")
    for port in range(args.start, args.end + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(args.timeout)
        result = s.connect_ex((args.target, port))
        if result == 0:
            service = services.get(port, 'unknown')
            line = f"Port {port} ({service}) — OPEN"
            print(line)
            f.write(line + "\n")
        s.close()
    f.write("\nScan completed.\n")

print(f"Results saved to {args.output}")