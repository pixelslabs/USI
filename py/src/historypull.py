import yfinance as yf
import pandas as pd
import numpy as np

# Function to calculate technical indicators
def calculate_indicators(data):
    # Calculate Moving Averages
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()
    
    # Calculate EMA
    data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
    
    # Calculate RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Calculate MACD
    exp12 = data['Close'].ewm(span=12, adjust=False).mean()
    exp26 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp12 - exp26
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    
    # Calculate Bollinger Bands
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['STD_20'] = data['Close'].rolling(window=20).std()
    data['Upper_Band'] = data['SMA_20'] + (data['STD_20'] * 2)
    data['Lower_Band'] = data['SMA_20'] - (data['STD_20'] * 2)
    
    return data

# Function to suggest buy range
def get_buy_range(data):
    latest = data.iloc[-1]
    buy_range = {
        'lower': round(latest['Lower_Band'], 2),
        'upper': round(latest['SMA_20'], 2)
    }
    return buy_range

# Main function
def analyze_stocks(tickers):
    for ticker in tickers:
        try:
            print(f"\nAnalyzing {ticker}...")
            
            # Download historical data
            stock = yf.Ticker(ticker)
            data = stock.history(period="1y")
            
            if data.empty:
                print(f"No data found for {ticker}")
                continue
                
            # Calculate indicators
            data = calculate_indicators(data)
            
            # Get latest values
            latest = data.iloc[-1]
            current_price = round(latest['Close'], 2)
            
            # Get buy range suggestion
            buy_range = get_buy_range(data)
            
            # Display results
            print(f"Current Price: ${current_price}")
            print(f"Suggested Buy Range: ${buy_range['lower']} - ${buy_range['upper']}")
            print("Technical Indicators:")
            print(f"50-Day SMA: ${round(latest['SMA_50'], 2)}")
            print(f"200-Day SMA: ${round(latest['SMA_200'], 2)}")
            print(f"20-Day EMA: ${round(latest['EMA_20'], 2)}")
            print(f"RSI: {round(latest['RSI'], 2)}")
            print(f"MACD: {round(latest['MACD'], 2)}")
            print(f"Bollinger Upper Band: ${round(latest['Upper_Band'], 2)}")
            print(f"Bollinger Lower Band: ${round(latest['Lower_Band'], 2)}")
            
        except Exception as e:
            print(f"Error analyzing {ticker}: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Add your list of tickers here
    tickers = ['XTIA','ARQQ','FCUV','QUBT','IONQ','RGTI','NITO','BHAT','RIME','SES','GSAT']
    
    analyze_stocks(tickers)