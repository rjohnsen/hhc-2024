+++
title = 'Elf Frostbit Decrypt'
date = 2024-12-14T14:54:19+01:00
draft = true
+++

## Objective

> Decrypt the Frostbit-encrypted Naughty-Nice list and submit the first and last name of the child at number 440 in the Naughty-Nice list.

## IOC's

### IOC's from frostbit_core_dump.13

#### Endpoints

```bash
strings frostbit_core_dump.13 | grep http
    https://api.frostbit.app/view/Fgcse2IEk5zg3BhQhlL/15d977db-9fa9-48f8-be38-d36c2e21b12d/status?digest=0081c004828085c081a0e424db82a0a0
    https://api.frostbit.app/api/v1/bot/15d977db-9fa9-48f8-be38-d36c2e21b12d/session
    https://api.frostbit.app/api/v1/bot/15d977db-9fa9-48f8-be38-d36c2e21b12d/keyit
```

##### Ransomware note

```html
https://api.frostbit.app/view/Fgcse2IEk5zg3BhQhlL/15d977db-9fa9-48f8-be38-d36c2e21b12d/status?digest=0081c004828085c081a0e424db82a0a0
```

![Ransomeware note](/images/act3/act3-frostbit-decrypt-1.png)

Links in screenshot verified to not be working.

##### Nonce

```html
https://api.frostbit.app/api/v1/bot/15d977db-9fa9-48f8-be38-d36c2e21b12d/session
    
    {
        "nonce": "e998a50d979ee2d7"
    }
```

##### Invalid API Path

```html
https://api.frostbit.app/api/v1/bot/15d977db-9fa9-48f8-be38-d36c2e21b12d/keyit
    {
        "error": "Invalid API Path"
    }
```

#### Encrypted key JSON

```bash
strings frostbit_core_dump.13 -n 10 | grep -i nonce
```

Output:

```json
{"encryptedkey":"2ea5d786947ab4dbc462dc0d1fe878b07f46df032f17b43aeeedea7a2683996377d3b57cc2f94781deef9f81e966309e09e26577d5110836c4236b8dc3bec734ed0060168b30530b99d66cb4d33d9e87712dd71fb8ab6d311430b55743994400e9eb452a378a6c930225f69f46bdef91581a6325b4e873458d4fc9287a2f4af7bbc68a6f3db16b1e463982a815b2fc291b1013e880a2a8f077c1fed52a7673ec1bfc7a4bb6edba03ab670332fa3627f20116f6ceeed97a757bb220494cd696e8f5f05869b6f57f5aef18e204c7213d634b56fae8751b7521d86eb5f7d692313398ff70cded16d5eddef0ec655e7a5279d97a15d1c8efa8aac1c4b0073657007a96e34eeeaae9460629ae9ce5d219d512afef28736e6844f297c02e6cf992e36de5fdc8e0f79b71e92a3ecac6c1b703c84ecd7ca8deb52061441d0c30e3c8be30f3a8658be84a26bf7e7ce3d5b4637da157f7e87795fcfecc8411532ad0cc7c6a8a4de2861c2df429507f1909928cb735b4e3758c139b865e0b2ffceac950880219bdf644e6dca7545c03bff09194624a8fbb0ea54ee6ee3caf4749ca2165873b02e46548be0bbffea92cad7bd89606ed3f1f157d4fedc393007de842ab1e17e23f6fb4b4b963f328f1b55bf2fbe1ad57109a4a835308d6dfa0aaf98069bf44f0c8d50fe302205a82c181587d7fab4c1bf562109593a601f7b026e4236f71fc8f","nonce":""}
```

#### Unspecified IOC's

The following IOC's were collected using the following command:

```bash
strings frostbit_core_dump.13 -n50
```

#### Unrecognized JSON 1

```json
{"digest":"10044402b080a8example202088819b8","status":"Key Set","statusid":"ZGTw7qlexampleQNiW"}
{"digest":"0081c004828085c081a0e424db82a0a0","status":"Key Set","statusid":"Fgcse2IEk5zg3BhQhlL"}

```

#### Long HEX text

```hex
2ea5d786947ab4dbc462dc0d1fe878b07f46df032f17b43aeeedea7a2683996377d3b57cc2f94781deef9f81e966309e09e26577d5110836c4236b8dc3bec734ed0060168b30530b99d66cb4d33d9e87712dd71fb8ab6d311430b55743994400e9eb452a378a6c930225f69f46bdef91581a6325b4e873458d4fc9287a2f4af7bbc68a6f3db16b1e463982a815b2fc291b1013e880a2a8f077c1fed52a7673ec1bfc7a4bb6edba03ab670332fa3627f20116f6ceeed97a757bb220494cd696e8f5f05869b6f57f5aef18e204c7213d634b56fae8751b7521d86eb5f7d692313398ff70cded16d5eddef0ec655e7a5279d97a15d1c8efa8aac1c4b0073657007a96e34eeeaae9460629ae9ce5d219d512afef28736e6844f297c02e6cf992e36de5fdc8e0f79b71e92a3ecac6c1b703c84ecd7ca8deb52061441d0c30e3c8be30f3a8658be84a26bf7e7ce3d5b4637da157f7e87795fcfecc8411532ad0cc7c6a8a4de2861c2df429507f1909928cb735b4e3758c139b865e0b2ffceac950880219bdf644e6dca7545c03bff09194624a8fbb0ea54ee6ee3caf4749ca2165873b02e46548be0bbffea92cad7bd89606ed3f1f157d4fedc393007de842ab1e17e23f6fb4b4b963f328f1b55bf2fbe1ad57109a4a835308d6dfa0aaf98069bf44f0c8d50fe302205a82c181587d7fab4c1bf562109593a601f7b026e4236f71fc8f
```

#### Client and Server handshakes and secrets 

```
CLIENT_HANDSHAKE_TRAFFIC_SECRET b628d6ae5a2016185a918875556cb201006357548a301e914aaa9fe2ac7490f7 95d29ae475a8cca66237ae742e80ef054694f1cac76005718eda63098ea1ed54
SERVER_HANDSHAKE_TRAFFIC_SECRET b628d6ae5a2016185a918875556cb201006357548a301e914aaa9fe2ac7490f7 60fad6da7c95990bbdaa9c642d8d7f9babb7da4017a709a00b899176ca431807
CLIENT_TRAFFIC_SECRET_0 b628d6ae5a2016185a918875556cb201006357548a301e914aaa9fe2ac7490f7 3a582c4fb15aa9f10aecdaa72ca7b73ae0dfdd8126dd64aa18b3ab80c3957331
SERVER_TRAFFIC_SECRET_0 b628d6ae5a2016185a918875556cb201006357548a301e914aaa9fe2ac7490f7 784b9c051b6ed71221f367cc790ac1b1c8dd70dd8690c69f01262745bf61cd78
```

{{% notice note %}}
These values when put into a text file and referenced in "(Pre)-Master-Secret log filename", will decode the TLS entries in the associated PCAP.
{{% /notice %}}

#### POST request for key

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