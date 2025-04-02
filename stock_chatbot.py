import yfinance as yf
import streamlit as st
import time

# Function to fetch stock data with retries
def fetch_with_retry(ticker, retries=3):
    for _ in range(retries):
        try:
            stock = yf.Ticker(ticker)
            stock_info = stock.info
            if stock_info:
                return stock_info
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {e}")
            time.sleep(1)  # Wait for a while before retrying
            continue
    return None  # Return None if it fails after retries

# Function to get stock data
def get_stock_data(ticker):
    stock_info = fetch_with_retry(ticker)
    if not stock_info:
        st.error(f"Unable to fetch information for {ticker}. Please check the ticker symbol.")
        return None
    return stock_info

# Streamlit UI for entering stock ticker
st.title("Stock Chatbot")

# Input field for stock symbol
stock_name = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, GOOG):")

# Check if stock name is provided
if stock_name:
    stock_data = get_stock_data(stock_name)

    if stock_data:
        # Display basic stock info
        st.write(f"**Stock Info for {stock_name}:**")
        st.write(stock_data)
        
        # Additional recommendation logic based on stock performance
        try:
            # Example: Simple recommendation logic based on previous closing price
            if 'previousClose' in stock_data:
                previous_close = stock_data['previousClose']
                current_price = stock_data['regularMarketPrice']

                # Simple recommendation (hold, buy, sell) based on the price trend
                if current_price > previous_close:
                    st.success(f"Current price of {stock_name} is higher than the previous close. Consider **buying**.")
                elif current_price < previous_close:
                    st.warning(f"Current price of {stock_name} is lower than the previous close. Consider **selling**.")
                else:
                    st.info(f"Current price of {stock_name} is the same as the previous close. **Hold**.")
            else:
                st.warning("Unable to retrieve previous close data for recommendation.")
        except KeyError as e:
            st.error(f"Error while analyzing stock: {e}")
else:
    st.info("Please enter a stock ticker to get started.")
