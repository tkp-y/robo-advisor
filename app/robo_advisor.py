# this is the "app/robo_advisor.py" file


import requests
import json
import csv
import os
from datetime import datetime



import pandas as pd
import plotly.express as px


#datetime object containing current date and time
now = datetime.now()


from dotenv import load_dotenv
load_dotenv()

#to convert numbers to price format
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
symbol = input("Please enter a stock or cryptocurrency symbol: ")
if symbol.isalpha() == False:
    print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")
    exit()


try:
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol + "&apikey=" + api_key
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


    #for the recommendation 
    #buy the stock if the latest closing price is less than 30% above the recent low
    if float(latest_close) < (float(recent_low) * 1.3):
        recommend = "Buy!"
        reason = "The stocks latest closing price is less than 30% higher than the recent low, which is under the threshold."
    else:
        recommend = "Do not buy!"
        reason = "The stocks latest closing price is more than 30% higher than the recent low, exceeding the threshold."



    #write to CSV
    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
    with open(csv_file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = csv_headers)
        writer.writeheader()
        for date in dates:
            daily_prices = tsd[date]
            writer.writerow({
                "timestamp": date,
                "open": daily_prices["1. open"],
                "high": daily_prices["2. high"],
                "low": daily_prices["3. low"],
                "close": daily_prices["4. close"],
                "volume": daily_prices["5. volume"]

            })

    #line graph
    csv_df = pd.read_csv(csv_file_path)

    graph = px.line(csv_df, x = "timestamp", y = "close", title = symbol + " Stock Prices Over Time")
    graph.show()

    #high and low stock prices line graph
    fig = px.line(csv_df, x="timestamp", y=["high", "low"], title = symbol + " High and Low Stock Prices Over Time")
    fig.show()
    
    #bar chart of the volumes
    bar = px.bar(csv_df, x = "timestamp", y = "volume", title = symbol + " Stock Volume Over Time")
    bar.show()

    print("-------------------------")
    print("SELECTED SYMBOL: " + symbol)
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT: " + now.strftime("%Y-%m-%d %H:%M:%S"))
    print("-------------------------")
    print("LATEST DAY: " + last_refreshed)
    print("LATEST CLOSE: " + to_usd(float(latest_close)))
    print("RECENT HIGH: " + to_usd(float(recent_high)))
    print("RECENT LOW: " + to_usd(float(recent_low)))
    print("-------------------------")
    print("RECOMMENDATION: " + recommend)
    print("RECOMMENDATION REASON: " + reason)
    print("-------------------------")
    print("WRITING DATA TO CSV: " + csv_file_path)
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")
except:
    print(symbol + " stock symbol not found. Please try again.")

