import sqlite3
import pandas as pd

# List of products to extract
products = ['อลูมิเนียมกระป๋องโค้ก', 'อลูมิเนียมแผ่นเพจ', 'อลูมิเนียมฉากขอบใหม่', 'อลูมิเนียมล้อแม็กช์']

# Connect to the SQLite database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Get the names of all tables except PrintHistoryLinks
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'PrintHistoryLinks'")
table_names = [row[0] for row in cursor.fetchall()]


# Function to extract data for a specific product
def extract_product_data(product):
    data = []
    for table_name in table_names:
        query = f'SELECT "ชนิดสินค้า", "ราคา / Price" FROM "{table_name}" WHERE "ชนิดสินค้า" = ?'
        cursor.execute(query, (product,))
        rows = cursor.fetchall()
        for row in rows:
            data.append({'Price': row[1], 'Date': table_name})
    return data


# Extract data for each product and save to CSV
for product in products:
    product_data = extract_product_data(product)
    df = pd.DataFrame(product_data)
    # Sort the DataFrame by the Date column
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')
    df.to_csv(f"{product}.csv", index=False, encoding='utf-8-sig')

# Close the database connection
conn.close()

print("Data has been extracted, sorted, and saved to CSV files.")
