import asyncio
import aiohttp
import csv
from datetime import datetime

# API Configuration
API_KEY = "your_alpha_vantage_api_key"  # Replace with your API key
BASE_URL = "https://www.alphavantage.co/query"
SYMBOL = "TSLA"  # Stock symbol (e.g., Tesla)
INTERVAL = "1min"  # Data interval


async def fetch_stock_data():
    async with aiohttp.ClientSession() as session:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "apikey": API_KEY,
        }
        async with session.get(BASE_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                time_series = data.get("Time Series (1min)", {})
                with open("/Users/sameer/Documents/2-development/projects/fintrack-ai/data/stock_data.csv", mode="a", newline="") as file:
                    writer = csv.writer(file)
                    for timestamp, values in time_series.items():
                        row = [
                            timestamp,
                            values["1. open"],
                            values["2. high"],
                            values["3. low"],
                            values["4. close"],
                            values["5. volume"],
                        ]
                        writer.writerow(row)
                        print(row)
                print(f"Data saved for {SYMBOL}")
            else:
                print(f"Error: {response.status}, {await response.text()}")


async def periodic_fetch(interval):
    # Write CSV headers if the file is empty
    with open("/Users/sameer/Documents/2-development/projects/fintrack-ai/data/stock_data.csv", mode="a", newline="") as file:
        if file.tell() == 0:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume"])

    while True:
        await fetch_stock_data()
        await asyncio.sleep(interval)  # Wait for `interval` seconds before fetching again


if __name__ == "__main__":
    # Fetch data every 60 seconds
    asyncio.run(periodic_fetch(60))
