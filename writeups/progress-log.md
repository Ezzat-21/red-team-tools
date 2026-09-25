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

## September 2026 — SSRF, CSRF, and Stage 2 Completion

### Completed
- SSRF — 5/7 PortSwigger labs (basic SSRF via unvalidated parameters, internal network
  scanning via SSRF, blacklist/whitelist filter bypasses, open redirect chaining;
  Labs 6-7 documented as watched — blind SSRF via Burp Collaborator OOB detection and
  Shellshock chaining require Burp Pro)
- CSRF — 8/8 PortSwigger labs (no defenses, method-based bypass, missing-parameter
  bypass, non-session-bound tokens, double-submit cookie weakness via CRLF injection,
  Referer validation bypasses via missing header and naive substring matching)
- Stage 2 — Web App Security — fully complete across all 6 vulnerability categories
- port_scanner_argparse.py: added --common flag for scanning well-known ports only

### Currently Working On
- Reviewing all of Stage 2 via active recall (explaining each vulnerability class from
  memory before checking cheatsheet) rather than passive re-reading
- Cold-redoing select PortSwigger labs without notes to test real retention
- Starting Hacker101 CTF as a bridge between academy labs and real-world bug hunting

### Next
- Complete Stage 2 review + Hacker101 practice
- Begin Stage 3 — Exploitation Fundamentals (TCM Practical Ethical Hacking +
  TryHackMe Jr Pentester path) — full recon-to-report methodology, Metasploit,
  privilege escalation, buffer overflows, password cracking
- Consider a low-stakes VDP (Vulnerability Disclosure Program) for real-world practice
  once Stage 3 is underway
