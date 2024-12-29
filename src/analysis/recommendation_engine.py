import pandas as pd

def generate_recommendations(csv_file):
    # Load data with indicators
    df = pd.read_csv(csv_file, parse_dates=["Timestamp"])
    recommendations = []

    for i, row in df.iterrows():
        recommendation = "Hold"  # Default recommendation

        # Example rules:
        # 1. Buy: If the closing price is below the lower Bollinger Band
        if row["Close"] < row["BB_Lower"]:
            recommendation = "Buy"
        # 2. Sell: If the closing price is above the upper Bollinger Band
        elif row["Close"] > row["BB_Upper"]:
            recommendation = "Sell"
        # 3. Hold: If RSI is between 30 and 70 (normal range)
        elif 30 <= row["RSI"] <= 70:
            recommendation = "Hold"

        recommendations.append(recommendation)

    # Add recommendations to the DataFrame
    df["Recommendation"] = recommendations

    # Save updated data with recommendations
    df.to_csv("../../data/stock_data_with_recommendations.csv", index=False)
    print("Recommendations generated and saved.")

if __name__ == "__main__":
    generate_recommendations("../../data/stock_data_with_indicators.csv")
