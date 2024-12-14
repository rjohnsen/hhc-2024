+++
title = 'Santa Vision'
date = 2024-12-14T14:53:58+01:00
draft = true
+++

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

### Santa vision A

> What username logs you into the SantaVision portal?

```bash
nmap -sS  34.67.56.14 -p 1-65535
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

#### Web page on port 8000

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

### Santa vision B

> Once logged on, authenticate further without using Wombley's or Alabaster's accounts to see the northpolefeeds on the monitors. What username worked here?

Clicking on the "List Available Clients" button, I got this output:

```json
Available clients: 'elfmonitor', 'WomblyC', 'AlabasterS'
```

Clicking on the "List Available Roles" button, I got this output:
```json
Available roles: 'SiteDefaultPasswordRole', 'SiteElfMonitorRole', 'SiteAlabsterSAdminRole', 'SiteWomblyCAdminRole'
```

In order to find the answer I tried to make a connection using MQTTX, trying various combination until landing: 

Answer:

```
elfmonitor:SiteElfMonitorRole
```

### Santa vision C

> Using the information available to you in the SantaVision platform, subscribe to the frostbitfeed MQTT topic. Are there any other feeds available? What is the code name for the elves' secret operation?


From Santafeed: 
```bash
Topic: santafeedQoS: 0
Sixteen elves launched operation: Idemcerybu
```

```
Idemcerybu
```

### Santa vision D

> There are too many admins. Demote Wombley and Alabaster with a single MQTT message to correct the northpolefeeds feed. What type of contraption do you see Santa on?


/api/v1/frostbitadmin/bot/<botuuid>/deactivate, authHeader: X-API-Key, status: Invalid Key, alert: Warning, recipient: Wombley

superAdminMode=true
