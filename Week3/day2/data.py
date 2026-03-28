import requests
import pandas as pd

API_KEY = "40XA3F2Y321IJLHN"
SYMBOL  = "TSLA"

url = (
    f"https://www.alphavantage.co/query"
    f"?function=TIME_SERIES_DAILY"
    f"&symbol={SYMBOL}"
    f"&apikey={API_KEY}"
)

print(f"Fetching {SYMBOL} data...")
response = requests.get(url)
data = response.json()

if "Time Series (Daily)" not in data:
    print("API Error:", data)
    exit()

ts = data["Time Series (Daily)"]
df = pd.DataFrame(ts).T
df.index.name = "date"
df.columns = ["open", "high", "low", "close", "volume"]
df = df.sort_index()

df.to_csv(f"{SYMBOL}_stock_data.csv")
print(f"Saved {len(df)} rows to {SYMBOL}_stock_data.csv")