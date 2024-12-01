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










------------- BELOW ARE NOTES ------------






As always when approacing files I haven't seen before, run the file through ```file``` command:

```bash
file SantaSwipeSecure.aab
    SantaSwipeSecure.aab: Zip archive data, at least v0.0 to extract, compression method=deflate
```

Unpacking it:

```bash
unzip SantaSwipeSecure.aab -d SantaSwipeSecure
```

See if I still can find a reference to the ```naughty``` list: 

```bash
grep -Rni naughty *

grep: base/dex/classes.dex: binary file matches
base/assets/index.html:85:            <li class="list-group-item list-group-item-danger illumination" onclick="showNaughtyList()">Naughty</li>
base/assets/index.html:94:    <p id="instructions">Swipe right to grant a spot on the Nice List, or swipe left to send them straight to the Naughty List.</p>
base/assets/index.html:140:            Android.addToNaughtyList(item.textContent); // Call Android interface to add to Naughty List
base/assets/index.html:166:    function showNaughtyList() {
base/assets/index.html:167:        Android.getNaughtyList();
base/assets/index.html:168:        document.getElementById('header').innerHTML = '<h2 class="illumination">Naughty</h2>';
```

Well yeah - kinda. Found the ```base/dex/classes.dex``` file interesting. For this stunt I will use ```jadx``` (skipping notes on installing Jadx):

```bash
mkdir ~/HHC/DEX
cp base/dex/classes.dex ~/HHC/DEX/
cd ~/HHC/DEX/
jadx -d ~/HHC/DEX/out ~/HHC/DEX/classes.dex
```

Finding references to ```naughty```:

```bash
grep -Rni naughty out

...
out/sources/com/northpole/santaswipe/DatabaseHelper.java:55:        db.execSQL("CREATE TABLE IF NOT EXISTS NaughtyList (Item TEXT);");
...
```


------

Bundletool route: 

````bash
wget https://github.com/google/bundletool/releases/download/1.17.2/bundletool-all-1.17.2.jar
java -jar bundletool-all-1.17.2.jar build-apks --bundle=SantaSwipeSecure.aab --output=output.apks --mode universal
unzip output.apks -d output
apktool d output/universal.apk
strings -n 15 smali/com/northpole/santaswipe/DatabaseHelper.smali | grep "const-string v2" | sed 's/^[^,]*, //; s/"//g'
strings smali/com/northpole/santaswipe/DatabaseHelper.smali > smali/com/northpole/santaswipe/DatabaseHelper.readable
```








Google the crap out of it to find a decent decompiler. Landed on ```BundleDecompiler```:

```bash
git clone git clone https://github.com/TamilanPeriyasamy/BundleDecompiler.git
```

Decompiling the AAB:

```

```

### Gold
