# Red Team Tools — Ahmed Ezzat

Security tools, notes, writeups and lab reports built during my Red Team learning path.

## Progress

- Stage 1a — Linux Mastery — DONE
- Stage 1b — Windows Fundamentals — DONE
- Stage 2 — Web App Security — IN PROGRESS
  - SQL Injection — 14/14 PortSwigger labs complete
  - XSS — 27/30 labs complete with structured methodology (28, 30 remaining; 22-23-25-26-29 watched only — Burp Pro or expert level)
  - Authentication — 14/14 PortSwigger labs complete (Lab 8 and Lab 14 documented as watched — Turbo Intruder / Burp macros required for full hands-on completion)
  - Access Control / IDOR — STARTING NEXT
  - After Access Control: SSRF → CSRF
- Stage 3 — Exploitation Fundamentals — UPCOMING
- Stage 4 — Active Directory — UPCOMING
- Stage 5 — OSCP Prep — UPCOMING
- Stage 6 — Red Team Ops — UPCOMING

## Python Tools

### banner_grabber.py
Connects to a port and grabs the service banner.

### recon.py
Combines port scanning and banner grabbing, with exception handling on `connect_ex()` and `recv()`.

### recon_advanced.py
Full recon tool with service dictionary, table output and timestamp.

### single_port_checker.py
Checks if a single port is open or closed.

### scanner.py
Port scanner with command line argument support via `sys.argv`.

### multi-service-checker.py
Checks FTP anonymous login, Telnet, MySQL, and SMTP (with VRFY username enumeration) in one run.

### formatted_vulnerability_script.py
Generates a formatted Markdown vulnerability report grouped by risk rating, written to `writeups/metasploitable-services.md`.

### check_anonymous_ftp.py
Tests if target allows anonymous FTP login with full handshake, including upload capability check.

### port_scanner/scanner.py
Port scanner with timestamped file output support.

### port_scanner_argparse.py
Advanced argparse-based port scanner — configurable target, port range, timeout, output file, and verbose mode (shows closed ports too). Validates target IP format before scanning.

### port_and_targets/main.py
Scans a single port across multiple targets read from a file.

### p19/brute_force_sim.py
Simulates brute-force login attempts against a target with timestamped logging.

## Notes

- `cheatsheet.md` — comprehensive reference covering Linux, Windows, networking, SSH,
  SQLi (14 labs), XSS (27 labs), Authentication (14 labs), OPSEC routine,
  credentials found, Python tools, Metasploitable services

## Writeups

- `progress-log.md` — weekly progress tracker
- `metasploitable-recon.md` — full recon writeup for Metasploitable 2
- `metasploitable-services.md` — service vulnerability report with risk ratings

## Lab Environment

- Kali Linux 192.168.56.102 — attacker machine
- Metasploitable 2 192.168.56.104 — target machine
- Host-Only isolated network in VirtualBox
