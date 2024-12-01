+++
title = 'Mobile Analysis'
date = 2024-11-23T13:18:24+01:00
draft = true
weight = 1
+++

## Objective

> Help find who has been left out of the naughty AND nice list this Christmas. Please speak with Eve Snowshoes for more information.

## Hints

**Mobile Analysis Easy - Tools**

| From | Objective | Description |
| ---- | --------- | ----------- |
| Eve Snowshoes | Mobile Analysis | Try using apktool or jadx |

**Mobile Analysis Easy - Missing**

| From | Objective | Description |
| ---- | --------- | ----------- |
| Eve Snowshoes | Mobile Analysis | Maybe look for what names are included and work back from that? |

**Mobile Analysis Hard - Format**

| From | Objective | Description |
| ---- | --------- | ----------- |
| Eve Snowshoes | Mobile Analysis | So yeah, have you heard about this new [Android app](https://developer.android.com/guide/app-bundle/app-bundle-format) format? Want to [convert it to an APK](https://github.com/HackJJ/apk-sherlock/blob/main/aab2apk.md) file? |

**Mobile Analysis Hard - Encryption and Obfuscation**

| From | Objective | Description |
| ---- | --------- | ----------- |
| Eve Snowshoes | Mobile Analysis | Obfuscated and encrypted? Hmph. Shame you can't just run strings on the file. |


**Eve Snowshoes conversation**

> Hi there, tech saviour! Eve Snowshoes and Team Alabaster in need of assistance.
> I've been busy creating and testing a modern solution to Santa’s Naughty-Nice List, and I even built an Android app to streamline things for Alabaster’s team.
> But here’s my tiny reindeer-sized problem: I made a [debug](https://www.holidayhackchallenge.com/2024/SantaSwipe.apk) version and a [release](https://www.holidayhackchallenge.com/2024/SantaSwipeSecure.aab) version of the app.
> I accidentally left out a child's name on each version, but for the life of me, I can't remember who!
> Could you start with the debug version first, figure out which child’s name isn’t shown in the list within the app, then we can move on to release? I’d be eternally grateful!

For clarity, I have included the links from Eve Snowshoes in cleartext here: 

* https://www.holidayhackchallenge.com/2024/SantaSwipe.apk
* https://www.holidayhackchallenge.com/2024/SantaSwipeSecure.aab

## Solution



### Silver

#### Getting the necessary files 

First I downloaded the ```aab``` and ```apk``` in Kali Linux:
```bash
wget https://www.holidayhackchallenge.com/2024/SantaSwipeSecure.aab
wget https://www.holidayhackchallenge.com/2024/SantaSwipe.apk
```

#### Investigating APK

Decompiling APK:

```bash
apktool d SantaSwipe.apk
```

The objective hints at there's a "naughty AND nice" list. Let's see where this list could be by just grepping for the word "naughty":

```bash
cd SantaSwipe
grep -Rni "naughty" *
```

In the, not so quite massive, output I found a reference to a database: 

```
smali_classes3/com/northpole/santaswipe/DatabaseHelper.smali:82:    const-string v2, "naughtynicelist.db"
```

Since this is an APK and I highly doubt the database comes with it, I reckoned that there were some insert statements in the ```DatabaseHelper.smali``` file. I found these statements: 

```sql
grep -i insert DatabaseHelper.smali
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Carlos, Madrid, Spain\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Aiko, Tokyo, Japan\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Maria, Rio de Janeiro, Brazil\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Liam, Dublin, Ireland\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Emma, New York, USA\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Chen, Beijing, China\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Fatima, Casablanca, Morocco\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Hans, Berlin, Germany\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Olga, Moscow, Russia\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Ravi, Mumbai, India\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Amelia, Sydney, Australia\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Juan, Buenos Aires, Argentina\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Sofia, Rome, Italy\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Ahmed, Cairo, Egypt\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Yuna, Seoul, South Korea\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Ellie, Alabama, USA\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Lucas, Paris, France\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Mia, Toronto, Canada\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Sara, Stockholm, Sweden\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Ali, Tehran, Iran\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Nina, Lima, Peru\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Anna, Vienna, Austria\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Leo, Helsinki, Finland\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Elena, Athens, Greece\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Davi, Sao Paulo, Brazil\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Marta, Warsaw, Poland\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Noah, Zurich, Switzerland\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Ibrahim, Ankara, Turkey\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Emily, Wellington, New Zealand\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Omar, Oslo, Norway\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Fatou, Dakar, Senegal\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Olivia, Vancouver, Canada\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Ethan, Cape Town, South Africa\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Santiago, Bogota, Colombia\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Isabella, Barcelona, Spain\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Ming, Shanghai, China\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Chloe, Singapore, Singapore\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Mohammed, Dubai, UAE\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Ava, Melbourne, Australia\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Luca, Milan, Italy\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Sakura, Kyoto, Japan\');"
    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Edward, New Jersey, USA\');"
```

Cleaned the output by some ````SED``` magic and stored it a CSV file: 

```bash
grep -i insert DatabaseHelper.smali | sed -E "s/.*'([^']+), ([^,]+), ([^']+)'.*/\1, \2, \3/" | sed 's/\\$//' | sort > apk-list.txt
```

Resulting in this list: 

```csv
Ahmed, Cairo, Egypt
Aiko, Tokyo, Japan
Ali, Tehran, Iran
Amelia, Sydney, Australia
Anna, Vienna, Austria
Ava, Melbourne, Australia
Carlos, Madrid, Spain
Chen, Beijing, China
Chloe, Singapore, Singapore
Davi, Sao Paulo, Brazil
Edward, New Jersey, USA
Elena, Athens, Greece
Ellie, Alabama, USA
Emily, Wellington, New Zealand
Emma, New York, USA
Ethan, Cape Town, South Africa
Fatima, Casablanca, Morocco
Fatou, Dakar, Senegal
Hans, Berlin, Germany
Ibrahim, Ankara, Turkey
Isabella, Barcelona, Spain
Juan, Buenos Aires, Argentina
Leo, Helsinki, Finland
Liam, Dublin, Ireland
Luca, Milan, Italy
Lucas, Paris, France
Maria, Rio de Janeiro, Brazil
Marta, Warsaw, Poland
Mia, Toronto, Canada
Ming, Shanghai, China
Mohammed, Dubai, UAE
Nina, Lima, Peru
Noah, Zurich, Switzerland
Olga, Moscow, Russia
Olivia, Vancouver, Canada
Omar, Oslo, Norway
Ravi, Mumbai, India
Sakura, Kyoto, Japan
Santiago, Bogota, Colombia
Sara, Stockholm, Sweden
Sofia, Rome, Italy
Yuna, Seoul, South Korea
```

#### Investigating AAB

Download the Bundletool from hint: 

```bash
wget https://github.com/google/bundletool/releases/download/1.17.2/bundletool-all-1.17.2.jar
```

Generating a keystore

```bash
keytool -genkey -v -keystore upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```

Running Bundletool

```bash
java -jar bundletool-all-1.17.2.jar build-apks --bundle=SantaSwipeSecure.aab --output=output.apks --mode=universal --ks=upload-keystore.jks --ks-key-alias=upload --ks-pass=pass:jallafisk
```

Collecting APK

```bash
mv output.apks output.zip
unzip output.zip -d output
cd output
```

From this folder I uploaded the extracted APK and loaded it into https://appetize.io/ and ran the APK there. By comparing the list in this APP (screenshot below) I found that the missing kid was ```Ellie```

![Mobile analysis silver](/images/act2/act2-mobile-analysis-silver.png)

### Gold

With the file ```output.apks``` from silver solution, I decompile it using ```apktool```:

```bash
cd universal
apktool d universal.apk
cd universal
```

Now standing inside the decompiled APK, I retry to find a point I can work on:

```bash
grep -Rni naughty *

...
smali/com/northpole/santaswipe/DatabaseHelper.smali
...
```

Inside this file I found several interesting lines, first something that loads "ek" and "iv" from R class as string:

```java
.line 25
sget v0, Lcom/northpole/santaswipe/R$string;->ek:I
...
.line 26
sget v2, Lcom/northpole/santaswipe/R$string;->iv:I
...
.line 335
:try_start_0
const-string v0, "AES/GCM/NoPadding"
```

It appears that we got a decrypt function utilzing "AES/GCM/NoPadding", using "ek" and "iv". In file res/values/strings.xml I found the following interesting values, which seems to correspond well to the above: 

```xml
<string name="ek">rmDJ1wJ7ZtKy3lkLs6X9bZ2Jvpt6jL6YWiDsXtgjkXw=</string>
...
<string name="iv">Q2hlY2tNYXRlcml4</string>
```

And a bunch of Base64 looking strings (which I extracted into a file):

```bash
strings smali/com/northpole/santaswipe/DatabaseHelper.smali | grep "const-string v" | sed 's/^[^,]*, //; s/"//g' > ~/HHC/b64.txt
```

The list looking like this: 

```
I2DF3+Y1t50nWMN2K9MV6Qx+1mbIOp5nPzrOusVi9a3n/50=
O2nb1+t38vJmctBqZpE87xttw59XDIVWsL+jOGYAZSakGQcwH9LkY0MNP74=
Lm3H1K45zb8hQ9R7K9MT/Bpv1toWCeg3YKGO+eApkQGBF09JMw==
JG3E0/o1t5MzX9h6b99wyRB8z9IZOEuf/8PQJ7tJYwF2ZBYDZDY=
MWfO0+M1t58yWdR3dN9wyQdrx9AS/R916miej6pBB+UB54ZZ1g==
...
```

Okay. I have much information. On this point I asked ChatGPT to give me a decryptor for "AES/GCM/NoPadding" in Python, giving it also the EK and IV. With the code it gave me, I made some changes to make it read the hashes from my text file of hases (b64.txt). The code ended up like this: 

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def decrypt_aes_gcm(encrypted_data_b64, key_b64, iv_b64):
    try:
        # Decode the Base64-encoded key, IV, and encrypted data
        key = base64.b64decode(key_b64)
        iv = base64.b64decode(iv_b64)
        encrypted_data = base64.b64decode(encrypted_data_b64)
        
        # Initialize the AES-GCM cipher for decryption
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        
        # Decrypt and verify the data (GCM mode doesn't use explicit padding)
        decrypted_data = cipher.decrypt_and_verify(encrypted_data[:-16], encrypted_data[-16:])
        
        # Return the decrypted string
        return decrypted_data.decode('utf-8')
    
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

key_b64 = "rmDJ1wJ7ZtKy3lkLs6X9bZ2Jvpt6jL6YWiDsXtgjkXw="
iv_b64 = "Q2hlY2tNYXRlcml4"

with open("b64.txt", "r") as infile:
    for line in infile.readlines():
        # Decrypt and print the result
        decrypted_result = decrypt_aes_gcm(line, key_b64, iv_b64)
        print("Decrypted:", decrypted_result)
```

The first run it presented me with this output:

```bash
...
Decrypted: Leila, Algiers, Algeria
Decrypted: Omar, Doha, Qatar
Decrypted: Marie, Luxembourg, Luxembourg
Decrypted: Tom, Los Angeles, USA
Decrypted: Edwards, New Jersey, USA
Decryption failed: Incorrect padding
Decrypted: None
Decryption failed: MAC check failed
Decrypted: None
Decryption failed: Incorrect padding
Decrypted: None
Decryption failed: Incorrect padding
Decrypted: None
Decryption failed: Incorrect padding
Decrypted: None
Decryption failed: Invalid base64-encoded string: number of data characters (41) cannot be 1 more than a multiple of 4
Decrypted: None
Decryption failed: MAC check failed
Decrypted: None
Decrypted: CREATE TRIGGER DeleteIfInsertedSpecificValue
    AFTER INSERT ON NormalList
    FOR EACH ROW
    BEGIN
        DELETE FROM NormalList WHERE Item = 'KGfb0vd4u/4EWMN0bp035hRjjpMiL4NQurjgHIQHNaRaDnIYbKQ9JusGaa1aAkGEVV8=';
    END;
```

Clearly the list isn't exactly properly cleaned. Anyhow, it appears there's an encrypted value in the DELETE statement at the very end. I simply copied that encrypted value into my "b64.txt" file and re-ran my Python script, which gave me the following output:

```bash
...
Decrypted: CREATE TRIGGER DeleteIfInsertedSpecificValue
    AFTER INSERT ON NormalList
    FOR EACH ROW
    BEGIN
        DELETE FROM NormalList WHERE Item = 'KGfb0vd4u/4EWMN0bp035hRjjpMiL4NQurjgHIQHNaRaDnIYbKQ9JusGaa1aAkGEVV8=';
    END;
Decrypted: Joshua, Birmingham, United Kingdom
```

The answer for gold is ```Joshua```