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
| distinct ip_addr;
```

> This saves the result of the query into a variable. Now, you can use that result easily in another query:

```sql
OutboundNetworkEvents  
| where src_ip in (twinkle_ips)  
| distinct <field>
````

How many distinct URLs did elves with the first name Twinkle visit?

```sql
let twinkle_ips =
    Employees
    | where name has "twinkle"
    | distinct ip_addr;
OutboundNetworkEvents  
    | where src_ip in (twinkle_ips)  
    | distinct url
    | summarize count()
```

Answer: 8

### Section 2: Operation Surrender: Alabaster's Espionage

### Section 3: Operation Snowfall: Team Wombley's Ransomware Raid

### Section 4: Echoes in the Frost: Tracking the Unknown Threat