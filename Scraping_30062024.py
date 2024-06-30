# import requests
# from bs4 import BeautifulSoup
# import sqlite3
# import pandas as pd
# from urllib.parse import urljoin
# import os
# import re
# import datetime
#
# # Base URL of the main page
# base_url = "https://wongpanit.com/list_history_price/"
#
# # List to store all print_history_price links
# print_history_price_links = []
#
#
# # Function to scrape links from a page
# def scrape_links_from_page(url):
#     # Send a GET request to the page
#     response = requests.get(url)
#     # Parse the HTML content
#     soup = BeautifulSoup(response.text, "html.parser")
#     # Find all links on the page
#     all_links = soup.find_all("a", href=True)
#     # Filter the links that contain "print_history_price"
#     page_print_history_price_links = [
#         urljoin(url, link_tag["href"]) for link_tag in all_links if "print_history_price" in link_tag["href"]
#     ]
#     # Extend the list of print_history_price links
#     print_history_price_links.extend(page_print_history_price_links)
#
#
# # Start with the base URL
# page_url = base_url
#
# while True:
#     # Scrape links from the current page
#     scrape_links_from_page(page_url)
#
#     # Send a GET request to the page
#     response = requests.get(page_url)
#     # Parse the HTML content
#     soup = BeautifulSoup(response.text, "html.parser")
#
#     # Try to find the "next page" link
#     next_page_link = soup.find("a",
#                                rel="next")
#
#     if next_page_link is not None:
#         # If the "next page" link exists, follow it to the next page
#         page_url = urljoin(page_url, next_page_link["href"])
#     else:
#         # If the "next page" link does not exist, we've reached the last page and can break the loop
#         break
#
# # Extract and sort the numerical values following 'https://wongpanit.com/print_history_price/'
# sorted_links = sorted(print_history_price_links, key=lambda x: int(x.split('/')[-1]))
#
# # Create SQLite database file if it doesn't exist
# db_filename = 'data.db'
# if not os.path.exists(db_filename):
#     conn = sqlite3.connect(db_filename)
#     conn.close()
#
# # Connect to the SQLite database
# conn = sqlite3.connect(db_filename)
# cursor = conn.cursor()
#
# # Create a table to store the links if it doesn't exist
# cursor.execute('''CREATE TABLE IF NOT EXISTS PrintHistoryLinks (
#                     id INTEGER PRIMARY KEY,
#                     link TEXT UNIQUE,
#                     update_date TEXT
#                 )''')
#
# # Insert each link into the table
# for link in enumerate(sorted_links, start=1):
#     cursor.execute('''INSERT OR IGNORE INTO PrintHistoryLinks (id, link) VALUES (?, ?)''', link)
#
# # Commit changes and close the connection
# conn.commit()
# conn.close()
#
# print("Links have been saved to the database ordered by the numerical values")
#
# # Function to create a new column in the PrintHistoryLinks table
# def add_column():
#     db_connection = sqlite3.connect('data.db')
#     cursor_col = db_connection.cursor()
#
#     # Define the SQL query to add the file_name column to the PrintHistoryLinks table
#     alter_query = "ALTER TABLE PrintHistoryLinks ADD COLUMN file_name TEXT"
#
#     # Execute the query
#     cursor_col.execute(alter_query)
#
#     # Commit the changes
#     db_connection.commit()
#
#     # Close the cursor and connection
#     cursor_col.close()
#     db_connection.close()
#
#
# # Function to scrape and process data from a given URL
# def process_url(url):
#     page = requests.get(url)
#     soup = BeautifulSoup(page.text, 'html.parser')
#
#     banner = soup.find_all('table')[0]
#
#     # Find the <h1> element within the <table> element
#     h1_element = banner.find('h1')
#
#     # Extract the text from the <h1> element
#     name = h1_element.get_text(strip=True)
#     # Split the string into words
#     words = name.split()
#
#     # Join the words back together with a single space between them
#     file_name = ' '.join(words)
#
#     print(file_name)
#
#     # Update the PrintHistoryLinks table with the file name
#     db_connection_out = sqlite3.connect('data.db')
#     cursor_out = db_connection_out.cursor()
#
#     # Define the SQL query to insert the file name into the PrintHistoryLinks table
#     insert_query = "UPDATE PrintHistoryLinks SET file_name = ? WHERE link = ?"
#
#     # Execute the query
#     cursor_out.execute(insert_query, (file_name, url))
#
#     # Commit the changes
#     db_connection_out.commit()
#
#     # Close the cursor and connection
#     cursor_out.close()
#     db_connection_out.close()
#
#     # print(soup.find_all('table')[5])  # Nonferrous metals
#
#     nonferrous_metals = soup.find_all('table')[5]
#
#     nonferrous_metals_title = nonferrous_metals.find_all('th')
#
#     main_title = nonferrous_metals_title[0].text.strip()
#     # print(main_title)
#
#     subcategories = nonferrous_metals_title[1].text.strip()
#     price = nonferrous_metals_title[2].text.strip()
#
#     nonferrous_metals_values = nonferrous_metals.find_all('td')
#
#     import re
#     # Initialize an empty list to store the values
#     nonferrous_metals_all_values_list = []
#
#     for nonferrous_metals_value in nonferrous_metals_values:
#         h1_tag = nonferrous_metals_value.find('h1')
#         if h1_tag:  # Check if <h1> tag exists
#             value = h1_tag.text.strip()  # Extract text within <h1> and remove leading/trailing whitespace
#             # Use regex to remove "-" at the end or just before the decimal point
#             value_without_dash = re.sub(r'(\.-|\.$)', '', value)
#
#             # Append the value to the list
#             nonferrous_metals_all_values_list.append(value_without_dash)
#             # print(value_without_dash, type(value_without_dash))
#
#     # Initialize empty lists to store values of different types
#     price_value = []
#     subcategories_value = []
#
#     for value in nonferrous_metals_all_values_list:
#         try:
#             # Try converting the value to a float
#             float_value = float(value)
#             # If successful, append the float value to the converted_values list
#             price_value.append(float_value)
#         except ValueError:
#             # If conversion to float fails, keep the value as string and append it to the converted_values list
#             subcategories_value.append(value)
#
#     # Create a DataFrame with MultiIndex
#     df_nonferrous_metals = pd.DataFrame(index=subcategories_value, columns=pd.MultiIndex.from_tuples(
#         [(main_title, subcategories), (main_title, price)]))
#     # Fill the DataFrame with values
#     df_nonferrous_metals[(main_title, subcategories)] = subcategories_value
#     df_nonferrous_metals[(main_title, price)] = price_value
#     df_nonferrous_metals = df_nonferrous_metals.reset_index(drop=True)
#
#     # Create a connection to the SQLite database (if the database doesn't exist, it will be created)
#     db_connection = sqlite3.connect('data.db')
#
#     # Save the DataFrame to the database
#     df_nonferrous_metals.to_sql(name=file_name, con=db_connection, if_exists='replace', index=False)
#
#     # Close the connection
#     db_connection.close()
#
# # Add the file_name column to the PrintHistoryLinks table
# add_column()
#
# # Connect to the SQLite database
# db_connection_outer = sqlite3.connect('data.db')
#
# # Create a cursor object to execute SQL queries
# cursor = db_connection_outer.cursor()
#
# # Define the SQL query to retrieve URLs from the PrintHistoryLinks table
# query = "SELECT link FROM PrintHistoryLinks ORDER BY id"
#
# # Execute the query
# cursor.execute(query)
#
# # Fetch all the rows from the result set
# rows = cursor.fetchall()
#
# # Extract the URLs from the rows
# urls = [row[0] for row in rows]
#
# # Close the cursor and connection
# cursor.close()
# db_connection_outer.close()
#
# # Initialize a counter to keep track of the number of iterations
# iteration_count = 0
#
# # Loop through the URLs and process each one
# while urls:
#     iteration_count += 1
#     link = urls.pop(0)  # Pop the first link from the list
#     process_url(link)
#
#     # Break the loop if there are no more URLs left to process
#     if not urls:
#         break
#
# # Print the total number of iterations
# print("Total iterations:", iteration_count)
#
# def updateFileNameColumn():
#     conn = sqlite3.connect('data.db')
#     cursor = conn.cursor()
#
#     # Fetch the file_name column from PrintHistoryLinks table
#     cursor.execute("SELECT link FROM PrintHistoryLinks")
#     rows = cursor.fetchall()
#
#     for row in rows:
#         file_name = row[0]
#         updated_file_name = processFileName(file_name)
#         # Update the table with the modified file name
#         cursor.execute("UPDATE PrintHistoryLinks SET update_date = ? WHERE link = ?",
#                        (updated_file_name, file_name))
#
#     # Commit the changes and close the connection
#     conn.commit()
#     conn.close()
#
#
# def processFileName(file_name):
#     tmp = "temporary word replace"
#     jan = "มกราคม"
#     feb = "กุมภาพันธ์"
#     mar = "มีนาคม"
#     apr = "เมษายน"
#     may = "พฤษภาคม"
#     jun = "มิถุนายน"
#     jul = "กรกฏาคม"
#     aug = "สิงหาคม"
#     sep = "กันยายน"
#     oct = "ตุลาคม"
#     nov = "พฤศจิกายน"
#     dec = "ธันวาคม"
#
#     file_name = file_name.replace("ใบแจ้งราคารับซื้อสินค้า วัน", '')
#     file_name = file_name.replace("(ราคาค้าปลีก)", '')
#
#     file_name = file_name.replace('ที่', tmp)
#
#     if tmp in file_name:
#         getDate = file_name[file_name.find(tmp) + len(tmp):]
#         date = int(getDate[0:3])
#
#         if re.search(jan, getDate):
#             month = 1
#         elif re.search(feb, getDate):
#             month = 2
#         elif re.search(mar, getDate):
#             month = 3
#         elif re.search(apr, getDate):
#             month = 4
#         elif re.search(may, getDate):
#             month = 5
#         elif re.search(jun, getDate):
#             month = 6
#         elif re.search(jul, getDate):
#             month = 7
#         elif re.search(aug, getDate):
#             month = 8
#         elif re.search(sep, getDate):
#             month = 9
#         elif re.search(oct, getDate):
#             month = 10
#         elif re.search(nov, getDate):
#             month = 11
#         elif re.search(dec, getDate):
#             month = 12
#         else:
#             return None
#
#         year = int(getDate[-5:]) - 543
#         x = datetime.datetime(year, month, date).date()
#         dataDate = x.strftime("%Y-%m-%d")
#         return dataDate
#     else:
#         return None
#
#
# updateFileNameColumn()


import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
from urllib.parse import urljoin
import os
import re
import datetime

# Base URL of the main page
base_url = "https://wongpanit.com/list_history_price/"

# List to store all print_history_price links
print_history_price_links = []


# Function to scrape links from a page
def scrape_links_from_page(url):
    # Send a GET request to the page
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    # Find all links on the page
    all_links = soup.find_all("a", href=True)
    # Filter the links that contain "print_history_price"
    page_print_history_price_links = [
        urljoin(url, link_tag["href"]) for link_tag in all_links if "print_history_price" in link_tag["href"]
    ]
    # Extend the list of print_history_price links
    print_history_price_links.extend(page_print_history_price_links)


# Start with the base URL
page_url = base_url

while True:
    # Scrape links from the current page
    scrape_links_from_page(page_url)

    # Send a GET request to the page
    response = requests.get(page_url)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Try to find the "next page" link
    next_page_link = soup.find("a", rel="next")

    if next_page_link is not None:
        # If the "next page" link exists, follow it to the next page
        page_url = urljoin(page_url, next_page_link["href"])
    else:
        # If the "next page" link does not exist, we've reached the last page and can break the loop
        break

# Extract and sort the numerical values following 'https://wongpanit.com/print_history_price/'
sorted_links = sorted(print_history_price_links, key=lambda x: int(x.split('/')[-1]))

# Create SQLite database file if it doesn't exist
db_filename = 'data.db'
if not os.path.exists(db_filename):
    conn = sqlite3.connect(db_filename)
    conn.close()

# Connect to the SQLite database
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Create a table to store the links if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS PrintHistoryLinks (
                    id INTEGER PRIMARY KEY,
                    link TEXT UNIQUE,
                    file_name TEXT,
                    update_date TEXT
                )''')

# Insert each link into the table
for link in enumerate(sorted_links, start=1):
    cursor.execute('''INSERT OR IGNORE INTO PrintHistoryLinks (id, link) VALUES (?, ?)''', link)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Links have been saved to the database ordered by the numerical values")


# Function to scrape and process data from a given URL
def process_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    banner = soup.find_all('table')[0]

    # Find the <h1> element within the <table> element
    h1_element = banner.find('h1')

    # Extract the text from the <h1> element
    name = h1_element.get_text(strip=True)
    # Split the string into words
    words = name.split()

    # Join the words back together with a single space between them
    file_name = ' '.join(words)

    print(file_name)

    # Update the PrintHistoryLinks table with the file name
    db_connection_out = sqlite3.connect('data.db')
    cursor_out = db_connection_out.cursor()

    # Define the SQL query to insert the file name into the PrintHistoryLinks table
    insert_query = "UPDATE PrintHistoryLinks SET file_name = ? WHERE link = ?"

    # Execute the query
    cursor_out.execute(insert_query, (file_name, url))

    # Commit the changes
    db_connection_out.commit()

    # Close the cursor and connection
    cursor_out.close()
    db_connection_out.close()

    # print(soup.find_all('table')[5])  # Nonferrous metals

    nonferrous_metals = soup.find_all('table')[5]

    nonferrous_metals_title = nonferrous_metals.find_all('th')

    main_title = nonferrous_metals_title[0].text.strip()
    # print(main_title)

    subcategories = nonferrous_metals_title[1].text.strip()
    price = nonferrous_metals_title[2].text.strip()

    nonferrous_metals_values = nonferrous_metals.find_all('td')

    # Initialize an empty list to store the values
    nonferrous_metals_all_values_list = []

    for nonferrous_metals_value in nonferrous_metals_values:
        h1_tag = nonferrous_metals_value.find('h1')
        if h1_tag:  # Check if <h1> tag exists
            value = h1_tag.text.strip()  # Extract text within <h1> and remove leading/trailing whitespace
            # Use regex to remove "-" at the end or just before the decimal point
            value_without_dash = re.sub(r'(\.-|\.$)', '', value)

            # Append the value to the list
            nonferrous_metals_all_values_list.append(value_without_dash)
            # print(value_without_dash, type(value_without_dash))

    # Initialize empty lists to store values of different types
    price_value = []
    subcategories_value = []

    for value in nonferrous_metals_all_values_list:
        try:
            # Try converting the value to a float
            float_value = float(value)
            # If successful, append the float value to the converted_values list
            price_value.append(float_value)
        except ValueError:
            # If conversion to float fails, keep the value as string and append it to the converted_values list
            subcategories_value.append(value)

    # Create a DataFrame with MultiIndex
    df_nonferrous_metals = pd.DataFrame(index=subcategories_value, columns=pd.MultiIndex.from_tuples(
        [(main_title, subcategories), (main_title, price)]))
    # Fill the DataFrame with values
    df_nonferrous_metals[(main_title, subcategories)] = subcategories_value
    df_nonferrous_metals[(main_title, price)] = price_value
    df_nonferrous_metals = df_nonferrous_metals.reset_index(drop=True)

    # Create a connection to the SQLite database (if the database doesn't exist, it will be created)
    db_connection = sqlite3.connect('data.db')

    # Save the DataFrame to the database
    df_nonferrous_metals.to_sql(name=file_name, con=db_connection, if_exists='replace', index=False)

    # Close the connection
    db_connection.close()


# Connect to the SQLite database
db_connection_outer = sqlite3.connect('data.db')

# Create a cursor object to execute SQL queries
cursor = db_connection_outer.cursor()

# Define the SQL query to retrieve URLs from the PrintHistoryLinks table
query = "SELECT link FROM PrintHistoryLinks ORDER BY id"

# Execute the query
cursor.execute(query)

# Fetch all the rows from the result set
rows = cursor.fetchall()

# Extract the URLs from the rows
urls = [row[0] for row in rows]

# Close the cursor and connection
cursor.close()
db_connection_outer.close()

# Initialize a counter to keep track of the number of iterations
iteration_count = 0

# Loop through the URLs and process each one
while urls:
    iteration_count += 1
    link = urls.pop(0)  # Pop the first link from the list
    process_url(link)

    # Break the loop if there are no more URLs left to process
    if not urls:
        break

# Print the total number of iterations
print("Total iterations:", iteration_count)


def addUpdatedFileNameColumn():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Check if the update_date column exists
    cursor.execute("PRAGMA table_info(PrintHistoryLinks)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]

    if "update_date" not in column_names:
        # Add the update_date column to PrintHistoryLinks table if it doesn't exist
        cursor.execute("ALTER TABLE PrintHistoryLinks ADD COLUMN update_date TEXT")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def updateFileNameColumn():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Fetch the file_name column from PrintHistoryLinks table
    cursor.execute("SELECT file_name FROM PrintHistoryLinks")
    rows = cursor.fetchall()

    for row in rows:
        file_name = row[0]
        updated_file_name = processFileName(file_name)
        # Update the table with the modified file name
        cursor.execute("UPDATE PrintHistoryLinks SET update_date = ? WHERE file_name = ?",
                       (updated_file_name, file_name))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def processFileName(file_name):
    tmp = "temporary word replace"
    jan = "มกราคม"
    feb = "กุมภาพันธ์"
    mar = "มีนาคม"
    apr = "เมษายน"
    may = "พฤษภาคม"
    jun = "มิถุนายน"
    jul = "กรกฏาคม"
    aug = "สิงหาคม"
    sep = "กันยายน"
    oct = "ตุลาคม"
    nov = "พฤศจิกายน"
    dec = "ธันวาคม"

    file_name = file_name.replace("ใบแจ้งราคารับซื้อสินค้า วัน", '')
    file_name = file_name.replace("(ราคาค้าปลีก)", '')

    file_name = file_name.replace('ที่', tmp)

    if tmp in file_name:
        getDate = file_name[file_name.find(tmp) + len(tmp):]
        date = int(getDate[0:3])

        if re.search(jan, getDate):
            month = 1
        elif re.search(feb, getDate):
            month = 2
        elif re.search(mar, getDate):
            month = 3
        elif re.search(apr, getDate):
            month = 4
        elif re.search(may, getDate):
            month = 5
        elif re.search(jun, getDate):
            month = 6
        elif re.search(jul, getDate):
            month = 7
        elif re.search(aug, getDate):
            month = 8
        elif re.search(sep, getDate):
            month = 9
        elif re.search(oct, getDate):
            month = 10
        elif re.search(nov, getDate):
            month = 11
        elif re.search(dec, getDate):
            month = 12
        else:
            return None

        year = int(getDate[-5:]) - 543
        x = datetime.datetime(year, month, date).date()
        dataDate = x.strftime("%d-%m-%Y")
        return dataDate
    else:
        return None


# Add the update_date column and update it with processed file name dates
addUpdatedFileNameColumn()
updateFileNameColumn()
