# Metasploitable 2 — Service Vulnerability Report
Generated: 2026-08-08_09-05-38

## CRITICAL Findings

| PORT       | SERVICE         | Version              | Notes                     |
| ---------- | --------------- | -------------------- | ------------------------- |
| 21         | FTP             | vsftpd 2.3.4         | backdoor exploit          |
| 139        | SMB             | Samba 3.0.20         | usermap_script exploit    |
| 1524       | Bindshell       | unknown              | instant root shell        |
| 6667       | IRC             | UnrealIRCd           | backdoor exploit          |

## HIGH Findings

| PORT       | SERVICE         | Version              | Notes                     |
| ---------- | --------------- | -------------------- | ------------------------- |
| 22         | SSH             | OpenSSH 4.7p1        | outdated version          |
| 23         | Telnet          | Linux telnetd        | plaintext credentials     |
| 80         | HTTP            | Apache 2.2.8         | old version, web apps     |
| 3306       | MySQL           | 5.0.51a              | no root password          |
| 5900       | VNC             | protocol 3.3         | default credentials       |
