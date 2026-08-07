# Red Team Tools — Ahmed Ezzat

Security tools, notes, writeups, and XSS/SQLi lab reports built during my Red Team learning path.

## Progress

- Stage 1a — Linux Mastery — DONE
- Stage 1b — Windows Fundamentals — DONE
- Stage 2 — Web App Security — IN PROGRESS
  - SQL Injection — 14 labs complete
  - XSS — 11 labs complete (structured methodology)
- Stage 3 — Exploitation Fundamentals — UPCOMING
- Stage 4 — Active Directory — UPCOMING
- Stage 5 — OSCP Prep — UPCOMING
- Stage 6 — Red Team Ops — UPCOMING

## Python Tools

### port_scanner.py
Scans ports 1-1024 on a target IP and prints open ports.

### banner_grabber.py
Connects to a target port and grabs the service banner.

### recon.py
Combines port scanning and banner grabbing in one tool.

### recon_advanced.py
Full recon tool with service dictionary, table output and timestamp.

### single_port_checker.py
Checks if a single port is open or closed.

### scanner.py
Port scanner with command line argument support.

### multi-service-checker.py
Checks FTP, Telnet, MySQL, VNC, and bindshell in one run.

### vulnerability-report.py
Generates a formatted vulnerability report with risk ratings and timestamp.

### check_anonymous_ftp.py
Tests if a target allows anonymous FTP login.

## Notes

- cheatsheet.md — Linux, Windows, networking, SSH, SQLi, XSS reference

## Writeups

- progress-log.md — weekly progress tracker
- metasploitable-recon.md — full recon writeup for Metasploitable 2
- xss-labs/ — structured XSS lab reports (Labs 1-11)
- sqli-labs/ — SQL injection lab notes

## Lab Environment

- Kali Linux 192.168.56.102 — attacker machine
- Metasploitable 2 192.168.56.104 — target machine
- Host-Only isolated network
