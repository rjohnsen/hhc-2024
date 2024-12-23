+++
title = 'Elf Frostbit Deactivate'
date = 2024-12-14T14:54:27+01:00
draft = true
weight = 4
+++

## Objective

> Wombley's ransomware server is threatening to publish the Naughty-Nice list. Find a way to deactivate the publication of the Naughty-Nice list by the ransomware server.

## Hints

| From | Hint |
| ---- | ---- |
| Dusty Giftwrap | There must be a way to deactivate the ransomware server's data publication. Perhaps one of the other North Pole assets revealed something that could help us find the deactivation path. If so, we might be able to trick the Frostbit infrastructure into revealing more details. |
| Dusty Giftwrap |  The Frostbit author may have mitigated the use of certain characters, verbs, and simple authentication bypasses, leaving us blind in this case. Therefore, we might need to trick the application into responding differently based on our input and measure its response. If we know the underlying technology used for data storage, we can replicate it locally using Docker containers, allowing us to develop and test techniques and payloads with greater insight into how the application functions. | 

## Solution

### Gold

From other objectives I have already found the deactivation endpoint: 

![Deactivation endpoint](/images/act3/act3-frostbit-decrypt-4.png)

For clarity: 

```
/api/v1/frostbitadmin/bot/<botuuid>/deactivate
```

It appears to requiring "authHeader: X-API-Key" set.

Looking at what HTTP verbs the endpoint support I see: 

![Supported HTTP verbs](/images/act3/act3-frostbit-deactivate-1.png)

* GET
* HEAD
* OPTIONS
