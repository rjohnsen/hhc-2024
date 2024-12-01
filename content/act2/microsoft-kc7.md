+++
title = 'Microsoft Kc7'
date = 2024-11-23T13:18:55+01:00
draft = true
weight = 5
+++

> Welcome to your mission to solve the The Great Elf Conflict! To do so, you'll need to harness the power of KQL (Kusto Query Language) to navigate through the data and uncover crucial evidence.
> 
> Your next step is to meet with Eve Snowshoes, Cyber Engineer, at the at the North Pole Cyber Defense Unit. Eve is known for unmatched expertise in KQL and has been eagerly awaiting your arrival. Alt text
> 
> Eve greets you with a nod and gestures toward the terminal. "KQL is like a key, unlocking the hidden secrets buried within the data."

### Section 1: KQL 101

#### Question 1

> Welcome to your mission to solve the The Great Elf Conflict! To do so, you'll need to harness the power of KQL (Kusto Query Language) to navigate through the data and uncover crucial evidence.
> 
> Your next step is to meet with Eve Snowshoes, Cyber Engineer, at the at the North Pole Cyber Defense Unit. Eve is known for unmatched expertise in KQL and has been eagerly awaiting your arrival. Alt text
> 
> Eve greets you with a nod and gestures toward the terminal. "KQL is like a key, unlocking the hidden secrets buried within the data."
> 
> Type let’s do this to begin your KQL training.

#### Question 2

> The first command Eve Snowshoes teaches you is one of the most useful in querying data with KQL. It helps you peek inside each table, which is critical for understanding the structure and the kind of information you're dealing with. By knowing what's in each table, you’ll be able to create more precise queries and uncover exactly what you need.

```sql
Employees
    | take 10
```

> Eve has shared the first table with you. Now, run a take 10 on all the other tables to see what they contain.
> 
> You can find the tables you have access to at the top of the ADX query window.
> 
> Once you've examined all the tables, type ```when in doubt take 10``` to proceed.


##### Tables available

| Table Name | Description |
| ---------- | ----------- |
| AuthenticationEvents | Records successful and failed logins to devices on the company network. This includes logins to the company’s mail server. |
| Email | Records emails sent and received by employees. |
| Employees | Contains information about the company’s employees. |
| FileCreationEvents | Records files stored on employee’s devices. |
| InboundNetworkEvent | Records inbound network events including browsing activity from the Internet to devices within the company network. |
| OutboundNetworkEvents | Records outbound network events including browsing activity from within the company network out to the Internet. |
| PassiveDns (External) | Records IP-domain resolutions. | 
| ProcessEvents | Records processes created on employee’s devices. |
| SecurityAlerts | Records security alerts from an employee’s device or the company’s email security system. |

#### Question 3

> Now, let’s gather more intelligence on the employees. To do this, we can use the count operator to quickly calculate the number of rows in a table. This is helpful for understanding the scale of the data you’re working with.

```sql
Employees
    | count 
```

How many elves did you find?

Used the example query: 

```sql
Employees
    | count 
```

The answer is 90

#### Question 4

> You can use the where operator with the Employees table to locate a specific elf. Here’s a template you can follow:

```sql
Employees
    | where <field><operator><value>
```

> **Field:** The column you want to filter by (e.g., role).
> **Operator:** The condition you’re applying (e.g., == for an exact match).
> **Value:** The specific value you’re looking for in the field (e.g., Chief Elf Officer).

Can you find out the name of the Chief Toy Maker?

```sql
Employees
    | where role has "toy"
```

Answer: Shinny Upatree

#### Question 5

> Here are some additional operators the North Pole Cyber Defense Unit commonly uses. 
> **==** : Checks if two values are exactly the same. Case-sensitive.
> **contains** : Checks if a string appears anywhere, even as part of a word. Not case-sensitive.
> **has** : Checks if a string is a whole word. Not case-sensitive.
> **has_any** : Checks if any of the specified words are present. Not case-sensitive.
> **in** : Checks if a value matches any item in a list. Case-sensitive.
> Type operator to continue.

#### Question 6

> We can learn more about an elf by cross-referencing information from other tables. Let’s take a look at Angel Candysalt’s correspondence. First, retrieve her email address from the Employees table, and then use it in a query in the Email table.

```sql
Email
    | where recipient == "<insert Angel Candysalt’s email address here>"
    | count
```

How many emails did Angel Candysalt receive?

```sql
let EMAIL_LIST = Employees
    | where name has "Candysalt"
    | project email_addr;
Email
    | where recipient in (EMAIL_LIST)
    | count
```

Answer: 31.

#### Question 7

> You can use the distinct operator to filter for unique values in a specific column.
> Here's a start:

```sql
Email
    | where sender has "<insert domain name here>"
    | distinct <field you need>
    | count
```

How many distinct recipients were seen in the email logs from twinkle_frostington@santaworkshopgeeseislands.org?

```sql
Email
    | where sender has "twinkle_frostington@santaworkshopgeeseislands.org"
    | distinct recipient
    | count
```

Answer: 32

#### Question 8

> It’s time to put everything we’ve learned into action!

```sql
OutboundNetworkEvents
    | where src_ip == "<insert IP here>"
    | <operator> <field>
    | <operator>
```

How many distinct websites did Twinkle Frostington visit?

```sql
let IPADDR = Employees
    | where name has "Twinkle Frostington"
    | project ip_addr;
OutboundNetworkEvents
    | where src_ip in (IPADDR)
    | summarize count()
```

Answer: 4

#### Question 9

> How many distinct domains in the PassiveDns records contain the word green?

```sql
PassiveDns
    | where <field> contains “<value>”
    | <operator> <field>
    | <operator>
```

> You may have notice we’re using contains instead of has here. That’s because has will look for an exact match (the word on its own), while contains will look for the specified sequence of letters, regardless of what comes before or after it. You can try both on your query to see the difference!

```sql
PassiveDns
    | where domain contains "green"
    | summarize count()
```

Answer: 10

#### Question 10

> Sometimes, you’ll need to investigate multiple elves at once. Typing each one manually or searching for them one by one isn’t practical. That’s where let statements come in handy. A let statement allows you to save values into a variable, which you can then easily access in your query.
> 
> Let’s look at an example. To find the URLs they accessed, we’ll first need their IP addresses. But there are so many Twinkles! So we’ll save the IP addresses in a let statement, like this:

```sql
let twinkle_ips =
    Employees
    | where name has "<the name we’re looking for>"
    | distinct ip_addr
;
```

> This saves the result of the query into a variable. Now, you can use that result easily in another query:

```sql
OutboundNetworkEvents  
    | where src_ip in (twinkle_ips)  
    | distinct <field>
```

How many distinct URLs did elves with the first name Twinkle visit?

```sql
let twinkle_ips =
    Employees
    | where name has "twinkle"
    | distinct ip_addr
;
OutboundNetworkEvents  
    | where src_ip in (twinkle_ips)  
    | distinct url
    | summarize count()
```

Answer: 8

#### Flag

The flag is the last question answered. Thus, ```8``` is the flag.

### Section 2: Operation Surrender: Alabaster's Espionage

#### Question 1

> Eve Snowshoes approaches with a focused expression. "Welcome to Operation Surrender: Alabaster's Espionage. In this phase, Team Alabaster has executed a covert operation, and your mission is to unravel their tactics. You'll need to piece together the clues and analyze the data to understand how they gained an advantage."
> 
> Type surrender to get started!

#### Question 2

> Team Alabaster, with their limited resources, was growing desperate for an edge over Team Wombley. Knowing that a direct attack would be costly and difficult, they turned to espionage. Their plan? A carefully crafted phishing email that appeared harmless but was designed to deceive Team Wombley into downloading a malicious file. The email contained a deceptive message with the keyword “surrender” urging Wombley’s members to click on a link.
>
> Now, it's up to you to trace the origins of this operation.
> 
> Who was the sender of the phishing email that set this plan into motion?
> 
> Try checking out the email table using the knowledge you gained in the previous section!

Answer:

```sql
Email
    | where subject has "surrender"
    | distinct sender
```

Sender is: surrender@northpolemail.com

#### Question 3

> Team Alabaster’s phishing attack wasn’t just aimed at a single target—it was a coordinated assault on all of Team Wombley. Every member received the cleverly disguised email, enticing them to click the malicious link that would compromise their systems.
> 
> Hint: the distinct operator would help here Your mission is to determine the full scale of this operation.
> 
> How many elves from Team Wombley received the phishing email?

Answer:

```sql
Email
    | where subject has "surrender"
    | distinct recipient
    | summarize count()
```

Number is: 22

#### Question 4

> The phishing email from Team Alabaster included a link to a file that appeared legitimate to Team Wombley. This document, disguised as an important communication, was part of a carefully orchestrated plan to deceive Wombley’s members into taking the bait.
> 
> To understand the full extent of this operation, we need to identify the file where the link led to in the email.
> 
> What was the filename of the document that Team Alabaster distributed in their phishing email?

Answer

```sql
Email
    | where subject has "surrender"
    | project document_name=tostring(split(link, '/')[-1])
    | distinct document_name
```

Document name is: Team_Wombley_Surrender.doc

#### Question 5

> As the phishing emails landed in the inboxes of Team Wombley, one elf was the first to click the URL, unknowingly triggering the start of Team Alabaster’s plan. By connecting the employees to their network activity, we can trace who fell for the deception first. To find the answer, you'll need to join two tables: Employees and OutboundNetworkEvents. The goal is to match employees with the outbound network events they initiated by using their IP addresses.
> 
> Here’s an example query to help you:

```sql
Employees
    | join kind=inner (
        OutboundNetworkEvents
    ) on $left.ip_addr == $right.src_ip // condition to match rows
    | where url contains "< maybe a filename :) >"
    | project name, ip_addr, url, timestamp // project returns only the information you select
    | sort by timestamp asc //sorts time ascending
```

> This query will give you a list of employees who clicked on the phishing URL. The first person to click will be at the top of the list!

Who was the first person from Team Wombley to click the URL in the phishing email?

Answer:

```sql
Employees
    | join kind=inner (
        OutboundNetworkEvents
    ) on $left.ip_addr == $right.src_ip // condition to match rows
    | where url contains "Team_Wombley_Surrender.doc"
    | project name, ip_addr, url, timestamp // project returns only the information you select
    | sort by timestamp asc //sorts time ascending
    | take 1
```

The one that clicked the link first was: Joyelle Tinseltoe

#### Question 6

> Once the phishing email was clicked and the malicious document was downloaded, another file was created upon execution of the .doc. This file allowed Team Alabaster to gain further insight into Team Wombley’s operations. To uncover this, you’ll need to investigate the processes that were executed on Joyelle Tinseltoe’s machine.
> 
> Your mission is to determine the name of the file that was created after the .doc was executed.
> 
> Focus on Joyelle Tinseltoe’s hostname and explore the ProcessEvents table. This table tracks which processes were started and by which machines. By filtering for Joyelle’s hostname and looking at the timestamps around the time the file was executed, you should find what you’re looking for. Here’s an example to help guide you:

```sql
ProcessEvents
    | where timestamp between(datetime("2024-11-25T09:00:37Z") .. datetime("2024-11-26T17:20:37Z")) //you’ll need to modify this
    | where hostname == "<Joyelle's hostname>"
```

> This query will show processes that ran on Joyelle Tinseltoe’s machine within the given timeframe.

What was the filename that was created after the .doc was downloaded and executed?

Answer:

```sql
let TIMESTART = toscalar(Employees
    | join kind=inner (
        OutboundNetworkEvents
    ) on $left.ip_addr == $right.src_ip // condition to match rows
    | where url contains "Team_Wombley_Surrender.doc"
    | project name, ip_addr, url, timestamp // project returns only the information you select
    | sort by timestamp asc //sorts time ascending
    | take 1
    | project timestamp)
;
let HOSTNAME = toscalar(Employees
    | where  name == "Joyelle Tinseltoe"
    | project hostname
);
ProcessEvents
    | where timestamp between(TIMESTART .. TIMESTART+1h) //you’ll need to modify this
    | where hostname == HOSTNAME
    | summarize count() by process_name
```

Output:

| process_name | count_ |
| ------------ | ------ |
| cmd.exe | 1 |
| keylogger.exe | 4 |
| Explorer.exe | 2 |

keylogger.exe (since it has the most entries)

#### Question 7

> Well done on piecing together the clues and unraveling the operation!
> 
> Team Alabaster's phishing email, sent from surrender@northpolemail.com, targeted 22 elves from Team Wombley. The email contained a malicious document named Team_Wombley_Surrender.doc, which led to the first click by Joyelle Tinseltoe.
> 
> After the document was downloaded and executed, a malicious file was created, impacting the entire Team Wombley as it ran on all their machines, giving Team Alabaster access to their keystokes!
>
> To obtain your flag use the KQL below with your last answer!

```sql
let flag = "Change This!";
let base64_encoded = base64_encode_tostring(flag);
print base64_encoded
```

Solution

```sql
let TIMESTART = toscalar(Employees
    | join kind=inner (
        OutboundNetworkEvents
    ) on $left.ip_addr == $right.src_ip // condition to match rows
    | where url contains "Team_Wombley_Surrender.doc"
    | project name, ip_addr, url, timestamp // project returns only the information you select
    | sort by timestamp asc //sorts time ascending
    | take 1
    | project timestamp)
;
let HOSTNAME = toscalar(Employees
| where  name == "Joyelle Tinseltoe"
| project hostname
);
let flag = toscalar(ProcessEvents
    | where timestamp between(TIMESTART .. TIMESTART+1h) //you’ll need to modify this
    | where hostname == HOSTNAME
    | summarize count() by process_name
    | where count_ >= 4
    | project process_name
);
let base64_encoded = base64_encode_tostring(flag);
print base64_encoded
```

```
a2V5bG9nZ2VyLmV4ZQ==
```

#### Flag

The flag is the last question answered. Thus, ```a2V5bG9nZ2VyLmV4ZQ==``` is the flag.


#### Question 8

> "Fantastic work on completing Section 2!" Eve Snowshoes, Senior Security Analyst, says with a proud smile.
>
>"You’ve demonstrated sharp investigative skills, uncovering every detail of Team Wombley’s attack on Alabaster. Your ability to navigate the complexities of cyber warfare has been impressive.
>
>But now, we embark on Operation Snowfall: Team Wombley’s Ransomware Raid. This time, the difficulty will increase as we dive into more sophisticated attacks. Stay sharp, and let’s see if you can rise to the occasion once again!"
>
> Type snowfall to begin

### Section 3: Operation Snowfall: Team Wombley's Ransomware Raid

#### Qustion 1

> Team Wombley’s assault began with a password spray attack, targeting several accounts within Team Alabaster. This attack relied on repeated login attempts using common passwords, hoping to find weak entry points. The key to uncovering this tactic is identifying the source of the attack. Alt text Authentication events can be found in the AuthenticationEvents table. Look for a pattern of failed login attempts.
> 
> Here’s a query to guide you:

```sql
AuthenticationEvents
    | where result == "Failed Login"
    | summarize FailedAttempts = count() by username, src_ip, result
    | where FailedAttempts >= 5
    | sort by FailedAttempts desc
```

What was the IP address associated with the password spray?

Solution

```sql
AuthenticationEvents
    | where result == "Failed Login"
    | summarize FailedAttempts = count() by username, src_ip, result
    | where FailedAttempts >= 5
    | sort by FailedAttempts desc
    | summarize count() by src_ip
    | limit 1
```

59.171.58.12

#### Question 2

> After launching the password spray attack, Team Wombley potentially had success and logged into several accounts, gaining access to sensitive systems.
> 
> Eve Snowshoes weighs in: "This is where things start to get dangerous. The number of compromised accounts will show us just how far they’ve infiltrated."
>
> How many unique accounts were impacted where there was a successful login from 59.171.58.12?

Solution

```sql
AuthenticationEvents
    | where src_ip == "59.171.58.12"
    | where description !has "failed"
    | distinct username
    | summarize count()
```

23

#### Question 3

> In order to login to the compromised accounts, Team Wombley leveraged a service that was accessible externally to gain control over Alabaster’s devices.
> 
> Eve Snowshoes remarks, "Identifying the service that was open externally is critical. It shows us how the attackers were able to bypass defenses and access the network. This is a common weak point in many systems."
> 
> What service was used to access these accounts/devices?

Solution

The answer was found by inspecting the output from the query:

```
User successfully logged onto Elf-Lap-A-Snowflakebreeze via RDP.
```

#### Question 4

> Once Team Wombley gained access to Alabaster's system, they targeted sensitive files for exfiltration. Eve Snowshoes emphasizes, "When critical files are exfiltrated, it can lead to devastating consequences. Knowing exactly what was taken will allow us to assess the damage and prepare a response."
> 
> The ProcessEvents table will help you track activities that occurred on Alabaster’s laptop. By narrowing down the events by timestamp and hostname, you’ll be able to pinpoint the file that was exfiltrated.
> 
> What file was exfiltrated from Alabaster’s laptop?

Solution

```sql
let HOSTNAME = toscalar(Employees
    | where name has "Alabaster"
    | project hostname
);
let TIMEWINDOW = toscalar(AuthenticationEvents
    | where src_ip == "59.171.58.12"
    | where description !has "failed"
    | order by timestamp asc
    | limit 1
    | project timestamp
);
ProcessEvents
    | where timestamp >= TIMEWINDOW+10m
    | where hostname == HOSTNAME
    | extend filename = tostring(split(process_commandline, "\\")[-1])
    | summarize count() by filename
    | order by count_ desc
```

Secret_Files.zip

#### Question 5

> After exfiltrating critical files from Alabaster’s system, Team Wombley deployed a malicious payload to encrypt the device, leaving Alabaster locked out and in disarray.
> 
> Eve Snowshoes comments, "The final blow in this attack was the ransomware they unleashed. Finding the name of the malicious file will help us figure out how they crippled the system."
> 
> What is the name of the malicious file that was run on Alabaster's laptop?

Solution (same as previous solution due to statistics made):

```sql
let HOSTNAME = toscalar(Employees
    | where name has "Alabaster"
    | project hostname
);
let TIMEWINDOW = toscalar(AuthenticationEvents
    | where src_ip == "59.171.58.12"
    | where description !has "failed"
    | order by timestamp asc
    | limit 1
    | project timestamp
);
ProcessEvents
    | where timestamp >= TIMEWINDOW+10m
    | where hostname == HOSTNAME
    | extend filename = tostring(split(process_commandline, "\\")[-1])
    | summarize count() by filename
    | order by count_ desc
```

EncryptEverything.exe

#### Question 6

> Outstanding work! You've successfully pieced together the full scope of Team Wombley’s attack. Your investigative skills are truly impressive, and you've uncovered every critical detail.
> 
> Just to recap: Team Wombley launched a cyber assault on Alabaster, beginning with a password spray attack that allowed them to gain access to several accounts. Using an external service over RDP, they infiltrated Alabaster’s system, exfiltrating sensitive files including the blueprints for snowball cannons and drones. To further their attack, Wombley executed a malicious file, which encrypted Alabaster’s entire system leaving them locked out and in chaos.
> 
> To obtain your flag use the KQL below with your last answer!

```sql
let flag = "Change This!";
let base64_encoded = base64_encode_tostring(flag);
print base64_encoded
```

Solution

```sql
let flag = "EncryptEverything.exe";
let base64_encoded = base64_encode_tostring(flag);
print base64_encoded
```

```
RW5jcnlwdEV2ZXJ5dGhpbmcuZXhl
```

#### Flag

The flag is the last question answered. Thus, ```RW5jcnlwdEV2ZXJ5dGhpbmcuZXhl``` is the flag.

### Section 4: Echoes in the Frost: Tracking the Unknown Threat

#### Question 1

> As you close out the investigation into Team Wombley’s attack, Eve Snowshoes meets you with a serious expression. "You’ve done an incredible job so far, but now we face our most elusive adversary yet. This isn’t just another team—it’s an unknown, highly skilled threat actor who has been operating in the shadows, leaving behind only whispers of their presence. We’ve seen traces of their activity, but they’ve covered their tracks well."
> 
> She pauses, the weight of the challenge ahead clear. "This is where things get even more difficult. We’re entering uncharted territory—prepare yourself for the toughest investigation yet. Follow the clues, stay sharp, and let’s uncover the truth behind these Echoes in the Frost."
> 
> Type stay frosty to begin

#### Question 2

> Noel Boetie, the IT administrator, reported receiving strange emails about a breach from colleagues. These emails might hold the first clue in uncovering the unknown threat actor’s methods. Your task is to identify when the first of these suspicious emails was received.
> 
> Eve Snowshoes remarks, "The timing of these phishing emails is critical. If we can identify the first one, we’ll have a better chance of tracing the threat actor’s initial moves."
> 
> What was the timestamp of first phishing email about the breached credentials received by Noel Boetie?

Solution

```sql
Email
    | where subject contains "breach"
    | order by timestamp asc
```

```
2024-12-12T14:48:55Z
```

#### Question 3

> Noel Boetie followed the instructions in the phishing email, downloading and running the file, but reported that nothing seemed to happen afterward. However, this might have been the key moment when the unknown threat actor infiltrated the system.
> 
> When did Noel Boetie click the link to the first file?

Solution

```sql
let FIRST_TIMESTAMP = toscalar(Email
    | where subject contains "breach"
    | order by timestamp asc
);
let BOETIE_IP = toscalar(Employees
    | where username contains "boetie"
    | project ip_addr
);
OutboundNetworkEvents
    | where timestamp >= FIRST_TIMESTAMP
    | where src_ip == BOETIE_IP
    | order by timestamp asc
    | limit 1
```

```
2024-12-12T15:13:55Z
```

#### Question 4

> The phishing email directed Noel Boetie to download a file from an external domain.
> 
> Eve Snowshoes, "The domain and IP they used to host the malicious file is a key piece of evidence. It might lead us to other parts of their operation, so let’s find it."
> 
> What was the IP for the domain where the file was hosted?

Solution

```sql
let FIRST_TIMESTAMP = toscalar(Email
    | where subject contains "breach"
    | order by timestamp asc
);
let BOETIE_IP = toscalar(Employees
    | where username contains "boetie"
    | project ip_addr
);
let MALWARE_IP = OutboundNetworkEvents
    | where timestamp >= FIRST_TIMESTAMP
    | where src_ip == BOETIE_IP
    | order by timestamp asc
    | limit 1
    | extend domain = tostring(split(url, "/")[2])
    | join PassiveDns on $left.domain == $right.domain
    | distinct ip
;
MALWARE_IP
```

```
182.56.23.122
```

#### Question 5

> Let’s back up for a moment. Now that we’re thinking this through, how did the unknown threat actor gain the credentials to execute this attack? We know that three users have been sending phishing emails, and we’ve identified the domain they used.
> 
> It’s time to dig deeper into the AuthenticationEvents and see if anything else unusual happened that might explain how these accounts were compromised.
> 
> Eve Snowshoes suggests, "We need to explore the AuthenticationEvents for these users. Attackers often use compromised accounts to blend in and send phishing emails internally. This might reveal how they gained access to the credentials."
> 
> Let’s take a closer look at the authentication events. I wonder if any connection events from 182.56.23.122. If so what hostname was accessed?

Solution

```sql
let FIRST_TIMESTAMP = toscalar(Email
    | where subject contains "breach"
    | order by timestamp asc
);
let BOETIE_IP = toscalar(Employees
    | where username contains "boetie"
    | project ip_addr
);
let MALWARE_IP = toscalar(OutboundNetworkEvents
    | where timestamp >= FIRST_TIMESTAMP
    | where src_ip == BOETIE_IP
    | order by timestamp asc
    | limit 1
    | extend domain = tostring(split(url, "/")[2])
    | join PassiveDns on $left.domain == $right.domain
    | distinct ip
);
AuthenticationEvents
    | where src_ip == MALWARE_IP
    | project hostname
```

```
WebApp-ElvesWorkshop
```

#### Question 6

> It appears someone accessed the WebApp-ElvesWorkshop from the IP address 182.56.23.122. This could be a key moment in the attack. We need to investigate what was run on the app server and, more importantly, if the threat actor dumped any credentials from it.
> 
> Eve Snowshoes, "Accessing the web app from an external IP is a major red flag. If they managed to dump credentials from the app server, that could explain how they gained access to other parts of the system."
> 
> What was the script that was run to obtain credentials?

Solution

```sql
let TIMEWINDOW = InboundNetworkEvents
    | where src_ip == "182.56.23.122"
    | order by timestamp asc
    | summarize minTime = min(timestamp), maxTime = max(timestamp)+1h
;
ProcessEvents
    | where timestamp between (toscalar(TIMEWINDOW | project minTime) .. toscalar(TIMEWINDOW | project maxTime) )
    | where hostname has "WebApp-ElvesWorkshop"
    | order by timestamp asc
    | take 1
```

```
Invoke-Mimikatz.ps1
```

#### Question 7

> Okay back to Noel, after downloading the file, Noel Boetie followed the instructions in the email and ran it, but mentioned that nothing appeared to happen.
> 
> Since the email came from an internal source, Noel assumed it was safe - yet this may have been the moment the unknown threat actor silently gained access. We need to identify exactly when Noel executed the file to trace the beginning of the attack.
> 
> Eve Snowshoes, "It’s easy to see why Noel thought the email was harmless - it came from an internal account. But attackers often use compromised internal sources to make their phishing attempts more believable."
> 
> What is the timestamp where Noel executed the file? 

Solution

```sql
let FIRST_TIMESTAMP = Email
    | where subject contains "breach"
    | order by timestamp asc
;
let BOETIE_DATA = Employees
    | where username contains "boetie"
    | project ip_addr, username
;
ProcessEvents
    | where username == toscalar(BOETIE_DATA | project username)
    | where timestamp > toscalar(FIRST_TIMESTAMP | project timestamp)
    | order by timestamp asc
```

```
2024-12-12T15:14:38Z
```

#### Question 9

> After Noel ran the file, strange activity began on the system, including the download of a file called holidaycandy.hta. Keep in mind that attackers often use multiple domains to host different pieces of malware.
>
> Eve explains, "Attackers frequently spread their operations across several domains to evade detection."
> 
> What domain was the holidaycandy.hta file downloaded from?

Solution

```sql
OutboundNetworkEvents
    | where url has "holidaycandy.hta"
    | extend domain = tostring(split(url, "/")[2])
    | distinct domain
```

```
compromisedchristmastoys.com
```

#### Question 10

> An interesting series of events has occurred: the attacker downloaded a copy of frosty.txt, decoded it into a zip file, and used tar to extract the contents of frosty.zip into the Tasks directory.
> 
> This suggests the possibility that additional payloads or tools were delivered to Noel’s laptop. We need to investigate if any additional files appeared after this sequence.
> 
> Eve Snowshoes, "When an attacker drops files like this, it’s often the prelude to more malicious actions. Let’s see if we can find out what else landed on Noel’s laptop."
> 
> Did any additional files end up on Noel’s laptop after the attacker extracted frosty.zip?
> 
> what was the first file that was created after extraction? 

Solution

```sql
let BOETIE_DATA = Employees
    | where username contains "boetie"
    | project ip_addr, username, hostname
;
let TIMEWINDOW = ProcessEvents
    | where hostname in (BOETIE_DATA | project hostname)
    | where process_commandline contains "frosty.zip"
    | summarize maxTimestamp = max(timestamp)
;
FileCreationEvents
    | where hostname in (BOETIE_DATA | project hostname)
    | where timestamp >= toscalar(TIMEWINDOW | project maxTimestamp)
```

```
sqlwriter.exe
```

#### Question 11

> In the previous question, we discovered that two files, sqlwriter.exe and frost.dll, were downloaded onto Noel’s laptop. Immediately after, a registry key was added that ensures sqlwriter.exe will run every time Noel’s computer boots.
> 
> This persistence mechanism indicates the attacker’s intent to maintain long-term control over the system.
> 
> Eve Snowshoes, "Adding a registry key for persistence is a classic move by attackers to ensure their malicious software runs automatically. It’s crucial to understand how this persistence is set up to prevent further damage."
> 
> What is the name of the property assigned to the new registry key?

Solution

```sql
let BOETIE_DATA = Employees
    | where username contains "boetie"
    | project ip_addr, username, hostname
;
let TIMEWINDOW = ProcessEvents
    | where hostname in (BOETIE_DATA | project hostname)
    | where process_commandline contains "frosty.zip"
    | summarize maxTimestamp = max(timestamp)
;
let FILECREATEDWINDOW = FileCreationEvents
    | where hostname in (BOETIE_DATA | project hostname)
    | where timestamp >= toscalar(TIMEWINDOW | project maxTimestamp)
    | take 1
    | project timestamp
;
ProcessEvents
    | where hostname in (BOETIE_DATA | project hostname)
    | where timestamp >= toscalar(FILECREATEDWINDOW | project timestamp)
```

```
frosty
```

#### Question 12

> Congratulations! You've successfully identified the threat actor's tactics. The attacker gained access to WebApp-ElvesWorkshop from the IP address 182.56.23.122, dumped credentials, and used those to send phishing emails internally to Noel.
> 
> The malware family they used is called Wineloader, which employs a technique known as DLL sideloading. This technique works by placing a malicious DLL in the same directory as a legitimate executable (in this case, sqlwriter.exe).
> 
> When Windows tries to load a referenced DLL without a full path, it checks the executable's current directory first, causing the malicious DLL to load automatically. Additionally, the attacker created a scheduled task to ensure sqlwriter.exe runs on system boot, allowing the malicious DLL to maintain persistence on the system.
> 
> To obtain your FINAL flag use the KQL below with your last answer! 

Solution

```sql
let finalflag = "frosty";
let base64_encoded = base64_encode_tostring(finalflag);
print base64_encoded
```

```
ZnJvc3R5
```

#### Flag

The flag is the last question answered. Thus, ```ZnJvc3R5``` is the flag.