import pandas as pd
import ta

def calculate_technical_indicators(csv_file):
    # Load data
    df = pd.read_csv(csv_file, parse_dates=["Timestamp"])
    df.set_index("Timestamp", inplace=True)

    # Calculate indicators
    df["SMA_10"] = ta.trend.sma_indicator(df["Close"], window=10)  # Simple Moving Average
    df["RSI"] = ta.momentum.rsi(df["Close"])                      # Relative Strength Index
    df["BB_Upper"], df["BB_Middle"], df["BB_Lower"] = ta.volatility.bollinger_hband_indicator(df["Close"]), \
                                                     ta.volatility.bollinger_mavg(df["Close"]), \
                                                     ta.volatility.bollinger_lband_indicator(df["Close"])

    # Save updated data
    df.to_csv("/Users/sameer/Documents/2-development/projects/fintrack-ai/data/stock_data_with_indicators.csv")
    print("Technical indicators calculated and saved.")

if __name__ == "__main__":
    calculate_technical_indicators("/Users/sameer/Documents/2-development/projects/fintrack-ai/data/stock_data.csv")
