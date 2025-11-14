"""
You are provided with a trade log file (tradelog.csv) format.
The columns are: date, process, host, log, bytes.
The exchange name (e.g., 'cme', 'lse') is part of the process name string.

tradelog.csv file content:

Also test your code for this unordered column i.e modify the code to parse 
different column order 
eg. (date, process, host, log,bytes) => (process, date, log, bytes, host)

date,process,host,log,bytes
20140206,cme_trader_2,ny-host-01,0345-cme_trader_2.log.gz,1500
20140206,lse_orderrouter_1,ln-host-a,1120-lse_orderrouter_1.log.gz,800
20140206,cme_trader_2,ny-host-01,0346-cme_trader_2.log.gz,500
20140207,cme_feedhandler_1,ny-host-02,0900-cme_feedhandler_1.log.gz,2500
20140207,lse_orderrouter_1,ln-host-b,1305-lse_orderrouter_1.log.gz,1200
20140207,cme_trader_1,ny-host-03,1015-cme_trader_1.log.gz,1800
20140207,lse_feedhandler_1,ln-host-a,1400-lse_feedhandler_1.log.gz,100

Write a Python script to process this log file and calculate:

The total number of bytes processed per day, order by date ascending
The total number of bytes processed per exchange, per day, order by date ascending
"""
from collections import defaultdict
from dataclasses import dataclass
import logging
from typing import List, Optional 

logger = logging.Logger(__name__)

@dataclass
class Fields:
    date: str
    bytes_: int
    exchange: str

def get_fields(columns: List[str], contents: List[str]) -> Optional[Fields]:
    if len(contents) != len(columns):
        return None
    data = dict(zip(columns, contents))
    date = data.get("date")
    if not date:
        return None 
    bytes_ = data.get("bytes")
    if not bytes_:
        return None
    exchange = None
    if process := data.get("process"):
        exchange = process.split("_")[0]
    else:
        return None
    return Fields(date=date, bytes_=int(bytes_), exchange=exchange)

try:
    with open("./tradelog.csv") as f:
        bytes_per_day = defaultdict(int)
        bytes_per_exchange_per_day = defaultdict(int)
        columns = f.readline().strip().split(',')
        for line in f:
            contents = line.strip().split(',')
            field = get_fields(columns=columns, contents=contents)
            if not field:
                logger.warning(
                    f"Couldn't parse skipping:  {contents}"
                )
                continue
            
            date = field.date
            bytes_ = field.bytes_
            exchange = field.exchange
            bytes_per_day[date]+= int(bytes_)
            bytes_per_exchange_per_day[(date, exchange)]+= int(bytes_)
        print("------ Bytes per day --------")
        for k,v in bytes_per_day.items():
            print(k,v)
        
        print("------ Bytes/exchange/day --------")
        for (date, exchange),v in bytes_per_exchange_per_day.items():
            print(date, exchange, v)
except FileNotFoundError:
    logger.error(f"File not found")
except IOError as e:
    logger.error(f"I/O error occurred {e}")
