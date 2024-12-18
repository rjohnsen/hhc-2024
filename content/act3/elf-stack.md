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

Answer: 





 LOGIN INFORMATION:
ess_syslog_sender  |            URL: http://localhost:5601
ess_syslog_sender  |            Username: elastic
ess_syslog_sender  |            Password: ELFstackLogin!
ess_syslog_sender  |
ess_syslog_sender  |            SET DATE IN ANALYSIS: DISCOVER TO 2024