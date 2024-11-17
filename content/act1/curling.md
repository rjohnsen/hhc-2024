+++
title = 'Curling'
date = 2024-11-17T14:18:57+01:00
draft = true
weight = 1
+++


## Objective 
> Team up with Bow Ninecandle to send web requests from the command line using Curl, learning how to interact directly with web servers and retrieve information like a pro!

## Solution

### Easy mode

#### Assignment 1

> 1) Unlike the defined standards of a curling sheet, embedded devices often have web servers on non-standard ports.  Use curl to retrieve the web page on host "curlingfun" port 8080.
> If you need help, run the 'hint' command.

```bash
curl http:/curlingfun:8080
```

![Curling 1](/images/act1/curling-1.png)

#### Assignment 2 

> 2) Embedded devices often use self-signed certificates, where your browser will not trust the certificate presented.  Use curl to retrieve the TLS-protected web page at https://curlingfun:9090/

```bash
curl --insecure https://curlingfun:9090
```

![Curling 2](/images/act1/curling-2.png)

#### Assignment 3

> 3) Working with APIs and embedded devices often requires making HTTP POST requests. Use curl to send a request to https://curlingfun:9090/ with the parameter "skip" set to the value "alabaster", declaring Alabaster as the team captain.

```bash
curl --insecure https://curlingfun:9090 -X POST -d "skip=alabaster"
```

![Curling 3](/images/act1/curling-3.png)

#### Assignment 4

> 4) Working with APIs and embedded devices often requires maintaining session state by passing a cookie.  Use curl to send a request to https://curlingfun:9090/ with a cookie called "end" with the value "3", indicating we're on the third end of the curling match.

```bash
curl --insecure --cookie "end=3" https://curlingfun:9090/
```
![Curling 4](/images/act1/curling-4.png)

#### Assignment 5

> 5) Working with APIs and embedded devices sometimes requires working with raw HTTP headers.  Use curl to view the HTTP headers returned by a request to https://curlingfun:9090/

```bash
curl --insecure --head https://curlingfun:9090/
```

![Curling 5](/images/act1/curling-5.png)

#### Assignment 6

> 6) Working with APIs and embedded devices sometimes requires working with custom HTTP headers.  Use curl to send a request to https://curlingfun:9090/ with an HTTP header called "Stone" and the value "Granite".

```bash
curl --insecure --header "Stone: Granite" https://curlingfun:9090/
```

![Curling 6](/images/act1/curling-6.png)

#### Assignment 7

> 7) curl will modify your URL unless you tell it not to.  For example, use curl to retrieve the following URL containing special characters: https://curlingfun:9090/../../etc/hacks

```bash
curl --insecure --path-as-is "https://curlingfun:9090/../../etc/hacks"
```

![Curling 7](/images/act1/curling-7.png)

#### Last assignment 

![Curling 8](/images/act1/curling-8.png)

### Hard mode

Hard mode hints and assignment is placed in a text file (_HARD-MODE.txt_) on disk: 

```bash
ls
HARD-MODE.txt  HELP
```

#### Assignment 1

Content is of _HARD-MODE.txt_ is:

> Prefer to skip ahead without guidance?  Use curl to craft a request meeting these requirements:
> 
> - HTTP POST request to https://curlingfun:9090/
> - Parameter "skip" set to "bow"
> - Cookie "end" set to "10"
> - Header "Hack" set to "12ft"

![Curling 9 ](/images/act1/curling-9.png)

Command to solve this assignment:

```bash
curl --insecure https://curlingfun:9090/ -X POST -d "skip=bow" --cookie "end=10" --header "Hack: 12ft"
```

![Curling 10 ](/images/act1/curling-10.png)

#### Assignment 2

> Excellent!  Now, use curl to access this URL: https://curlingfun:9090/../../etc/button

Command to solve this assignment:

```bash
curl --insecure https://curlingfun:9090/../../etc/button -X POST -d "skip=bow" --cookie "end=10" --header "Hack: 12ft" --path-as-is
```

![Curling 11](/images/act1/curling-11.png)

#### Assignment 3

Command to solve this assignment:

```bash
curl --insecure https://curlingfun:9090/GoodSportsmanship -X POST -d "skip=bow" --cookie "end=10" --header "Hack: 12ft" --path-as-is -L
```

![Curling 12](/images/act1/curling-12.png)

