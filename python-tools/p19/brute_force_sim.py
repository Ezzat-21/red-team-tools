import socket
import datetime
IP = "192.168.56.104"
FILE = "/home/kali/red-team-tools/python-tools/p19/wordlist.txt"

def brute_force(filename):
    with open(filename,'r') as f:
        
        for (i,password) in enumerate(f,start=1):
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Attempt {i}: Testing password: {password.strip()}")

def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(2)
    if s.connect_ex((IP,22)) == 0:
        brute_force(FILE)
    else:
        print("Port 22 is CLOSED")
    s.close()

if __name__ == "__main__":
    main()