import pandas as pd

# Load the CSV files into pandas DataFrames
aluminum_can = pd.read_csv("aluminum_can.csv")
final_data = pd.read_csv("final_data.csv")

# Convert 'update_date' and 'Date' columns to datetime objects for matching
aluminum_can['update_date'] = pd.to_datetime(aluminum_can['update_date'])
final_data['Date'] = pd.to_datetime(final_data['Date'])

# Merge the DataFrames on matching dates (Performing a left merge to retain all data from aluminum_can)
merged_data = pd.merge(aluminum_can, final_data, left_on='update_date', right_on='Date', how='left')

# Rename the specified column
merged_data.rename(columns={ "('ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ราคา / หน่วย')_x": "price" }, inplace=True)

# Select the desired columns
selected_columns = ['price', 'export', 'update_date']
merged_data = merged_data[selected_columns]

# Fill missing values in 'export' column
# Fill 2018 missing values with 252.485
merged_data.loc[merged_data['update_date'].dt.year == 2018, 'export'] = 252.485

# Fill missing values for the year 2024 with the previous available values
merged_data['export'] = merged_data.groupby(merged_data['update_date'].dt.year)['export'].ffill()

# Save the merged data to a new CSV file with 'Date' column based on 'update_date'
merged_data.to_csv("preprocess_data.csv", index=False)

# Display the shape of the merged data to verify data retention
print("Merged data shape:", merged_data.shape)
