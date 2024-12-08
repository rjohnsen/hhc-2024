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

```
DroneDataAnalystExpertMedal
```

Heading back into the web app, I submitted this password from the "Admin Console" endpoint:

![Found text](/images/act2/act2-drone-path-13.png)

### Gold