import pandas as pd

# Read CSV file into DataFrame, specifying thousands parameter
df = pd.read_csv('final_data.csv', thousands=',')

# Rename the desired column
df.rename(columns={"('ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ราคา / หน่วย')": "price of aluminum extrusion"}, inplace=True)

# Select desired columns
desired_columns = ["price of aluminum extrusion", 'Set_Price', 'USD_Price', 'import', 'export', 'gdp', 'cpi']

selected_df = df[desired_columns]

# Function to create lagged features and fill early rows with current values
def create_lagged_features(dataframe, column_list, max_lag):
    for column in column_list:
        for lag in range(1, max_lag + 1):
            lagged_column_name = f'{column}_lag_{lag}'
            dataframe[lagged_column_name] = dataframe[column].shift(lag)
            # Fill early rows with the current value of the column
            dataframe[lagged_column_name].fillna(dataframe[column], inplace=True)
    return dataframe

# Define maximum number of lag periods
max_lag = 3  # Example: 3 lag periods

# Create lagged features for the selected columns
lagged_df = create_lagged_features(selected_df, desired_columns, max_lag)

# Save the DataFrame with lagged features to a CSV file
lagged_df.to_csv('price_of_aluminum_extrusion_with_lag.csv', index=False)

print("Data with lagged features saved to 'price_of_aluminum_extrusion_with_lag.csv'")
