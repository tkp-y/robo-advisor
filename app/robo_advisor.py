# this is the "app/robo_advisor.py" file


import requests
import json
import csv
import os

#to convert numbers to price format
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71


request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
response = requests.get(request_url)



parsed_response = json.loads(response.text)

tsd = parsed_response["Time Series (Daily)"]

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

dates = list(tsd.keys()) #sort to ensure latest day is first
latest_day = dates[0]

latest_close = parsed_response["Time Series (Daily)"][latest_day]["4. close"]

high_prices = []
low_prices = []

#maximum of all high prices
for date in dates:
    high_price = float(tsd[date]["2. high"])
    low_price = float(tsd[date]["3. low"])
    high_prices.append(high_price)
    low_prices.append(low_price)



recent_high = max(high_prices)
recent_low = min(low_prices)



#write to CSV
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

with open(csv_file_path, "w") as csv_file:
    writer.DictWrite(csv_file, filednames = ["city", "name"])

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: " + last_refreshed)
print("LATEST CLOSE: " + to_usd(float(latest_close)))
print("RECENT HIGH: " + to_usd(float(recent_high)))
print("RECENT LOW: " + to_usd(float(recent_low)))
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("WRITING DATA TO CSV: " + csv_file_path)
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

