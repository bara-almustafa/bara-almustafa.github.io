---
layout: default
title: "Bypassing SMB Signing with note"
date: 2026-11-24
author: 0xcybersoldier
tags: [active-directory, ad, SMB, bloodyAD, coerce_name , krbrelayx , PetitPotam  ]
---

Hello everyone today we will talk about Bypassing  SMB Signing with note . 
so before what is SMB Singing ? 
SMB signing is the mitigation everyone recommends against the whole relay class of attacks (NTLM or Kerberos)

![SMB Signing Prevention Workflow]({{'assets/img/smb-signing.jfif' | relative_url}})

In a relay, an attacker captures an authentication (NTLM or Kerberos) and forwards it to a service, acting as the victim. Reflection is the case where it is sent back to the machine it came from.

Enforced SMB signing is the usual way to stop relay to SMB, whatever the authentication protocol. Without the session key, the attacker cannot sign the traffic, so a signing-required target refuses the session. Domain Controllers require SMB signing by default.
for more detials : 
[What is SMB Signing based on Microsoft Documentation](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing-overview)



------------

>Microsoft is explicit about what signing buys you:

The signature also confirms the sender’s and receiver’s identities, and prevents relay attacks.

[Microsoft, Overview of SMB signing](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing-overview)
So the wall is clear: with signing enforced, relay to SMB is supposed to be dead. This note is about getting through it anyway.



-----------------
# The SMB signing angle

SMB lets a client re-authenticate an existing session. When it does, the server keeps the original signing key rather than deriving a new one: the specification says “the existing Session.SessionKey will be retained” (['MS-SMB2, section 3.3.5.5.2'](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-smb2/5ecc02fb-0e60-4cba-afeb-f13100a6e65e)), and the server only regenerates the signing key when the request “is not for session reauthentication” (['MS-SMB2, section 3.3.5.5.3, step 7'](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-smb2/5ed93f06-a1d2-4837-8954-fa8b833c2654)). So on re-authentication the original key is kept, and that part is documented.

What the specification describes here is a principal re-authenticating its own session (for example after it expires), not a different identity being swapped onto an existing session’s key. The server simply does not re-check that the re-authenticating identity matches the original one, and that missing check, rather than the key retention itself, is what makes the swap possible.

So the idea is simple: open an SMB session as a low-privilege account you control (so you can sign it), then re-authenticate that same session with the relayed authentication of a privileged account. The session’s identity becomes privileged, but signing keeps using the key you control, so a target that requires signing still accepts it.

On any host that requires SMB signing, Domain Controllers included, a relayed privileged authentication yields a privileged session that is still signed with the low-privilege key. Enforced signing did not stop it.
![smb_signing_key_retention_bypass Workflow]({{'assets/img/smb_signing_key_retention_bypass.png' | relative_url}})

-------------

# What it implies today
 
Enforced SMB signing used to be a reliable stop for relay attacks: even if an attacker captured or coerced an NTLM or Kerberos authentication, a signing-required server would refuse to accept it over a relayed connection. With that enforcement defeated, the barrier is gone — a relayed authentication can reach a signing-required server again, including in the reflective case where the victim and the target are the same host. This matters most for Domain Controllers, since they're the highest-value target for this kind of relay. But defeating signing isn't itself a compromise. It only removes a blocker; the attacker still needs to capture and relay an authentication that actually carries privileges on the target, through something like LLMNR or mDNS poisoning or coercion. And the fork can still be closed: a server that checks the same identity re-authenticates — the binding check the specification already defines — stops this regardless of whether signing enforcement holds. So the right read isn't "signing enforcement is broken," it's "signing enforcement is necessary but no longer sufficient on its own, unless it's paired with that identity check."

![smb signing relay flow Workflow]({{'assets/img/smb_signing_relay_flow.png' | relative_url}})


--------
# A note on patching
This looks like it is being fixed. A same-user check on re-authentication shows up on Windows 11 24H2 / Server 2025 around September 2026, and similar changes seem to have reached the other supported Windows versions, servers and workstations alike, in the weeks after. I have not traced every build, and one or two end-of-life versions may never receive it. So it is probably better read as a patch window than a permanent gap: a host that is current on updates is likely no longer affected, while hosts behind that wave still are. I could not find a CVE for this specific change, in Microsoft’s update guide, the KB notes, or public trackers; it reads as silent hardening rather than a tracked fix. Corrections welcome.

> Update, 2026-10-21. This blog post is released.

> Update, 2026-10-23. SpecterOps published Raj Patel’s “LDAP Switcheroo” the same re-authentication idea against LDAP signing on domain controllers. It covers both SMB and LDAP.

> Update, 2026-10-30. MSRC confirms this issue was reported by @mad31k as part of a RCE chain and fixed in CVE-2026-69676.

----------------
# LAB 
Two small things, for authorized testing only:

1. reauthx, a small fork of krbrelayx that adds one opt-in flag, --reauth-bypass. With the flag off, it behaves exactly like krbrelayx. It also ships patchcheck.py (recon) and coerce_name.py (coercion-name helper).
2. reauth_swap, a NetExec module that checks whether a host still allows the cross-user re-authentication swap.



What follows is an example. Two low-privilege domain accounts the attacker controls: user1 does the real work (recon, the DNS record on the DC, the coercion, and the relay’s base session); user2 is only the second identity the step 1 viability check needs to test the cross-user swap. The target is FS01 at 10.0.0.10; the DC that holds the AD-integrated DNS zone is at 10.0.0.5; the relay listens on 10.0.0.50.

| Role     | OS                                 | IP         | Notes                                              |
|----------|------------------------------------|------------|-----------------------------------------------------|
| DC01     | Windows Server 2022                | 10.0.0.5   | AD DS + AD-integrated DNS                           |
| FS01     | Windows Server 2022 (member)       | 10.0.0.10  | Domain-joined, SMB signing required                 |
| Attacker | Kali / Debian Linux                | 10.0.0.1  | impacket, NetExec, PetitPotam, bloodyAD             |

1. Recon - the one precondition to confirm first is that the target enforces SMB signing (signing:True in both outputs below). That is the wall this technique walks through; if signing were not enforced, a plain relay would already work and none of this would be needed. The NetExec module checks viability directly, and patchcheck.py then places the host in the patch window - here the first patch (CVE-2025-33073) is already in, so the CMTI name is dead and the coercion goes through a Unicode confusable name instead.

![Using nxc with reauth_swap]({{'assets/img/smb-lab1.png' | relative_url}})

OR 

![ patchcheck ]({{'assets/img/smb-lab2.png' | relative_url}})


2. Point a DNS record at the relay - build the coercion name for the target, add an AD-integrated DNS record for it on the DC, and confirm it resolves to the relay. The Unicode name carries a confusable letter (and the dots are confusables too), so it is built in a sub-shell and never typed by hand; I do not print it literally below.

![ Point a DNS record at the relay ]({{'assets/img/smb-lab3.png' | relative_url}})
3. Start the relay with the signing bypass - the base session is user1, whose signing key you control. Leave it running.

![Setting a smb server in kali]({{'assets/img/smb-lab6.png' | relative_url}})

4. Coerce the target - it authenticates to the relay, which reflects it back onto FS01 while keeping user1’s signing key.

![Coerce the target]({{'assets/img/smb-lab8.png' | relative_url}})

The relay window then shows the swap and a SYSTEM-level dump:

![ output ]({{'assets/img/smb-lab7.png' | relative_url}})
5. Cleanup - remove the DNS record and stop the relay.
![ cleaning up ]({{'assets/img/smb-lab9.png' | relative_url}})

Repository Used : github.com/aas-n/reauthx.



-----------------------------------
# Credits and references
I am not the person who did the hard work here. I connected dots that others drew, and I am small next to the researchers who actually move this field. Thanks in particular to:

1. mad31k for originally reporting this bug to MSRC.
2. Raj Patel (SpecterOps), for the LDAP Switcheroo, the same idea carried to LDAP signing.
3. NeffIsBack and ThatTotallyRealMyth, for the spec reading that sharpened how key retention and the missing identity check should be told apart.
4. Dirk-jan Mollema, for krbrelayx, which this forks.
4. Synacktiv, for the modern authentication reflection analysis.
5. SySS, Semperis, for the research this note leans on.
6. and blackfield for  original post 
