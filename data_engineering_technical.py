import pandas as pd
import pandas_ta as ta

# Read CSV file into DataFrame, specifying thousands parameter if needed
df = pd.read_csv('final_data.csv', thousands=',')

# Rename the desired column if necessary
df.rename(columns={"('ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ราคา / หน่วย')": "price of aluminum extrusion"}, inplace=True)

# Select columns of interest for analysis
columns_of_interest = ["price of aluminum extrusion", 'Set_Price', 'USD_Price', 'import', 'export', 'gdp', 'cpi']

# Ensure all selected columns are numeric
df[columns_of_interest] = df[columns_of_interest].apply(pd.to_numeric, errors='coerce')

# Calculate RSI (Relative Strength Index)  a popular momentum oscillator used in technical analysis to measure the speed and change of price movements.
for column in columns_of_interest:
    df[f'{column}_RSI'] = ta.rsi(df[column], window=14)

# Calculate MACD (Moving Average Convergence Divergence) a trend-following momentum indicator used in technical analysis to identify changes in the strength, direction, momentum, and duration of a trend in a stock's price.
for column in columns_of_interest:
    macd_result = ta.macd(df[column])
    if isinstance(macd_result, pd.DataFrame):
        df[f'{column}_MACD'] = macd_result.iloc[:, 0]  # MACD line
        df[f'{column}_MACD_signal'] = macd_result.iloc[:, 1]  # Signal line
        df[f'{column}_MACD_hist'] = macd_result.iloc[:, 2]  # MACD histogram
    else:
        print(f"MACD calculation failed for {column}")

# Manually calculate Bollinger Bands: a set of three lines plotted in relation to a security's price: a middle line and two outer bands. Bollinger Bands are used to measure market volatility and identify potential overbought or oversold
for column in columns_of_interest:
    rolling_mean = df[column].rolling(window=20).mean()
    rolling_std = df[column].rolling(window=20).std()
    df[f'{column}_BB_MIDDLE'] = rolling_mean
    df[f'{column}_BB_UPPER'] = rolling_mean + 2 * rolling_std
    df[f'{column}_BB_LOWER'] = rolling_mean - 2 * rolling_std

# Fill empty values with values from the row below
df.fillna(method='bfill', inplace=True)

# Save the DataFrame with calculated indicators to a CSV file
df.to_csv('price_of_aluminum_extrusion_with_technical_indicators.csv', index=False)

print("Technical indicators (RSI, MACD, Bollinger Bands) saved to 'price_of_aluminum_extrusion_with_technical_indicators.csv'")









