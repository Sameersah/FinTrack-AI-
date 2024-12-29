import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the Llama model and tokenizer
model_name = "meta-llama/Llama-3.2-1B-Instruct"  # Replace with the model you are using
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=True)

# Load stock data
STOCK_DATA_FILE = "../../data/stock_data_with_recommendations.csv"
df = pd.read_csv(STOCK_DATA_FILE)

# Function to get TSLA stock data
def get_tsla_data():
    latest_data = df.iloc[-1]  # Get the most recent row
    return {
        "Stock": "TSLA",
        "Latest Price": latest_data["Close"],
        "Recommendation": latest_data["Recommendation"],
        "RSI": latest_data["RSI"],
        "SMA_10": latest_data["SMA_10"],
    }

# Function to generate response using the Llama model
def generate_response(user_query, stock_info=None):
    if stock_info:
        # Incorporate stock information into the response
        summary = (
            f"Stock: {stock_info['Stock']}\n"
            f"Latest Price: {stock_info['Latest Price']}\n"
            f"Recommendation: {stock_info['Recommendation']}\n"
            f"RSI: {stock_info['RSI']}, SMA_10: {stock_info['SMA_10']}\n"
        )
        prompt = f"User Query: {user_query}\nBased on the following stock data, provide a detailed response:\n{summary}"
    else:
        # General query
        prompt = f"User Query: {user_query}\nRespond as a financial advisor."

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=1000)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Chat loop
def chat():
    print("Welcome to the Stock Advisor Chat! Type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Determine if the user is asking about TSLA
        if "TSLA" in user_input.upper():
            stock_info = get_tsla_data()
            response = generate_response(user_input, stock_info)
        else:
            response = generate_response(user_input)

        print(f"\nAI: {response}")

if __name__ == "__main__":
    chat()
