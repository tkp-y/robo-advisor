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
#check if the input is all letters
if symbol.isalpha() == False:
    print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")
    exit()
#check if input is between 1 and 5 characters
elif len(symbol) < 1 or len(symbol) > 5:
    print("Oh, expecting a properly-formed stock symbol like 'MSFT' with the correct number of letters. Please try again.")
    exit()



try:
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol + "&apikey=" + api_key
    weekly_request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=" + symbol + "&apikey=" + api_key
    response = requests.get(request_url)
    weekly_response = requests.get(weekly_request_url)


    #parse the text
    parsed_response = json.loads(response.text)
    weekly_parsed_response = json.loads(weekly_response.text)

    tsd = parsed_response["Time Series (Daily)"]
    weekly_tsd = weekly_parsed_response["Weekly Time Series"]

    #find the last refreshed date
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    weekly_dates = []
    #get list of dates
    dates = list(tsd.keys()) #sort to ensure latest day is first

    #FURTHER EXPLORATION
    week_list = list(weekly_tsd.keys())
    #go through 52 weeks, find each date and add to list
    for num in range(0,52):
        weekly_dates.append(week_list[num])
    
    
    latest_day = dates[0]

  #find the latest closing price
    latest_close = parsed_response["Time Series (Daily)"][latest_day]["4. close"]

    #FURTHER EXPLORATION
    #create lists to hold the high and low prices from each data
    high_prices = []
    low_prices = []
    for date in weekly_dates:
        high_price = float(weekly_tsd[date]["2. high"])
        low_price = float(weekly_tsd[date]["3. low"])
        high_prices.append(high_price)
        low_prices.append(low_price)

    #find maximum of all high prices, minimum of all low prices
    recent_high = max(high_prices)
    recent_low = min(low_prices)


    #for the recommendation 
    #buy the stock if the latest closing price is less than 25% above the recent low
    if float(latest_close) < (float(recent_low) * 1.25):
        recommend = "Buy!"
        reason = "The stocks latest closing price is less than 25% higher than the recent low, which is under the threshold."
    else:
        recommend = "Do not buy!"
        reason = "The stocks latest closing price is more than 25% higher than the recent low, exceeding the threshold."



    #write info to CSV
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

    #FURTHER EXPLORATION
    #line graph for closing stock prices over time
    csv_df = pd.read_csv(csv_file_path)

    graph = px.line(csv_df, x = "timestamp", y = "close", title = symbol + " Stock Prices Over Time")
    graph.show()

    #high and low stock prices line graph
    fig = px.line(csv_df, x="timestamp", y=["high", "low"], title = symbol + " High and Low Stock Prices Over Time")
    fig.show()
    
    #bar chart of the volumes
    bar = px.bar(csv_df, x = "timestamp", y = "volume", title = symbol + " Stock Volume Over Time")
    bar.show()


    #print out the output
    print("-------------------------")
    print("SELECTED SYMBOL: " + symbol)
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT: " + now.strftime("%Y-%m-%d %H:%M:%S"))
    print("-------------------------")
    print("LATEST DAY: " + last_refreshed)
    print("LATEST CLOSE: " + to_usd(float(latest_close)))
    print("52-WEEK HIGH: " + to_usd(float(recent_high)))
    print("52-WEEK LOW: " + to_usd(float(recent_low)))
    print("-------------------------")
    print("RECOMMENDATION: " + recommend)
    print("RECOMMENDATION REASON: " + reason)
    print("-------------------------")
    print("WRITING DATA TO CSV: " + csv_file_path)
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")
except:
    #if the stock symbol is not found, print out message
    print(symbol + " stock symbol not found. Please try again.")


#Adapted from Professor Rossetti's screencast
