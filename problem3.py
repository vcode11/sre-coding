"""
Problem: You have a CSV file (stock_data.csv) containing daily stock price information.
 The columns are: Date, Ticker, Open, High, Low, Close, Volume.

Date,Ticker,Open,High,Low,Close,Volume
2025-04-18,AAPL,170.50,172.80,170.10,172.50,55000000
2025-04-18,GOOG,140.10,141.50,139.80,141.20,25000000
2025-04-21,AAPL,172.60,173.50,171.90,173.00,48000000
2025-04-21,GOOG,141.30,142.00,140.50,140.80,22000000
2025-04-22,AAPL,173.10,175.00,172.80,174.90,61000000
2025-04-22,GOOG,140.90,141.20,139.50,139.90,28000000

Task: Write a Python script that reads this file and performs the following for a specific stock ticker (e.g., AAPL):
Calculate the daily price range (High - Low) for each day the ticker appears.
Find the date with the largest price range for that ticker.
Calculate the average trading volume for that ticker over the period present in the file.
Output: Print the date with the largest range and the calculated average volume for the specified ticker.

Example Output (for AAPL):

Ticker: AAPL
Date with largest price range: 2025-04-22 (Range: $2.20)
Average daily volume: 54666666.67

"""
import csv
from dataclasses import dataclass
from collections import defaultdict
import sys

@dataclass 
class VolumeData:
    volume: int
    days: int

    def avg(self) -> float:
        return self.volume / self.days

@dataclass
class DatePriceRange:
    date: str
    price_range: float 

with open("./stock_data.csv") as f:
    volume_data = defaultdict(lambda : VolumeData(0, 0))
    price_range_data = {}
    csv_reader = csv.DictReader(f)
    for i, row in enumerate(csv_reader):
        if i == 0:
            continue
        ticker = row['Ticker']
        date = row['Date']
        price_range = float(row['High']) - float(row['Low'])
        volume_data[ticker].volume += int(row["Volume"])
        volume_data[ticker].days += 1
        if not price_range_data.get(ticker):
            price_range_data[ticker] = DatePriceRange(
                date=date, 
                price_range=price_range
            )
        if price_range > price_range_data[ticker].price_range:
            price_range_data[ticker].price_range = price_range
            price_range_data[ticker].date = date

ticker = input().strip().upper()
if ticker not in volume_data:
    print("Ticker not found")
    sys.exit(1)
print(ticker)
print(f"Average volume for {ticker} is {volume_data[ticker].avg()}")
print(
      f"Max price range for {ticker} is"
      f"{price_range_data[ticker].price_range}" 
      f" on {price_range_data[ticker].date}"
    )