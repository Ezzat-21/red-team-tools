AHMED EZZAT — RED TEAM CHEATSHEET
Last Updated: July 2026
======================================================

LINUX
======================================================

Find SUID binaries:
find / -perm -4000 2>/dev/null

Find writable files:
find / -writable -type f 2>/dev/null

Find files containing password:
grep -r "password" /etc/ 2>/dev/null

List users with real shells:
cat /etc/passwd | grep -v "nologin\|false"

Live log monitoring:
tail -f /var/log/auth.log

Failed SSH attempts:
grep "Failed password" /var/log/auth.log

Successful SSH logins:
grep "Accepted" /var/log/auth.log

Check cron jobs:
crontab -l && cat /etc/crontab

Disable history:
unset HISTFILE && export HISTSIZE=0

Clear history file:
cat /dev/null > ~/.bash_history

Surgical log clean:
sed -i '/YOUR_IP/d' /var/log/auth.log

======================================================
NETWORKING
======================================================

Standard recon scan:
nmap -sV -sC TARGET_IP

Full port scan:
nmap -p- TARGET_IP

Ping sweep:
nmap -sn 192.168.56.0/24

Stealth scan:
nmap -sS TARGET_IP

Banner grab with netcat:
nc TARGET_IP PORT

Send raw HTTP GET:
nc TARGET_IP 80 then type: GET / HTTP/1.0

Capture traffic:
wireshark

Filter by IP in Wireshark:
ip.addr == TARGET_IP

Filter FTP in Wireshark:
ip.addr == TARGET_IP && ftp

File transfer — Python HTTP server:
python3 -m http.server 8080

File transfer — netcat send:
nc TARGET_IP 4444 < file.txt

File transfer — netcat receive:
nc -lvp 4444 > file.txt

Check routing table:
route -n

Check ARP table:
arp -a

======================================================
SSH
======================================================

Basic connect:
ssh user@IP

Connect with key:
ssh user@IP -i keyfile

Connect on custom port:
ssh user@IP -p 2222

Generate key pair:
ssh-keygen -t rsa -b 4096

Copy public key to target:
ssh-copy-id user@IP

Port forward:
ssh -L localport:target:targetport user@IP

Brute force:
hydra -l user -P wordlist ssh://IP

Find private keys:
find / -name "id_rsa" 2>/dev/null

======================================================
PROXYCHAINS & TOR
======================================================

Start TOR:
sudo service tor start

Verify IP changed:
proxychains curl ifconfig.me

Run tool through TOR:
proxychains TOOL OPTIONS

Config file:
/etc/proxychains4.conf

======================================================
PYTHON TOOLS
======================================================

Port checker:
python3 ~/tools/port_check.py

Port scanner:
python3 ~/tools/port_scanner.py

Banner grabber:
python3 ~/tools/banner_grab.py

Full recon tool:
python3 ~/tools/recon.py

======================================================
TARGET LAB
======================================================

Metasploitable IP: 192.168.56.101
Kali IP:           192.168.56.102
FTP creds:         msfadmin / msfadmin
SSH creds:         msfadmin / msfadmin
Telnet creds:      msfadmin / msfadmin

Known vulnerabilities (exploit in Stage 3):
- vsftpd 2.3.4 — backdoor exploit
- Samba 3.0.20 — usermap_script
- OpenSSH 4.7p1 — outdated

======================================================
SERVICES FOUND ON METASPLOITABLE
======================================================

Port 21   — FTP      — vsftpd 2.3.4
Port 22   — SSH      — OpenSSH 4.7p1
Port 23   — Telnet
Port 25   — SMTP
Port 53   — DNS
Port 80   — HTTP
Port 111  — RPC
Port 139  — SMB      — Samba 3.0.20
Port 445  — SMB      — Samba 3.0.20
Port 512  — rexec
Port 513  — rlogin
Port 514  — rsh
