import requests
from bs4 import BeautifulSoup
import pandas as pd
# import sqlite3
from tabulate import tabulate

# Step 1: Fetch data from the website
url = 'https://wongpanit.com/print_history_price/97'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

# print(soup)

# print(soup.find_all('table')[0])  # Banner & Bill name Date
# 1 PAGE has 8 table(0-7)
# print(soup.find_all('table')[1])  # Steel
# print(soup.find_all('table')[2])  # Paper
# print(soup.find_all('table')[3])  # Glass
# print(soup.find_all('table')[4])  # Plastic
# print(soup.find_all('table')[5])  # Nonferrous metals
# print(soup.find_all('table')[6])  # E-waste
# print(soup.find_all('table')[7])  # Other scraps

# SET INSTANCE
table1 = soup.find_all('table')[1]
# print(table1)
garbage_title = table1.find_all('th')
# print(garbage_title)
garbage_table_title = [title.text for title in garbage_title]
# print(garbage_table_title)

# Extract the main title
main_title = garbage_title[0].text.strip()
# print(main_title)

subcategories = garbage_title[1].text.strip()
price = garbage_title[2].text.strip()

# Combine the main title with unique subcategories and prices
combined_title = {
    main_title: {
        'ชนิดสินค้า': subcategories,
        'ราคา / หน่วย': price
    }
}
# print(combined_title)

# Convert the combined_title dictionary into a DataFrame
df = pd.DataFrame.from_dict(combined_title, orient='index')

# Print the DataFrame
print(tabulate(df))

# df = pd.DataFrame(columns=garbage_table_title)
# print(tabulate(df, headers='keys'))

# # Find the first row in the table (which contains the headers)
# header = table1.find('th').text.strip()
# print(header)  # Steel

# header_row = table1.find('tr')
# # Extract individual header cells
# header_cells = header_row.find_all('th')
# print(header_cells)
#
# # Initialize lists to store subcategories and prices
# subcategories = []
# prices = []
#
# # Iterate through the header cells
# for i in range(len(header_cells)):
#     # Check if there are enough cells left to extract both subcategory and price
#     if i + 1 < len(header_cells):
#         subcategories.append(header_cells[i].text.strip())
#         prices.append(header_cells[i + 1].text.strip())
#
# # Now, subcategories and prices should be aligned correctly
# print(subcategories)
# print(prices)

# subcategory_rows = table1.find_all('tr')[1]
# # print(subcategory_rows)
