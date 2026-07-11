# Metasploitable 2 — Full Recon

Target: 192.168.56.104
Date: July 2026

## Tools Used
- nmap -sV -sC
- netcat
- custom Python recon_advanced.py
- Wireshark

## Open Ports Found

Port 21   FTP    vsftpd 2.3.4     CRITICAL — backdoor vulnerability
Port 22   SSH    OpenSSH 4.7p1    HIGH — outdated version
Port 23   Telnet plaintext        HIGH — credentials sent in cleartext
Port 25   SMTP   Postfix          MEDIUM — VRFY enabled
Port 53   DNS    BIND 9.4.2       MEDIUM — version exposed
Port 80   HTTP   Apache 2.2.8     HIGH — old version, web apps exposed
Port 139  SMB    Samba 3.0.20     CRITICAL — usermap_script exploit
Port 445  SMB    Samba 3.0.20     CRITICAL — usermap_script exploit
Port 1524 Shell  Bindshell        CRITICAL — root shell already open
Port 6667 IRC    UnrealIRCd       CRITICAL — backdoor vulnerability

## Key Findings from -sC Scripts
- Anonymous FTP login allowed on port 21
- SMTP VRFY enabled — username enumeration possible
- SSLv2 supported on port 25 — broken encryption
- NFS shares exposed via port 111
- SMB guest access allowed, message signing disabled
- Machine name: metasploitable, domain: localdomain

## Key Findings from Raw HTTP GET
- Apache 2.2.8 with PHP 5.2.4 — both outdated
- WebDAV enabled — file upload may be possible
- Web apps exposed: DVWA, phpMyAdmin, Mutillidae, TWiki

## Private Keys Found
- /home/msfadmin/.ssh/id_rsa — SSH private key
- /etc/mysql/server-key.pem  — MySQL SSL key

## SUID Binaries — Exploit in Stage 3
- /usr/bin/nmap
- /usr/bin/at
- /usr/lib/pt_chown

## Vulnerabilities to Exploit in Stage 3
1. vsftpd 2.3.4 backdoor — port 21
2. Samba usermap_script  — port 139
3. UnrealIRCd backdoor   — port 6667
4. Bindshell             — port 1524 — netcat = instant root
