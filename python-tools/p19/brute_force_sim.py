import socket
import datetime

with open("/home/kali/red-team-tools/python-tools/p19/wordlist.txt","r") as f:
    
    for (i,password) in enumerate(f,start=1):
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  Attempt {i}: Testing password: {password.strip()}")