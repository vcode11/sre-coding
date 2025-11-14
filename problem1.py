"""
You are given a file (files.txt) where each line represents a file entry 
with its path, size in bytes, and last modified timestamp (Unix epoch). T
he format is comma-separated: filepath,size,modified_timestamp.

Write a Python script that reads this file and calculates the total size 
of files for each file extension type (e.g., .log, .csv, .xml, .pdf, .zip). 
Ignore files with no extension.

Example:
/var/log/app.log,10240,1678886400
/home/user/data.csv,51200,1678886460
/etc/config.xml,1024,1678800000
/var/log/kernel.log,20480,1678890000
/home/user/report.pdf,204800,1678886520
/home/user/archive.zip,1024000,1678790000
/var/log/sys.log,15360,1678890060
"""
import logging
from collections import defaultdict
logger = logging.Logger(__name__)
try:
    with open("./file1.txt") as f:
        sizes_map = defaultdict(int)
        for line in f:
            try:
                filename, size, ts = line.split(",")
                names = filename.split('.')
                if len(names) < 2:
                    continue
                sizes_map[names[-1]]+= int(size)
            except Exception as e:
                logger.warning(f"Couldn't parse {line}")
                continue
except FileNotFoundError:
    logger.error(f"File doesn't exist")
except Exception as e:
    logger.error(f"Couldn't open the file due to {e}")

data = [(size, filetype) for filetype, size in sizes_map.items()]
data.sort(reverse=True)

print("---Sizes per extension are ---")
for size, filetype in data:
    print(f"{filetype} {size}")