import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('RecyclingCost.db')
cursor = conn.cursor()

# Initialize an empty dataframe
df_aluminum_can = pd.DataFrame()

# Fetch file_name and update_date from PrintHistoryLinks table
cursor.execute("SELECT file_name, update_date FROM PrintHistoryLinks")
rows = cursor.fetchall()

# Loop through each row
for row in rows:
    file_name, update_date = row

    # Fetch column names from the corresponding table
    cursor.execute(f"PRAGMA table_info('{file_name}')")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]

    # Fetch data from the corresponding table where the specified column equals 'อลูมิเนียมกระป๋องโค้ก'
    query = f"SELECT * FROM '{file_name}' WHERE [('ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ชนิดสินค้า')] = ?"
    cursor.execute(query, ('อลูมิเนียมกระป๋องโค้ก',))
    data = cursor.fetchone()

    # If data exists, create a dataframe with fetched data and set column names
    if data:
        temp_df = pd.DataFrame([data], columns=column_names)
        # Add update_date column to the dataframe
        temp_df['update_date'] = update_date
        # Append the dataframe to the main dataframe
        df_aluminum_can = pd.concat([df_aluminum_can, temp_df], ignore_index=True)

# Close the connection
conn.close()

# Print the dataframe
print("Dataframe:")
print(df_aluminum_can)

# Print column names to debug
print("Column Names:", df_aluminum_can.columns)

# Convert 'update_date' column to datetime
df_aluminum_can['update_date'] = pd.to_datetime(df_aluminum_can['update_date'], format='%d-%m-%Y')

# Save the dataframe as a CSV file
df_aluminum_can.to_csv('aluminum_can.csv', index=False)

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(df_aluminum_can['update_date'], df_aluminum_can["('ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ราคา / "
                                                            "หน่วย')"], color='blue', label='Data')

# Fit linear regression
regression_model = LinearRegression()
X = df_aluminum_can['update_date'].apply(lambda x: x.toordinal()).values.reshape(-1, 1)
y = df_aluminum_can["('ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ราคา / หน่วย')"]
regression_model.fit(X, y)

# Plotting the regression line
plt.plot(df_aluminum_can['update_date'], regression_model.predict(X), color='red', label='Linear Regression')

plt.title('Linear Regression: Aluminum Can')
plt.xlabel('Date')
plt.ylabel('Price per unit')
plt.legend()

# Save the plot as PNG image
plt.savefig('linear_regression_plot.png')

plt.show()
