+++
title = 'Elf Stack'
date = 2024-12-14T14:54:09+01:00
draft = true
weight = 1
+++

## Objective

> Help the ElfSOC analysts track down a malicious attack against the North Pole domain.

You are offered to either download the logs and do the excersices on your own, or download the ELK stack (logs included): 

* https://hhc24-elfstack.holidayhackchallenge.com/download_file/log_chunk_2.log.zip
* https://hhc24-elfstack.holidayhackchallenge.com/download_file/elf-stack-siem-with-logs.zip
* https://hhc24-elfstack.holidayhackchallenge.com/download_file/log_chunk_1.log.zip

I chose to mainly solve this objective using Elastic, since this is what I am used to. However, as we shall see later on, some CLI magic had to happen.

## Hints

| From | Hint |
| ---- | ---- |
| Fitzy Shortstack | Fitzy Shortstack |
| Fitzy Shortstack | Some elves have tried to make tweaks to the Elf Stack log parsing logic, but only a seasoned SIEM engineer or analyst may find that task useful. |
| Fitzy Shortstack | I was on my way to grab a cup of hot chocolate the other day when I overheard the reindeer talking about playing games. The reindeer mentioned trying to invite Wombley and Alabaster to their games. This may or may not be great news. All I know is, the reindeer better create formal invitations to send to both Wombley and Alabaster. |
| Fitzy Shortstack | I'm part of the ElfSOC that protects the interests here at the North Pole. We built the Elf Stack SIEM, but not everybody uses it. Some of our senior analysts choose to use their command line skills, while others choose to deploy their own solution. Any way is possible to hunt through our logs! |
| Fitzy Shortstack | One of our seasoned ElfSOC analysts told me about a great resource to have handy when hunting through event log data. I have it around here somewhere, or maybe it was online. Hmm. |
| Fitzy Shortstack | Our Elf Stack SIEM has some minor issues when parsing log data that we still need to figure out. Our ElfSOC SIEM engineers drank many cups of hot chocolate figuring out the right parsing logic. The engineers wanted to ensure that our junior analysts had a solid platform to hunt through log data. |

## Solution

### Silver

#### Question 1

> How many unique values are there for the event_source field in all logs?

**Answer:** 5

**Comment:**

_Elastic's visualization library in **Kibana** makes it simple to create insightful, dynamic table views from Elasticsearch data. Tables provide a structured way to display detailed information, making them ideal for logs, metrics, and categorical data analysis. With easy configuration and filtering options, users can highlight key metrics and trends directly within their datasets. Interactive dashboards enhance these table views, allowing seamless cross-filtering and drill-downs. This approach ensures a clear and actionable understanding of your data._


![Answer silver 1](/images/act3/act3-elfstack-s1.png)

#### Question 2

> Which event_source has the fewest number of events related to it?

**Answer:** AuthLog

**Comment:**

_Elastic's visualization library to the rescue for this one as well_

![Answer silver 2](/images/act3/act3-elfstack-s1.png)


#### Question 3

> Using the event_source from the previous question as a filter, what is the field name that contains the name of the system the log event originated from?

**Answer:** event.hostname

![Answer silver 3](/images/act3/act3-elfstack-s3.png)

_Most fields can be found either by poking around in the record itself, as seen here. Or, by looking into the "Available fields" section on the left side (given that you have a representational selection of records from your query)_

#### Question 4

> Which event_source has the second highest number of events related to it?

**Answer:** NetflowPmacct

![Answer silver 4](/images/act3/act3-elfstack-s1.png)

**Comment:**

_Elastic's visualization library to the rescue for this one as well_

#### Question 5

> Using the event_source from the previous question as a filter, what is the name of the field that defines the destination port of the Netflow logs?

**Answer:** event.port_dst

![Answer silver 5](/images/act3/act3-elfstack-s5.png)

**Comment:**

_Most fields can be found either by poking around in the record itself, as seen here. Or, by looking into the "Available fields" section on the left side (given that you have a representational selection of records from your query)_

#### Question 6

> Which event_source is related to email traffic?

**Answer:** SnowGlowMailPxy

![Answer silver 6](/images/act3/act3-elfstack-s1.png)

**Comment:**

_Elastic's visualization library .. We are getting pretty used to this view by now_

#### Question 7

> Looking at the event source from the last question, what is the name of the field that contains the actual email text?

**Answer:** event.Body

![Answer silver 7](/images/act3/act3-elfstack-s7.png)

**Comment:**

_Elastic's visualization library .. Yup - we are pretty used to this view by now_

#### Question 8

> Using the 'GreenCoat' event_source, what is the only value in the hostname field?

**Answer:** SecureElfGwy

![Answer silver 8](/images/act3/act3-elfstack-s8.png)

**Comment:**

_Here I built myself a view consisting of "@timestamp", "event.source" and "hostname". This is a great way to build custom views when your are hunting for something_

#### Question 9 

> Using the 'GreenCoat' event_source, what is the name of the field that contains the site visited by a client in the network?

**Answer:** event.url

![Answer silver 9](/images/act3/act3-elfstack-s9.png)

**Comment:**

_Nothing much to elaborate on here_

#### Question 10

> Using the 'GreenCoat' event_source, which unique URL and port (URL:port) did clients in the TinselStream network visit most?

**Answer:** pagead2.googlesyndication.com:443

![Answer silver 10](/images/act3/act3-elfstack-s10.png)

**Comment:**

_Elastic's visualization library table view can handle multiple columns - which make it a great tool for tasks like this._

#### Question 11

> Using the 'WindowsEvent' event_source, how many unique Channels is the SIEM receiving Windows event logs from?

**Answer:** 5

![Answer silver 11](/images/act3/act3-elfstack-s11.png)

**Comment:**

_Elastic's visualization library has many options you can fiddle with on the right side according to taste, preference and assignment._

#### Question 12

> What is the name of the event.Channel (or Channel) with the second highest number of events?

**Answer:** Microsoft-Windows-Sysmon/Operational

![Answer silver 12](/images/act3/act3-elfstack-s11.png)

**Comment:**

_Elastic's visualization library .. you can also interpet data yourself in this tool ..._

#### Question 13

> Our environment is using Sysmon to track many different events on Windows systems. What is the Sysmon Event ID related to loading of a driver?

**Answer:** 6

**Comment:**

_You know the objective is getting serious when you got questions related to Sysmon. For reference I have chosen to include a reference to Sysmon Event Ids here. Another good resource for the ids is: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon_

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

#### Question 14

> What is the Windows event ID that is recorded when a new service is installed on a system?

**Answer:** 4697

**Comment:**

_A great resource for looking up Windows Event IDs is: https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/_

#### Question 15

> Using the WindowsEvent event_source as your initial filter, how many user accounts were created?

**Answer:** 0

**Comment:**

_Looked for Windows event code 4720, but couldn't find any. So I figured out there were none user created_

![Answer silver 15](/images/act3/act3-elfstack-s15.png)

### Gold

#### Question 1

> What is the event.EventID number for Sysmon event logs relating to process creation?

**Answer:** 1

**Comment:**

_This is just one of the IDs you must know by the heart._

#### Question 2

> How many unique values are there for the 'event_source' field in all of the logs?

**Answer:** 5 

**Comment:**

_The same answer for some ealier questions._

#### Question 3

> What is the event_source name that contains the email logs?

**Answer:** SnowGlowMailPxy

**Comment:**

_The same answer for some ealier questions._

#### Question 4

> The North Pole network was compromised recently through a sophisticated phishing attack sent to one of our elves. The attacker found a way to bypass the middleware that prevented phishing emails from getting to North Pole elves. As a result, one of the Received IPs will likely be different from what most email logs contain. Find the email log in question and submit the value in the event 'From:' field for this email log event.

**Answer:** kriskring1e@northpole.local

![Answer gold 4](/images/act3/act3-elfstack-g4.png)

**Comment:**

_Elastic's visualization library to the rescue for this one as well_

#### Question 5

> Our ElfSOC analysts need your help identifying the hostname of the domain computer that established a connection to the attacker after receiving the phishing email from the previous question. You can take a look at our GreenCoat proxy logs as an event source. Since it is a domain computer, we only need the hostname, not the fully qualified domain name (FQDN) of the system.

**Answer:** SleighRider

**Comment:**

_Step 1: Finding information by using Lens. My hypothesis here is to find the IP, hostname and user that occurs the least:_

![Answer gold 5a](/images/act3/act3-elfstack-g5a.png)

_Step 2: Having a set of interesting IP, hostname and user, I could start narrowing down the resultset in Kibana. In this screenshot I have narrowed myself in on user "elf_user02" due to findings in step 1:_

![Answer gold 5b](/images/act3/act3-elfstack-g5b.png)

#### Question 6

> What was the IP address of the system you found in the previous question?

**Answer:** 172.24.25.12

**Comment:**

_Added field "even.ip" to the result table view for the search from question 5 above._

![Answer gold 6](/images/act3/act3-elfstack-g6.png)

#### Question 7

> A process was launched when the user executed the program AFTER they downloaded it. What was that Process ID number (digits only please)?

**Answer:** 10014

**Comment:**

_According to the question we are looking for a process that was launched. Given the context the last few questions (regarding user "elf_user02"), I made a hypothesis that this username would be present in the commandline - both in the "event.CommandLine" and the "event.ParentCommandLine". Based on this, I made the following query:_
```sql
(event.CommandLine:*user* AND event.CommandLine:*elf_user02*) OR (event.ParentCommandLine:*user* AND event.ParentCommandLine:*elf_user02*)
```

![Answer gold 7](/images/act3/act3-elfstack-g7.png)

_I also filtered on "event.EventID: 1" according to the Sysmon table I included earlier._

#### Question 8

> Did the attacker's payload make an outbound network connection? Our ElfSOC analysts need your help identifying the destination TCP port of this connection.

**Answer:** 8443

**Comment:**

_For this question I thought it was important to extract IOC's from the previous query:_

| IOC | Value |
| --- | ----- |
| Process ID | 10014 |
| Download path | ```C:\Users\elf_user02\Downloads\howtosavexmas\howtosavexmas.pdf.exe``` |
| Parent Process ID | 5680 |
| Parent Process | Explorer.exe |
| Download Time | Sep 15, 2024 @ 16:37:50.00 |
| Execution Time | Sep 15, 2024 @ 16:38:34.000 | 
| Event Hostname | SleighRider.northpole.local |

_Based on the IOC list above, I identified the "Download Time" and the filename from the "Download Path" as important indicators. The string **"howtosavexmas"** makes an excellent wildcard search term because of its uniqueness. Combined with **Sysmon Event ID 3 (Network Connection)**, these elements provided valuable input for my query. I focused on finding timestamps in the search results that closely matched the download's time window, enabling a more targeted investigation._ 

![Answer gold 8](/images/act3/act3-elfstack-g8.png)


#### Question 9

> The attacker escalated their privileges to the SYSTEM account by creating an inter-process communication (IPC) channel. Submit the alpha-numeric name for the IPC channel used by the attacker.

**Answer:** ddpvccdbr

**Comment:**

_IPC means Pipes. I just made a wildcard search for pipe paired with Sysmon ID 1._

![Answer gold 9](/images/act3/act3-elfstack-g9.png)

#### Question 10

> The attacker's process attempted to access a file. Submit the full and complete file path accessed by the attacker's process.

**Answer:** C:\Users\elf_user02\Desktop\kkringl315@10.12.25.24.pem

**Comment:**

_In this query I have filtered on certain event ids. Here’s a table summarizing the filtered event IDs and their descriptions:_

| **Event ID** | **Source**         | **Description**                                                                                      | **Details**                                                                                   |
|--------------|--------------------|------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| **4663**     | Windows Security   | **Audit Object Access**: Logged when a file or folder is accessed, modified, or deleted.            | Requires "Audit Object Access" policy and specific auditing settings on the object.          |
| **4656**     | Windows Security   | **Handle Request**: Logged when an attempt is made to access an object (file or directory).         | Shows requested access before it is granted or denied.                                        |
| **11**       | Sysmon             | **File Created**: Logged when a new file is created.                                                | Includes the file path, providing insight into potential malicious file creation activity.    |
| **15**       | Sysmon             | **File Deleted**: Logged when a file is deleted.                                                    | Tracks file deletion, useful for identifying attempts to cover tracks or remove evidence.     |
| **23**       | Sysmon             | **FileStream Created**: Logged when an alternate data stream (ADS) is created within a file.        | Indicates potential hiding of data within ADS, a technique often used by attackers.|

_I have also filtered on some process ID's present in either "event.processId" and "event.ProcessID". Why there are two fields having nearly identical names is unknown to me. Anyways, these process ids where found along the way during the investigation (this is how I roll as a threat hunter).

![Answer gold 10](/images/act3/act3-elfstack-g10.png)

#### Question 11

> The attacker attempted to use a secure protocol to connect to a remote system. What is the hostname of the target server?

**Answer:** kringleSSleigH

**Comment:**

_Followed the trail using the IP from the last question (it wasn't visible in my screenshot)._

![Answer gold 11](/images/act3/act3-elfstack-g11.png)

#### Question 12

> The attacker created an account to establish their persistence on the Linux host. What is the name of the new account created by the attacker?

**Answer:** ssdh

**Comment:**

_On this one I was lazy. I thought he attacker used the CLI on the Linux host. So - adduser was the most likely from my mind._

![Answer gold 12](/images/act3/act3-elfstack-g12.png)

#### Question 13

> The attacker wanted to maintain persistence on the Linux host they gained access to and executed multiple binaries to achieve their goal. What was the full CLI syntax of the binary the attacker executed after they created the new user account?

**Answer:** ```/usr/sbin/usermod -a -G sudo ssdh```

**Comment:**

_From the previous question and answer I saw that the term "TTY" figured a lot._

![Answer gold 13](/images/act3/act3-elfstack-g13.png)

#### Question 14

> The attacker enumerated Active Directory using a well known tool to map our Active Directory domain over LDAP. Submit the full ISO8601 compliant timestamp when the first request of the data collection attack sequence was initially recorded against the domain controller.

**Answer:** 2024-09-16T11:10:12-04:00

**Comment:**

_I had issues finding the right timestamp. I retorted to creating a Lucene regex seach matching the format I needed, hopefully wishing it would match a timestmap. And it did:_

```reqex
/.*\d{4}\-\d{2}\-\d{2}T\d{2}:\d{2}:\d{2}\-\d{2}:\d{2}.*/ AND *dc01*
```
_Also narrowed down the query to handle just "event.ServicePort: 389" (lDAP)_

![Answer gold 14](/images/act3/act3-elfstack-g14.png)

#### Question 15

> The attacker attempted to perform an ADCS ESC1 attack, but certificate services denied their certificate request. Submit the name of the software responsible for preventing this initial attack.

**Answer:** KringleGuard

**Comment:**

_For this query I found the following Windows Event IDs important:_

| **Event ID** | **Source**         | **Description**                                                                                        | **Details**                                                                                   |
|--------------|--------------------|--------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| **4888**     | Windows Security   | **Object Added to Central Access Policy**: Logged when an object (e.g., a file) is added to a Central Access Policy. | Indicates a change in resource access management under Dynamic Access Control (DAC).         |
| **4889**     | Windows Security   | **Central Access Policy Removed from Object**: Logged when a Central Access Policy is removed from an object.         | Tracks changes to DAC-based access control policies on resources.                            |
| **4890**     | Windows Security   | **Central Access Policy on Object Access Attempt**: Logged when access to an object under a Central Access Policy is attempted. | Useful for monitoring and troubleshooting access issues related to DAC policies.             |

![Answer gold 15](/images/act3/act3-elfstack-g15.png)

#### Question 16

> We think the attacker successfully performed an ADCS ESC1 attack. Can you find the name of the user they successfully requested a certificate on behalf of?

**Answer:** nutcrakr

**Comment:**

_Using the same query as the last one_

![Answer gold 16](/images/act3/act3-elfstack-g16.png)

#### Question 17

> One of our file shares was accessed by the attacker using the elevated user account (from the ADCS attack). Submit the folder name of the share they accessed.

**Answer:** WishLists

**Comment:**

_This event ID was important for this query:_

| **Event ID** | **Source**         | **Description**                                                                                   | **Details**                                                                                   |
|--------------|--------------------|---------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| **5145**     | Windows Security   | **A network share object was accessed.**                                                         | Logged when a file or folder is accessed over a shared network resource (SMB).               |

![Answer gold 17](/images/act3/act3-elfstack-g17.png)

#### Question 18

> The naughty attacker continued to use their privileged account to execute a PowerShell script to gain domain administrative privileges. What is the password for the account the attacker used in their attack payload?

**Answer:** fR0s3nF1@k3_s

**Comment:**

_I fiddled quite a bit with finding something sensible in Elastic. After much struggle I downloaded the logs to my Kali machine and started grepping instead. With that approach it took me some 10 seconds on a slow computer to find the password:_

```bash
grep -i nutcrakr *.log
```

_Output, password found in PowerShell variable ```$pswd```:_

```bash
log_chunk_2.log:<134>1 2024-09-16T11:33:12-04:00 SleighRider.northpole.local WindowsEvent - - - {"MessageNumber": 1, "MessageTotal": 1, "ScriptBlockText": "Add-Type -AssemblyName System.DirectoryServices\n$ldapConnString = \"LDAP://CN=Domain Admins,CN=Users,DC=northpole,DC=local\"\n$username = \"nutcrakr\"\n$pswd = 'fR0s3nF1@k3_s'\n$nullGUID = [guid]'00000000-0000-0000-0000-000000000000'\n$propGUID = [guid]'00000000-0000-0000-0000-000000000000'
```

#### Question 19 

> The attacker then used remote desktop to remotely access one of our domain computers. What is the full ISO8601 compliant UTC EventTime when they established this connection?

**Answer:** 2024-09-16T15:35:57.000Z

**Comment:**

_Logon ID 10 in Windows refers to a Remote Interactive Logon. It is typically associated with Remote Desktop Protocol (RDP) sessions, where a user connects to a machine remotely using tools like Remote Desktop._

![Answer gold 19](/images/act3/act3-elfstack-g19.png)

#### Question 20

> The attacker is trying to create their own naughty and nice list! What is the full file path they created using their remote desktop connection?

**Answer:** C:\WishLists\santadms_only\its_my_fakelst.txt

**Comment:**

_Here I narrowed down/filtered my query using artefacts I had found along the way. When I had a low number of records (37), I simply scrolled through the customized view table and found a reference to Notepad_

![Answer gold 20](/images/act3/act3-elfstack-g20.png)

#### Question 21

> The Wombley faction has user accounts in our environment. How many unique Wombley faction users sent an email message within the domain?

**Answer:** 4

**Comment:**
_I simply took a look at all the receiving e-mail addresses and found a pattern - "wco". I figured out that the "w" was for "Wombley". I set up my query like in the screenshot, and then went into the "Field Statistics" to get more information_

![Answer gold 21](/images/act3/act3-elfstack-g21.png)

#### Question 22

> The Alabaster faction also has some user accounts in our environment. How many emails were sent by the Alabaster users to the Wombley faction users?

**Answer:** 22

**Comment:**

_I took basis in the previous query results and added "asnowball" into the mix after finding this reference in the query results._

![Answer gold 22](/images/act3/act3-elfstack-g22.png)

#### Question 23

> Of all the reindeer, there are only nine. What's the full domain for the one whose nose does glow and shine? To help you narrow your search, search the events in the 'SnowGlowMailPxy' event source.

**Answer:** rud01ph.glow

**Comment:**

_For this I took basis in the question text and extracted some sensible keywords to search for. All MacGyver style:_

![Answer gold 23](/images/act3/act3-elfstack-g23.png)

#### Question 24

> Question 24: With a fiery tail seen once in great years, what's the domain for the reindeer who flies without fears? To help you narrow your search, search the events in the 'SnowGlowMailPxy' event source.

**Answer:** c0m3t.halleys

**Comment:**

_The qustion starts of with an important clue, "With a fiery tail seen once in great years". This could only mean Halleys comet, which will be the basis for my query:_

![Answer gold 24](/images/act3/act3-elfstack-g24.png)

_And done!_ 

![Answer gold 25](/images/act3/act3-elfstack-g25.png)


