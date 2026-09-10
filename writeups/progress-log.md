# Progress Log
Ahmed Ezzat — Red Team Roadmap

## July 2026 — Week 2

### Completed
- Stage 1a Linux Mastery — done
- Stage 1b Windows Fundamentals — done
- Built 4 Python tools from scratch
- Full OPSEC routine — disable history, clear logs, surgical clean
- Found private keys on Metasploitable
- Completed full recon on Metasploitable — all services documented
- Started Stage 2 — watched first SQLi video

### Currently Working On
- Stage 2 Web App Security
- Rana Khalil SQLi series + PortSwigger labs

### Next
- First PortSwigger SQLi lab
- Continue SQLi series

---

## July 2026 — Week 3

### Completed
- SQL Injection — fully complete
- 14 labs solved on PortSwigger (Labs 15-16 watched, require Burp Pro)
- Labs 17-18 watched
- Covered: WHERE clause, login bypass, UNION attacks, Oracle/MySQL/PostgreSQL/MSSQL syntax
- Blind SQLi: boolean-based, conditional errors, time-based
- Full SQLi methodology documented in cheatsheet
- Built 6 additional Python scripts from scratch
- Full OPSEC routine now automatic — no notes needed
- Direct MySQL access confirmed — root with no password
- DVWA hardcoded credentials found in config file
- Shadow file extracted and transferred via netcat
- SMTP username enumeration via VRFY

## August 2026 — Week 4-5

### Completed
- XSS Labs 1-11 with full structured methodology
- Paused labs for 3 days to study browser parsing fundamentals
- Studied HTML parser states, JS contexts, URL contexts
- Developed structured analysis methodology for every lab
- Manual FTP enumeration with netcat
- SMTP username enumeration — confirmed root, msfadmin, user, bin, daemon, sys
- VNC access with default credentials — root GUI desktop
- Bindshell instant root via port 1524
- Built vulnerability report script with risk ratings

## August 2026 — Week 5-6

### Completed
- XSS Labs 14-27 with full structured methodology
- Labs 22-23-25-26: watched only — Burp Pro / AngularJS expert level
- Lab 24: watched with tutorial — CSRF concept introduced
- Lab 27: solved — SVG animate attribute modification technique
- World-writable directories found — /var/www/dav critical for Stage 3
- nmap SUID privilege escalation documented
- .rhosts + + found — passwordless rlogin as root confirmed
- tcpdump SSH capture — compared encrypted SSH vs plaintext FTP
- argparse port scanner built with service lookup and file output
- Warm-up tasks completed through L22, N22, P22

## August 2026 — Week 7-8

## September 2026 — Access Control / IDOR Module Complete

### Completed
- Access Control / IDOR — 13/13 PortSwigger labs
- Theory: vertical vs horizontal vs context-dependent access control, root causes
  (unprotected functionality, identifier-based trust, platform misconfiguration,
  multi-step process flaws)
- Unprotected admin panels: obscure paths (guessed and discovered via page source)
- Client-controlled authorization values: forged cookies, injected roleid fields
- IDOR family: predictable ID parameters, leaked GUIDs, data leakage in redirect
  bodies, password disclosure chained with IDOR, predictable static filenames
- Layer/method/step-based bypasses: X-Original-URL header trust mismatch,
  method-based access control (GET vs POST), multi-step process missing a
  check on step 2, Referer header trusted as identity proof
- Full module pattern summary: every bug reduces to "is there a check?" vs
  "is the check trustworthy?"
- Testing methodology internalized: comparison across user identity/privilege,
  not across input values (distinct from SQLi/XSS approach)

### Currently Working On
- Repo progress sync (this update)

### Next
- Start SSRF vulnerabilities on PortSwigger
- Then: CSRF
- Move to Stage 3 (Exploitation Fundamentals) after completing Stage 2
