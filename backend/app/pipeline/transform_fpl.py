from datetime import datetime
import time

def transform_stocks(stocks_raw):
    if "Time Series (Daily)" not in stocks_raw:
        print(f"Skipping - unexpected response: {stocks_raw}")
        return []
        
    stocks_transformed = [{
        "fetched_at":  datetime.utcnow().isoformat(),
        "ticker":      stocks_raw["Meta Data"]["2. Symbol"],
        "trade_date":  date,
        "open_price":  float(values["1. open"]),
        "high_price":  float(values["2. high"]),
        "low_price":   float(values["3. low"]),
        "close_price": float(values["4. close"]),
        "volume":      int  (values["5. volume"])

    }
    for date, values in stocks_raw["Time Series (Daily)"].items()
    ]

    return stocks_transformed


if __name__ == "__main__":
    from etl.extractors.stocks_extractor import fetch_stocks_data

    TICKERS = ["AAPL", "MSFT", "NVDA", "GOOGL", "META", "AMZN"]

    for ticker in TICKERS:
        raw_stocks_data = fetch_stocks_data(ticker)
        print(transform_stocks(raw_stocks_data))
        time.sleep(2)