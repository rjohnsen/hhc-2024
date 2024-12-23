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

The tip mentions that the infratructure may reveal something about itself, let's try the debug trick from earlier objectives: 

![Debug mode](/images/act3/act3-frostbit-deactivate-2.png)

For clarity, here's the output: 

```json
{"debug":true,"error":"Timeout or error in query:\nFOR doc IN config\n    FILTER doc.<key_name_omitted> == '{user_supplied_x_api_key}'\n    <other_query_lines_omitted>\n    RETURN doc"}
```

This query language looks like ArangoDB, and ChatGPT think that as well. There's a mention of "user_supplied_x_api_key". Let's see if I can trigger something by manipulating it: 

![Debug mode](/images/act3/act3-frostbit-deactivate-3.png)

For clarity, here's the output: 

```json
{"debug":true,"error":"Invalid Key"}
```

Setting header field: 
```
X-Api-Key: 'OR 1 == 1 //
```

Yields this error: 

```json
{"debug":true,"error":"Request Blocked"}
```

### Overview of keywords allowed or blocked 

It appears that certain keywords are blocked, trying to map them out (according to https://docs.arangodb.com/stable/aql/fundamentals/syntax/):

| Keyword | Blocked | Open |
| ------- | ------- | ---- |
| AGGREGATE |  | X |
| ALL |  | X |
| ALL_SHORTEST_PATHS |  | X |
| AND |  | X |
| ANY |  | X |
| ASC |  | X |
| COLLECT |  | X |
| DESC |  | X |
| DISTINCT |  | X |
| FALSE |  | X |
| FILTER | X |  |
| FOR | X |  |
| GRAPH |  | X |
| IN |  | X |
| INBOUND |  | X |
| INSERT | X |  |
| INTO |  | X |
| K_PATHS |  | X |
| K_SHORTEST_PATHS |  | X |
| LET | X |  |
| LIKE |  | X |
| LIMIT |  | X |
| NONE |  | X |
| NOT |  | X |
| NULL |  | X |
| OR |  | X |
| OUTBOUND |  | X |
| REMOVE |  | X |
| REPLACE |  | X |
| RETURN | X |  |
| SHORTEST_PATH |  | X |
| SORT |  | X |
| TRUE |  | X |
| UPDATE | X |  |
| UPSERT |  | X |
| WINDOW |  | X |
| WITH | X |  |
| FOR | X |  |
| RETURN | X |  |
| FILTER | X |  |
| SEARCH |  | X |
| SORT |  | X |
| LIMIT |  | X |
| LET | X |  |
| COLLECT |  | X |
| WINDOW |  | X |
| INSERT | X |  |
| UPDATE | X |  |
| REPLACE |  | X |
| REMOVE |  | X |
| UPSERT |  | X |
| WITH | X |  |

