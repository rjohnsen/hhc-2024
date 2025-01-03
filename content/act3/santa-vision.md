+++
title = 'Santa Vision'
date = 2024-12-14T14:53:58+01:00
draft = true
weight = 2
+++

## Objective

> Alabaster and Wombley have poisoned the Santa Vision feeds! Knock them out to restore everyone back to their regularly scheduled programming.

## Hints

| From | Hint |
| ---- | ---- |
| Ribb Bonbowford | jefferson is great for analyzing JFFS2 file systems. |
| Ribb Bonbowford | See if any credentials you find allow you to subscribe to any MQTT feeds. |
| Ribb Bonbowford | Consider checking any database files for credentials... |

In addition, there were some interesting hints in the conversation with Ribb Bonbowford: 

> Hi, Ribb Bonbowford here, ready to guide you through the SantaVision dilemma!
> 
> The Santa Broadcast Network (SBN) has been hijacked by Wombley's goons—they're using it to spread propaganda and recruit elves! And Alabaster joined in out of necessity. Quite the predicament, isn’t it?
> 
> To access this challenge, use this terminal to access your own instance of the SantaVision infrastructure.
> 
> Once it's done baking, you'll see an IP address that you'll need to scan for listening services.
>
> Our target is the technology behind the SBN. We need make a key change to its configuration.
> 
> We’ve got to remove their ability to use their admin privileges. This is a delicate maneuver—are you ready?
>
> We need to change the application so that multiple administrators are not permitted. A misstep could cause major issues, so precision is key.
> 
> Once that’s done, positive, cooperative images will return to the broadcast. The holiday spirit must prevail!
>
> This means connecting to the network and pinpointing the right accounts. Don’t worry, we'll get through this.
> 
> Let’s ensure the broadcast promotes unity among the elves. They deserve to see the season’s spirit, don't you think?
> 
> Remember, it’s about cooperation and togetherness. Let's restore that and bring back the holiday cheer. Best of luck!
> 
> The first step to unraveling this mess is gaining access to the SantaVision portal. You'll need the right credentials to slip through the front door—what username will get you in?

## Solution

### Silver

#### Santa vision A

> What username logs you into the SantaVision portal?

The very first thing I did was to portscan the given IP to learn more what my next steps should be: 

```bash
nmap -sS 34.72.28.246 -p 1-65535
```

These were the ports I found: 


| PORT      | STATE    | SERVICE     | 
| --------- | -------- | ----------- | 
| 22/tcp    | open     | ssh         |
| 25/tcp    | filtered | smtp        |
| 1883/tcp  | open     | mqtt        |
| 5355/tcp  | filtered | llmnr       |
| 8000/tcp  | open     | http-alt    |
| 9001/tcp  | open     | tor-orport  |
| 18290/tcp | filtered | unknown     |
| 48328/tcp | filtered | unknown     |

Inspecting the HTML code on the landing page ```34.67.56.14:8000``` I found what seemed like a ```mqtt``` credential:

```html
<div class="footer" id="footer">
  <b>©2024 Santavision Elventech Co., Ltd. Snow Rights Reserved.<br>(<i>topic 'sitestatus'</i> available.)</b>
</div> <!-- mqtt: elfanon:elfanon -->

      </div>
    </div>
    <!-- scripts -->
    <script src="https://code.jquery.com/jquery-3.6.1.min.js" type="text/javascript"></script>
    <!-- JavaScript Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous"></script>
    
  </body>
</html>
```

**Answer:**

```
elfanon:elfanon
```

Logging in:

![Login](/images/act3/act3-santa-vision-1.png)

#### Santa vision B

> Once logged on, authenticate further without using Wombley's or Alabaster's accounts to see the northpolefeeds on the monitors. What username worked here?

When logged in, I was greeted with this dashboard: 

![Logged in](/images/act3/act3-santa-vision-11.png)

Clicking on the "List Available Clients" button, I got this output:

```
Available clients: 'elfmonitor', 'WomblyC', 'AlabasterS'
```

Clicking on the "List Available Roles" button, I got this output:

```
Available roles: 'SiteDefaultPasswordRole', 'SiteElfMonitorRole', 'SiteAlabsterSAdminRole', 'SiteWomblyCAdminRole'
```

**Answer:**

In order to find the answer I tried to make a connection using MQTTX using the options in the dashboard, trying various combination of roles until landing on:

```
elfmonitor:SiteElfMonitorRole
```

Turning on the monitors:

![Login](/images/act3/act3-santa-vision-2.png)

#### Santa vision C

> Using the information available to you in the SantaVision platform, subscribe to the frostbitfeed MQTT topic. Are there any other feeds available? What is the code name for the elves' secret operation?

By connecting to the feed I saw an reference to "santafeed". Trying my luck I downloaded a MQTT client (MQTTX) and connected to the Santafeed:

![Connecting](/images/act3/act3-santa-vision-3.png)

Finding the name of the secret operation in the "santafeed":

![Findind the name of the secret operation](/images/act3/act3-santa-vision-4.png)

From Santafeed: 

```bash
Sixteen elves launched operation: Idemcerybu
```

**Answer:**

From this message the name of the secret operation is:

```
Idemcerybu
```

#### Santa vision D

> There are too many admins. Demote Wombley and Alabaster with a single MQTT message to correct the northpolefeeds feed. What type of contraption do you see Santa on?

During this assignment I found several feeds.
* frostbitfeed
* northpolefeeds
* santafeed

Nesting together the hints from the GUI and MQTT messages, I found out the message format I should send: 

```html
singleAdminMode=true&role=SiteElfMonitorRole&user=WombleyC
```

Using the web dashboard I sent this as plaintext to Santafeed, and then paid attention to the monitors as they changed:

![Findind the name of the secret operation](/images/act3/act3-santa-vision-5.png)


**Answer:**

```
pogo stick
```

### Gold

#### Santa vision A

> What username logs you into the SantaVision portal?

I found a new topic by using BurpSuite navigating to the logon form site:

* sitestatus

By listening in on the logon process using BurpSuite I found a direct link for login:

```
<p>You should be redirected automatically to the target URL: <a href="/auth?id=viewer&amp;loginName=elfanon">/auth?id=viewer&amp;loginName=elfanon</a>. If not, click the link.
```

Investigating further on the ```sitestatus``` feed I found an interesting download:

![Interesting download](/images/act3/act3-santa-vision-6.png)

```
/static/sv-application-2024-SuperTopSecret-9265193/applicationDefault.bin
```

Using Kali, I downloaded the file: 

```bash
wget http://34.72.28.246:8000/static/sv-application-2024-SuperTopSecret-9265193/applicationDefault.bin
```

Investigating what it was:

```bash
file applicationDefault.bin
    applicationDefault.bin: Linux jffs2 filesystem data little endian
```

According to the hints, Jefferson could be used to treat this file (including here the instruction setting it up):

```bash
python3 -m venv env
source env/bin/activate
pip install -U pip
pip install jefferson
```

Using Jefferson, extracting results to folder "out":

```bash
jefferson -d out applicationDefault.bin
```


In file ```out/app/src/accounts/views.py``` I found a reference to a SQLite database:

```python
@accounts_bp.route("/static/sv-application-2024-SuperTopSecret-9265193/applicationDefault.bin", methods=["GET"])
def firmware():
    return send_from_directory("static", "sv-application-2024-SuperTopSecret-9265193/applicationDefault.bin", as_attachment=True)

@accounts_bp.route("/sv2024DB-Santa/SantasTopSecretDB-2024-Z.sqlite", methods=["GET"])
def db():
    return send_from_directory("static", "sv2024DB-Santa/SantasTopSecretDB-2024-Z.sqlite", as_attachment=True)
```

Downloading the SQLite database: 

```bash
wget http://34.72.28.246:8000/sv2024DB-Santa/SantasTopSecretDB-2024-Z.sqlite
```

Opened it up in ```sqlitebrowser``` and found a user table: 

![User table](/images/act3/act3-santa-vision-7.png)

**Answer:** 

The credentials for gold in A is: 

```
santaSiteAdmin:S4n+4sr3411yC00Lp455wd
```

I also found a reference to another user in the codebase: 

```python
core/views.py:54:        mqttPublish.single("$CONTROL/dynamic-security/v1","{\"commands\":[{\"command\": \"deleteClient\",\"username\": \""+name+"\"}]}",hostname="localhost",port=1883,auth={'username':"SantaBrokerAdmin", 'password':"8r0k3R4d1mp455wD"})
```

#### Santa vision B

> Once logged on, authenticate further without using Wombley's or Alabaster's accounts to see the northpolefeeds on the monitors. What username worked here?

While inspecting the HTTPS headers for the monitoring GUI, I found something interesting for call 

```
http://34.30.225.171:8000/auth?id=viewer&loginName=santaSiteAdmin
```

It appears that there's some credentials hidden in the response headers:

![Hidden username in headers](/images/act3/act3-santa-vision-8.png)

**Answer:**

```
santashelper2024:playerSantaHelperPass7183926777
```

Note: the password changes whenever the environment is reset ... Thus, any references to this password from hereon may be somewhat off due to this.

#### Santa vision C

> Using the information available to you in the SantaVision platform, subscribe to the frostbitfeed MQTT topic. Are there any other feeds available? What is the code name for the elves' secret operation?

Taking the answer for Silver C, "Idemcerybu" I asked ChatGPT what on earth this could be. It answered it was most likely ROT13. So I asked it to loop through every positions, ending up with a shift of 11. 

**Answer:** Snowmobile

#### Santa vision D

> There are too many admins. Demote Wombley and Alabaster with a single MQTT message to correct the northpolefeeds feed. What type of contraption do you see Santa on?

**Answer:** Hovercraft

In order to solve this I had to send the same message as in Silver D, but by using a client instead of the website: 

![Sending request using MQTTX](/images/act3/act3-santa-vision-9.png)

By obsering the monitors I now see what kind of vehicle santa is using: 

![Hovercraft](/images/act3/act3-santa-vision-10.png)

**Answer:** Hovercraft
