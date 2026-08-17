# Red Team Tools — Ahmed Ezzat

Security tools, notes, writeups and lab reports built during my Red Team learning path.

## Progress

- Stage 1a — Linux Mastery — DONE
- Stage 1b — Windows Fundamentals — DONE
- Stage 2 — Web App Security — IN PROGRESS
  - SQL Injection — 14 PortSwigger labs complete
  - XSS — 27 of 30 labs complete with structured methodology
  - Labs 22-23-25-26-29 watched only — require Burp Pro or expert knowledge
  - Labs 28 and 30 remaining
- Stage 3 — Exploitation Fundamentals — UPCOMING
- Stage 4 — Active Directory — UPCOMING
- Stage 5 — OSCP Prep — UPCOMING
- Stage 6 — Red Team Ops — UPCOMING

## Python Tools

### banner_grabber.py
Connects to a port and grabs the service banner.

### recon.py
Combines port scanning and banner grabbing.

### recon_advanced.py
Full recon tool with service dictionary, table output and timestamp.

### single_port_checker.py
Checks if a single port is open or closed.

### scanner.py
Port scanner with command line argument support via sys.argv.

### multi-service-checker.py
Checks FTP anonymous login, Telnet, MySQL, VNC, bindshell in one run.

### vulnerability_report.py
Generates formatted vulnerability report with risk ratings and timestamp.

### check_anonymous_ftp.py
Tests if target allows anonymous FTP login with full handshake.

### port_scanner/scanner.py
port scanner 

### port_scanner_argparse.py
Advanced argparse port scanner with service lookup, timeout control and file output.

### port_and_targets/main.py
Scans port 80 across multiple targets read from a file.

### service_report.py
Generates markdown vulnerability report from service dictionary grouped by risk.

### p19/wordlist_logger.py
Simulates brute force logging with timestamp and attempt counter.

## Notes

- cheatsheet.md — comprehensive reference covering Linux, Windows,
  networking, SSH, SQLi labs 1-14, XSS labs 1-27, OPSEC routine,
  credentials found, Python tools, Metasploitable services

## Writeups

- progress-log.md — weekly progress tracker
- metasploitable-recon.md — full recon writeup for Metasploitable 2
- metasploitable-services.md — service vulnerability report with risk ratings

## Lab Environment

- Kali Linux 192.168.56.102 — attacker machine
- Metasploitable 2 192.168.56.104 — target machine
- Host-Only isolated network in VirtualBox
