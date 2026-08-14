import socket
import argparse


parser = argparse.ArgumentParser(description='Port Scanner')

parser.add_argument(
    "-t",
    "--target",
    required=True,
    help="Target IP address"
)
parser.add_argument(
    "-s",
    "--start",
    type=int,
    default=1,
    help="Scan Starting Position"
)
parser.add_argument(
    "-e",
    "--end",
    type=int,
    default=1025,
    help="Scan Ending Position"
)
parser.add_argument(
    "-T",
    "--timeout",
    type=float,
    default=0.1,
    help="Timeout Period"
)
args = parser.parse_args()



print(f"Scanning {args.target} ports {args.start}-{args.end}...")

for port in range(args.start, args.end + 1 ):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(args.timeout)
    result = s.connect_ex((args.target, port))
    if result == 0:
        print(f"port {port} is open")
    s.close()

print("Scan completed.")