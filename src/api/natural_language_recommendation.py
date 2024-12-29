import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd
import torch

# Retrieve the access token from the environment variable
access_token = os.getenv('HUGGINGFACE_TOKEN')

# Specify the model name
model_name = "meta-llama/Llama-3.2-1B-Instruct"

# Load the tokenizer and model with the access token
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=access_token)
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=access_token)

# Load stock data
STOCK_DATA_FILE = "../../data/stock_data_with_recommendations.csv"
df = pd.read_csv(STOCK_DATA_FILE)

# Debugging: Print columns
print("Columns in CSV:", df.columns)

def query_recommendation():
    # Fixed stock symbol
    stock_symbol = "TSLA"

    # Ensure the dataframe has the expected structure
    required_columns = [
        "Timestamp", "Open", "High", "Low", "Close", "Volume",
        "SMA_10", "RSI", "BB_Upper", "BB_Middle", "BB_Lower", "Recommendation"
    ]
    if not all(col in df.columns for col in required_columns):
        return f"Error: Missing required columns. Found columns: {list(df.columns)}"

    # Get the latest data
    latest_data = df.iloc[-1]
    summary = (
        f"Stock: {stock_symbol}\n"
        f"Timestamp: {latest_data['Timestamp']}\n"
        f"Open: {latest_data['Open']}, High: {latest_data['High']}, Low: {latest_data['Low']}\n"
        f"Close: {latest_data['Close']}, Volume: {latest_data['Volume']}\n"
        f"SMA_10: {latest_data['SMA_10']}, RSI: {latest_data['RSI']}\n"
        f"Bollinger Bands:\n"
        f"  Upper: {latest_data['BB_Upper']}, Middle: {latest_data['BB_Middle']}, Lower: {latest_data['BB_Lower']}\n"
        f"Recommendation: {latest_data['Recommendation']}\n"
    )

    # Generate a detailed recommendation using the Llama model
    prompt = f"Based on the following stock data, provide a detailed investment recommendation:\n{summary}"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=600)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response.strip()

if __name__ == "__main__":
    response = query_recommendation()
    print(f"\nAI Response:\n{response}")
