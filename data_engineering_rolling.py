import pandas as pd

# Read CSV file into DataFrame, specifying thousands parameter
df = pd.read_csv('final_data.csv', thousands=',')

# Rename the desired column
df.rename(columns={"('ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ราคา / หน่วย')": "price of aluminum extrusion"}, inplace=True)

# Select the particular column for which to calculate statistics
column_name = "price of aluminum extrusion"

# Select desired columns
desired_columns = ["price of aluminum extrusion", 'Set_Price', 'USD_Price', 'import', 'export', 'gdp', 'cpi']

df = df[desired_columns]

# Calculate rolling averages
df[f'{column_name}_7_day_avg'] = df[column_name].rolling(window=7).mean()
df[f'{column_name}_30_day_avg'] = df[column_name].rolling(window=30).mean()

# Calculate rolling standard deviations
df[f'{column_name}_7_day_std'] = df[column_name].rolling(window=7).std()
df[f'{column_name}_30_day_std'] = df[column_name].rolling(window=30).std()

# Fill the empty columns with the value below them
df.fillna(method='bfill', inplace=True)

# Save the DataFrame with calculated statistics to a CSV file
df.to_csv('price_of_aluminum_extrusion_with_rolling.csv', index=False)

print("Data with statistics saved to 'price_of_aluminum_extrusion_with_rolling.csv'")

