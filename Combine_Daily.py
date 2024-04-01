import pandas as pd

# Load data from CSV files
price_data = pd.read_csv('aluminum_can.csv')
set_data = pd.read_csv('SET_Index_Historical_Data.csv')
usd_data = pd.read_csv('USD_THB_Historical_Data.csv')

# Rename 'update date' column to 'Date' in price_data
price_data.rename(columns={'update_date': 'Date'}, inplace=True)

# Convert date columns to datetime format
price_data['Date'] = pd.to_datetime(price_data['Date']).dt.strftime('%d/%m/%Y')
set_data['Date'] = pd.to_datetime(set_data['Date'], dayfirst=True).dt.strftime('%d/%m/%Y')
usd_data['Date'] = pd.to_datetime(usd_data['Date'], dayfirst=True).dt.strftime('%d/%m/%Y')

# Merge data

# Merge only 'Price' columns from set_data and usd_data
merged_data = pd.merge(price_data, set_data[['Date', 'Price']], on='Date', how='outer')
merged_data.rename(columns={'Price': 'Set_Price'}, inplace=True)  # Rename 'Price' column from set_data
merged_data = pd.merge(merged_data, usd_data[['Date', 'Price']], on='Date', how='outer')
merged_data.rename(columns={'Price': 'USD_Price'}, inplace=True)  # Rename 'Price' column from usd_data

# Sort data by date
merged_data = merged_data.sort_values(by='Date')

# Define the column with missing data
specific_column = "('ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ชนิดสินค้า')"

# Fill missing values with data from the previous row
merged_data = merged_data.ffill()
merged_data = merged_data.bfill()

# Save merged data to CSV
merged_data.to_csv('merged_daily_data.csv', index=False)

aluminum_data = pd.read_csv('merged_daily_data.csv')
import_export_gdp_cpi_data = pd.read_csv('Import_Export_GDP_CPI.csv')

# Convert date columns to datetime format
aluminum_data['Date'] = pd.to_datetime(aluminum_data['Date'], format='%d/%m/%Y')
import_export_gdp_cpi_data['year'] = pd.to_datetime(import_export_gdp_cpi_data['year'], format='%Y').dt.year

# Merge daily data with import_export_gdp_cpi_data based on year
combined_data = pd.merge(aluminum_data, import_export_gdp_cpi_data, left_on=aluminum_data['Date'].dt.year, right_on='year')

# Drop redundant columns
combined_data.drop(columns=['year'], inplace=True)

# Convert the 'Date' column to datetime format
combined_data['Date'] = pd.to_datetime(combined_data['Date'])

# Sort the data based on the 'Date' column in ascending order
combined_data = combined_data.sort_values(by='Date')

# Save the combined data to a new CSV file
combined_data.to_csv('final_data.csv', index=False)
