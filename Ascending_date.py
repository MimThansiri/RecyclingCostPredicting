import pandas as pd

# Read the CSV file
df_SET = pd.read_csv('SET_Index_Historical_Data.csv')
df_USD = pd.read_csv('USD_THB_Historical_Data.csv')

# Convert 'Date' column to datetime with format day-month-year
df_SET['Date'] = pd.to_datetime(df_SET['Date'], format='%d-%m-%Y')
df_USD['Date'] = pd.to_datetime(df_USD['Date'], format='%d-%m-%Y')

# Sort the DataFrame by the 'Date' column
df_SET = df_SET.sort_values(by='Date')
df_USD = df_USD.sort_values(by='Date')

# Convert 'Date' column back to strings in the format day-month-year
df_SET['Date'] = df_SET['Date'].dt.strftime('%d-%m-%Y')
df_USD['Date'] = df_USD['Date'].dt.strftime('%d-%m-%Y')

# Save the sorted DataFrame to a CSV file with the same name
df_SET.to_csv('SET_Index_Historical_Data.csv', index=False)
df_USD.to_csv('USD_THB_Historical_Data.csv', index=False)

# Print a message to indicate the process is done
print("Data sorted and saved successfully.")
