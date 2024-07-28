import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Read CSV file into DataFrame, specifying thousands parameter if needed
df = pd.read_csv('final_data.csv', thousands=',')

# Rename the desired column if necessary
df.rename(columns={"('ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ราคา / หน่วย')": "price of aluminum extrusion"}, inplace=True)

# Select columns of interest for analysis
columns_of_interest = ["price of aluminum extrusion", 'Set_Price', 'USD_Price', 'import', 'export', 'gdp', 'cpi']

# Ensure all selected columns are numeric
df[columns_of_interest] = df[columns_of_interest].apply(pd.to_numeric, errors='coerce')

# Normalization (Min-Max scaling) for each column
scaler_minmax = MinMaxScaler()
for column in columns_of_interest:
    df[f'{column}_normalized'] = scaler_minmax.fit_transform(df[[column]])

# Standardization (Z-score scaling) for each column
scaler_standard = StandardScaler()
for column in columns_of_interest:
    df[f'{column}_standardized'] = scaler_standard.fit_transform(df[[column]])

# Save the DataFrame with normalized and standardized columns to a CSV file
df.to_csv('price_of_aluminum_extrusion_normalized_standardized.csv', index=False)

print("Normalized and standardized data saved to 'price_of_aluminum_extrusion_normalized_standardized.csv'")
