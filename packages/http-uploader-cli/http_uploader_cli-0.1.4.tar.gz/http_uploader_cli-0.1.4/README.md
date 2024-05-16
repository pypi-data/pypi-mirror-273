### Http Uploader CLI

#### Dependencies
- aiohttp
- aiofiles
- aiomultiprocess

|Parameter|Description|
|:--------|-----------|
|--input-file [path-to-file]|Path to txt file to read|
|--url [url]|Service url to send POST|
|--filter [a.b.c == [value]]|Filter to handle JSONs (default: None)|
|--n-lines [num]|Number of lines to send (default: all)|
|--cpus [num]|Processes to use for reading file (default: 4)|
|--coroutines [num]|Requests amount to send (default: send all from 1 request)|

#### Example
```shell
$ python -m http_uploader --input-file ./tests/integration/data/test_jsons.txt --filter 'd == "ddd"' --url https://httpbin.org/post
+------------+------------+---------------+---------------+
| Sent lines | Sent bytes | Skipped lines | Skipped bytes |
+------------+------------+---------------+---------------+
|     4      |    204     |       0       |       0       |
+------------+------------+---------------+---------------+
```
