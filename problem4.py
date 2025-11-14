"""
You are given a sample Nginx access log file (access.log). 
The format is the standard combined log format.

192.168.1.101 - - [21/Apr/2025:10:05:15 +0100] "GET /index.html HTTP/1.1" 200 512 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
192.168.1.102 - - [21/Apr/2025:10:05:20 +0100] "GET /styles/main.css HTTP/1.1" 200 1024 "http://example.com/index.html" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
192.168.1.101 - - [21/Apr/2025:10:05:21 +0100] "GET /images/logo.png HTTP/1.1" 200 2048 "http://example.com/index.html" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
192.168.1.103 - - [21/Apr/2025:10:06:05 +0100] "GET /products/item1 HTTP/1.1" 200 1800 "-" "Chrome/110.0.0.0"
192.168.1.104 - - [21/Apr/2025:10:06:30 +0100] "GET /nonexistentpage HTTP/1.1" 404 150 "-" "Firefox/109.0"
192.168.1.101 - - [21/Apr/2025:10:07:00 +0100] "POST /api/submit HTTP/1.1" 201 50 "http://example.com/form.html" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
192.168.1.102 - - [21/Apr/2025:10:07:15 +0100] "GET /index.html HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"

Task: Write a Python script to parse this log file and determine:
The count of each HTTP status code (e.g., 200, 404, 304, 201).
The top 3 most requested resource paths (the part between the HTTP method 
and the HTTP version, e.g., /index.html, /styles/main.css). Ignore query parameters if present.
Output: Print the status code counts and the top 3 requested paths with their counts.
Example Output:

Status Code Counts:
200: 3
404: 1
201: 1
304: 1

Top 3 Requested Paths:
/index.html: 2
/styles/main.css: 1
/images/logo.png: 1

"""
from dataclasses import dataclass
import re
from typing import Optional
from collections import Counter

http_regex = re.compile(r"([^\s]+)(?:[^\"]+)(?:\"GET|POST|PUT|DELETE)\s+([^\s]+)(?:[^\"]+)(?:[^\d]+)\s+(\d+)")

@dataclass
class HttpData:
    ip: str
    path: str
    status_code: int


def get_http_data_from_log(line: str) -> Optional[HttpData]:
    mo = http_regex.match(line)
    if mo is None:
        return None
    if len(mo.groups()) != 3:
        print(mo.groups())
        return None
    ip, path, status_code = (
        mo.groups()[0], 
        mo.groups()[1], 
        int(mo.groups()[2])
    )
    return HttpData(ip, path, status_code)

with open("./access.log") as f:
    status_codes = Counter()
    paths = Counter()
    ips = Counter()
    for line in f:
        line = line.strip()
        data = get_http_data_from_log(line.strip())
        if not data:
            print(f"Failed to parse {line}")
            continue
        status_codes[data.status_code]+=1
        paths[data.path]+=1
        ips[data.ip]+=1

print("Status Codes")
for k, v in status_codes.items():
    print(k, v, sep=" Count: ")

print("\nTop 3 requested paths")
for k, v in paths.most_common(3):
    print(k, v, sep=" Count: ")

print("\nTop 3 ip(s)")
for k, v in ips.most_common(3):
    print(k, v, sep=" Count: ")
        
        
