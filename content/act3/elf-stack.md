+++
title = 'Elf Stack'
date = 2024-12-14T14:54:09+01:00
draft = true
+++

## Objective

> Help the ElfSOC analysts track down a malicious attack against the North Pole domain.

You are offered to either download the logs and do the excersices on your own, or download the ELK stack (logs included): 

* https://hhc24-elfstack.holidayhackchallenge.com/download_file/log_chunk_2.log.zip
* https://hhc24-elfstack.holidayhackchallenge.com/download_file/elf-stack-siem-with-logs.zip
* https://hhc24-elfstack.holidayhackchallenge.com/download_file/log_chunk_1.log.zip

## Easy mode

> Question 1: How many unique values are there for the event_source field in all logs?

Answer: 5

![Answer silver 1](/images/act3/act3-elfstack-s1.png)

> Question 2: Which event_source has the fewest number of events related to it?

Answer: AuthLog

![Answer silver 2](/images/act3/act3-elfstack-s1.png)


> Question 3: Using the event_source from the previous question as a filter, what is the field name that contains the name of the system the log event originated from?

Answer: event.hostname

![Answer silver 3](/images/act3/act3-elfstack-s3.png)

> Question 4: Which event_source has the second highest number of events related to it?

Answer: NetflowPmacct

![Answer silver 4](/images/act3/act3-elfstack-s1.png)

> Question 5: Using the event_source from the previous question as a filter, what is the name of the field that defines the destination port of the Netflow logs?

Answer: event.port_dst

![Answer silver 5](/images/act3/act3-elfstack-s5.png)

> Question 6: Which event_source is related to email traffic?

Answer: SnowGlowMailPxy

![Answer silver 6](/images/act3/act3-elfstack-s1.png)

> Question 7: Looking at the event source from the last question, what is the name of the field that contains the actual email text?

Answer: event.Body

![Answer silver 7](/images/act3/act3-elfstack-s7.png)

> Question 8: Using the 'GreenCoat' event_source, what is the only value in the hostname field?

Answer: SecureElfGwy

![Answer silver 8](/images/act3/act3-elfstack-s8.png)

> Question 9: Using the 'GreenCoat' event_source, what is the name of the field that contains the site visited by a client in the network?

Answer: event.url

![Answer silver 9](/images/act3/act3-elfstack-s9.png)

> Question 10: Using the 'GreenCoat' event_source, which unique URL and port (URL:port) did clients in the TinselStream network visit most?

Answer: pagead2.googlesyndication.com:443

![Answer silver 10](/images/act3/act3-elfstack-s10.png)

> Question 11: Using the 'WindowsEvent' event_source, how many unique Channels is the SIEM receiving Windows event logs from?

Answer: 5

![Answer silver 11](/images/act3/act3-elfstack-s11.png)

> Question 12: What is the name of the event.Channel (or Channel) with the second highest number of events?

Answer: Microsoft-Windows-Sysmon/Operational

![Answer silver 12](/images/act3/act3-elfstack-s11.png)

> Question 13: Our environment is using Sysmon to track many different events on Windows systems. What is the Sysmon Event ID related to loading of a driver?

Answer: 6

According to this list Sysmon Event ID List:

| **Event ID** | **Name**                | **Description**                                                                                      |
|--------------|-------------------------|------------------------------------------------------------------------------------------------------|
| **1**        | ProcessCreate          | Logs when a process is created, including command line arguments and parent process information.    |
| **2**        | FileCreateTime         | Logs changes to file creation time (can be used to detect timestomping).                            |
| **3**        | NetworkConnect         | Logs outbound network connections initiated by a process.                                           |
| **4**        | SysmonConfigChange     | Logs when the Sysmon configuration is changed.                                                      |
| **5**        | ProcessTerminate       | Logs when a process is terminated.                                                                  |
| **6**        | DriverLoad             | Logs when a driver is loaded, including details about its signing status.                           |
| **7**        | ImageLoad              | Logs when an image (DLL or executable) is loaded into a process.                                    |
| **8**        | CreateRemoteThread     | Logs when a thread is created in another process (often used for code injection).                   |
| **9**        | RawAccessRead          | Logs when raw disk access is performed, typically for malicious activity like MBR access.           |
| **10**       | ProcessAccess          | Logs when a process accesses another process (e.g., via OpenProcess API).                        |
| **11**       | FileCreate             | Logs when a file is created or overwritten.                                                         |
| **12**       | RegistryEvent (SetValue)| Logs when a registry value is set or modified.                                                      |
| **13**       | RegistryEvent (Key/Value Create/Delete) | Logs when a registry key or value is created or deleted.                               |
| **14**       | RegistryEvent (Key/Value Rename) | Logs when a registry key or value is renamed.                                           |
| **15**       | FileCreateStreamHash   | Logs creation of alternate data streams (ADS) and provides a hash of the stream contents.           |
| **16**       | ServiceConfigurationChange | Logs changes to service configurations.                                                         |
| **17**       | PipeEvent (Pipe Created) | Logs when a named pipe is created.                                                               |
| **18**       | PipeEvent (Pipe Connected) | Logs when a named pipe is connected.                                                            |
| **19**       | WmiEvent (Filter)      | Logs WMI filter activity, useful for detecting WMI-based attacks.                                   |
| **20**       | WmiEvent (Consumer)    | Logs WMI consumer activity.                                                                        |
| **21**       | WmiEvent (FilterToConsumer Binding) | Logs the binding of a WMI filter to a consumer.                                            |
| **22**       | DNSEvent               | Logs DNS query activity.                                                                           |
| **23**       | FileDelete             | Logs file deletions (if enabled).                                                                  |
| **24**       | ClipboardChange        | Logs clipboard activity (disabled by default; must be enabled in configuration).                   |
| **25**       | ProcessTampering       | Logs process image tampering, such as code injection or manipulation.                              |
| **26**       | FileDeleteDetected     | Logs when file deletion is detected, providing additional context (used with FileDelete).           |

> Question 14: What is the Windows event ID that is recorded when a new service is installed on a system?

Answer: 4697

> Question 15: Using the WindowsEvent event_source as your initial filter, how many user accounts were created?

Answer: 0

Looked for Windows event code 4720, but couldn't find any. So I figured out there were none user created

![Answer silver 15](/images/act3/act3-elfstack-s15.png)


## Hard mode 

> Question 1: What is the event.EventID number for Sysmon event logs relating to process creation?

Answer: 1

> Question 2: How many unique values are there for the 'event_source' field in all of the logs?

Answer: 5 

> Question 3: What is the event_source name that contains the email logs?

Answer: SnowGlowMailPxy

> Question 4: The North Pole network was compromised recently through a sophisticated phishing attack sent to one of our elves. The attacker found a way to bypass the middleware that prevented phishing emails from getting to North Pole elves. As a result, one of the Received IPs will likely be different from what most email logs contain. Find the email log in question and submit the value in the event 'From:' field for this email log event.

Answer: kriskring1e@northpole.local

![Answer gold 4](/images/act3/act3-elfstack-g4.png)

> Question 5: Our ElfSOC analysts need your help identifying the hostname of the domain computer that established a connection to the attacker after receiving the phishing email from the previous question. You can take a look at our GreenCoat proxy logs as an event source. Since it is a domain computer, we only need the hostname, not the fully qualified domain name (FQDN) of the system.

Answer: SleighRider

Finding information by using Lens:

![Answer gold 5a](/images/act3/act3-elfstack-g5a.png)

Narrowing down the resultset in Kibana:

![Answer gold 5b](/images/act3/act3-elfstack-g5b.png)

> Question 6: What was the IP address of the system you found in the previous question?

Answer: 172.24.25.12

![Answer gold 6](/images/act3/act3-elfstack-g6.png)

> Question 7: A process was launched when the user executed the program AFTER they downloaded it. What was that Process ID number (digits only please)?

Answer: 10014

Query: 

```sql
(event.CommandLine:*user* AND event.CommandLine:*elf_user02*) OR (event.ParentCommandLine:*user* AND event.ParentCommandLine:*elf_user02*)
```

![Answer gold 7](/images/act3/act3-elfstack-g7.png)

> Question 8: Did the attacker's payload make an outbound network connection? Our ElfSOC analysts need your help identifying the destination TCP port of this connection.

IOC's extracted from the previous query:

| IOC | Value |
| --- | ----- |
| Process ID | 10014 |
| Download path | ```C:\Users\elf_user02\Downloads\howtosavexmas\howtosavexmas.pdf.exe``` |
| Parent Process ID | 5680 |
| Parent Process | Explorer.exe |
| Download Time | Sep 15, 2024 @ 16:37:50.00 |
| Execution Time | Sep 15, 2024 @ 16:38:34.000 | 
| Event Hostname | SleighRider.northpole.local |

Answer: 8443

![Answer gold 8](/images/act3/act3-elfstack-g8.png)


> Question 9: The attacker escalated their privileges to the SYSTEM account by creating an inter-process communication (IPC) channel. Submit the alpha-numeric name for the IPC channel used by the attacker.

Answer: ddpvccdbr

![Answer gold 9](/images/act3/act3-elfstack-g9.png)

> Question 10: The attacker's process attempted to access a file. Submit the full and complete file path accessed by the attacker's process.

Answer: C:\Users\elf_user02\Desktop\kkringl315@10.12.25.24.pem

![Answer gold 10](/images/act3/act3-elfstack-g10.png)

> Question 11: The attacker attempted to use a secure protocol to connect to a remote system. What is the hostname of the target server?

Answer: kringleSSleigH

![Answer gold 11](/images/act3/act3-elfstack-g11.png)

> Question 12: The attacker created an account to establish their persistence on the Linux host. What is the name of the new account created by the attacker?

Answer: ssdh

![Answer gold 12](/images/act3/act3-elfstack-g12.png)

> Question 13: The attacker wanted to maintain persistence on the Linux host they gained access to and executed multiple binaries to achieve their goal. What was the full CLI syntax of the binary the attacker executed after they created the new user account?

Answer: ```/usr/sbin/usermod -a -G sudo ssdh```

![Answer gold 13](/images/act3/act3-elfstack-g13.png)

> Question 14: The attacker enumerated Active Directory using a well known tool to map our Active Directory domain over LDAP. Submit the full ISO8601 compliant timestamp when the first request of the data collection attack sequence was initially recorded against the domain controller.

Answer: 2024-09-16T11:10:12-04:00

I had issues finding the right timestamp. I retorted to creating a Lucene regex seach matching the format I needed, hopefully wishing it would match a timestmap. And it did:

```sql
/.*\d{4}\-\d{2}\-\d{2}T\d{2}:\d{2}:\d{2}\-\d{2}:\d{2}.*/ AND *dc01*
```

![Answer gold 14](/images/act3/act3-elfstack-g14.png)

> Question 15: The attacker attempted to perform an ADCS ESC1 attack, but certificate services denied their certificate request. Submit the name of the software responsible for preventing this initial attack.

Answer: KringleGuard

![Answer gold 15](/images/act3/act3-elfstack-g15.png)

> Question 16: We think the attacker successfully performed an ADCS ESC1 attack. Can you find the name of the user they successfully requested a certificate on behalf of?

Answer: nutcrakr

![Answer gold 16](/images/act3/act3-elfstack-g16.png)

> Question 17: One of our file shares was accessed by the attacker using the elevated user account (from the ADCS attack). Submit the folder name of the share they accessed.

Answer: WishLists

![Answer gold 17](/images/act3/act3-elfstack-g17.png)

> Question 18: The naughty attacker continued to use their privileged account to execute a PowerShell script to gain domain administrative privileges. What is the password for the account the attacker used in their attack payload?

Answer: 



 LOGIN INFORMATION:
ess_syslog_sender  |            URL: http://localhost:5601
ess_syslog_sender  |            Username: elastic
ess_syslog_sender  |            Password: ELFstackLogin!
ess_syslog_sender  |
ess_syslog_sender  |            SET DATE IN ANALYSIS: DISCOVER TO 2024