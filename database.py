# import requests
# from bs4 import BeautifulSoup
# import sqlite3
# import pandas as pd
# from urllib.parse import urljoin
# import os
# import re
# from datetime import datetime
#
# # Base URL of the main page
# base_url = "https://wongpanit.com/list_history_price/"
#
# # List to store all print_history_price links
# print_history_price_links = []
#
# # Function to scrape links from a page
# def scrape_links_from_page(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     all_links = soup.find_all("a", href=True)
#     page_print_history_price_links = [urljoin(url, link_tag["href"]) for link_tag in all_links if "print_history_price" in link_tag["href"]]
#     print_history_price_links.extend(page_print_history_price_links)
#
# # Start with the base URL
# page_url = base_url
#
# while True:
#     scrape_links_from_page(page_url)
#     response = requests.get(page_url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     next_page_link = soup.find("a", rel="next")
#
#     if next_page_link is not None:
#         page_url = urljoin(page_url, next_page_link["href"])
#     else:
#         break
#
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
#                     file_name TEXT
#                 )''')
#
# # Insert each link into the table
# for id, link in enumerate(sorted_links, start=1):
#     cursor.execute('''INSERT OR IGNORE INTO PrintHistoryLinks (id, link) VALUES (?, ?)''', (id, link))
#
# # Commit changes and close the connection
# conn.commit()
# conn.close()
#
# print("Links have been saved to the database ordered by the numerical values")
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
#         getDate = file_name[file_name.find(tmp) + len(tmp):].strip()
#         date = int(re.search(r'\d+', getDate).group())
#
#         if jan in getDate:
#             month = 1
#         elif feb in getDate:
#             month = 2
#         elif mar in getDate:
#             month = 3
#         elif apr in getDate:
#             month = 4
#         elif may in getDate:
#             month = 5
#         elif jun in getDate:
#             month = 6
#         elif jul in getDate:
#             month = 7
#         elif aug in getDate:
#             month = 8
#         elif sep in getDate:
#             month = 9
#         elif oct in getDate:
#             month = 10
#         elif nov in getDate:
#             month = 11
#         elif dec in getDate:
#             month = 12
#         else:
#             return None
#
#         year = int(re.search(r'\d{4}', getDate).group()) - 543
#         x = datetime(year, month, date).date()
#         dataDate = x.strftime("%Y-%m-%d")
#         return dataDate
#     else:
#         return None
#
# # Function to scrape and process data from a given URL
# def process_url(url):
#     page = requests.get(url)
#     soup = BeautifulSoup(page.text, 'html.parser')
#
#     h1_element = soup.find('h1')
#     h1_text = h1_element.get_text(strip=True) if h1_element else None
#     file_name = processFileName(h1_text)
#     print(file_name)
#
#     db_connection_out = sqlite3.connect('data.db')
#     cursor_out = db_connection_out.cursor()
#
#     # Update the PrintHistoryLinks table with the h1 text
#     update_query = "UPDATE PrintHistoryLinks SET file_name = ? WHERE link = ?"
#     cursor_out.execute(update_query, (h1_text, url))
#     db_connection_out.commit()
#
#     nonferrous_metals = soup.find_all('table')[5]
#     nonferrous_metals_values = nonferrous_metals.find_all('td')
#
#     nonferrous_metals_all_values_list = []
#     for nonferrous_metals_value in nonferrous_metals_values:
#         h1_tag = nonferrous_metals_value.find('h1')
#         if h1_tag:
#             value = h1_tag.text.strip()
#             value_without_dash = re.sub(r'(\.-|\.$)', '', value)
#             nonferrous_metals_all_values_list.append(value_without_dash)
#
#     price_value = []
#     subcategories_value = []
#     for value in nonferrous_metals_all_values_list:
#         try:
#             float_value = float(value)
#             price_value.append(float_value)
#         except ValueError:
#             subcategories_value.append(value)
#
#     columns = ['ชนิดสินค้า', 'ราคา / Price']
#     df_nonferrous_metals = pd.DataFrame(list(zip(subcategories_value, price_value)), columns=columns)
#     df_nonferrous_metals['ประเภทโลหะที่มีค่าสูง / Nonferrous metals'] = 'Nonferrous metals'
#     df_nonferrous_metals = df_nonferrous_metals[['ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ชนิดสินค้า', 'ราคา / Price']]
#     df_nonferrous_metals = df_nonferrous_metals.reset_index(drop=True)
#
#     # Filter the DataFrame to include only specified items
#     items_to_include = ['อลูมิเนียมกระป๋องโค้ก', 'อลูมิเนียมแผ่นเพจ', 'อลูมิเนียมฉากขอบใหม่', 'อลูมิเนียมล้อแม็กช์']
#     df_filtered = df_nonferrous_metals[df_nonferrous_metals['ชนิดสินค้า'].isin(items_to_include)]
#
#     df_filtered.to_sql(name=file_name, con=db_connection_out, if_exists='replace', index=False)
#     db_connection_out.commit()
#     cursor_out.close()
#     db_connection_out.close()
#
# # Connect to the SQLite database
# db_connection_outer = sqlite3.connect('data.db')
# cursor = db_connection_outer.cursor()
# query = "SELECT link FROM PrintHistoryLinks ORDER BY id"
# cursor.execute(query)
# rows = cursor.fetchall()
# urls = [row[0] for row in rows]
# cursor.close()
# db_connection_outer.close()
#
# iteration_count = 0
# while urls:
#     iteration_count += 1
#     link = urls.pop(0)
#     process_url(link)
#
#     if not urls:
#         break
#
# print("Total iterations:", iteration_count)
#
#
# def remove_duplicates_and_reset_ids():
#     conn = sqlite3.connect('data.db')
#     cursor = conn.cursor()
#
#     # Remove duplicates based on file_name
#     cursor.execute('''DELETE FROM PrintHistoryLinks
#                       WHERE rowid NOT IN (
#                           SELECT MIN(rowid)
#                           FROM PrintHistoryLinks
#                           GROUP BY file_name
#                       )''')
#
#     # Create a new table with the same structure
#     cursor.execute('''CREATE TABLE PrintHistoryLinks_new (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         link TEXT UNIQUE,
#                         file_name TEXT
#                     )''')
#
#     # Copy data from the old table to the new table
#     cursor.execute('''INSERT INTO PrintHistoryLinks_new (link, file_name)
#                       SELECT link, file_name FROM PrintHistoryLinks ORDER BY id''')
#
#     # Drop the old table
#     cursor.execute('''DROP TABLE PrintHistoryLinks''')
#
#     # Rename the new table to the original name
#     cursor.execute('''ALTER TABLE PrintHistoryLinks_new RENAME TO PrintHistoryLinks''')
#
#     # Commit the changes and close the connection
#     conn.commit()
#     conn.close()
#
# # Call the function to remove duplicates and reset the IDs
# remove_duplicates_and_reset_ids()

import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
from urllib.parse import urljoin
import os
import re
from datetime import datetime

# Base URL of the main page
base_url = "https://wongpanit.com/list_history_price/"

# List to store all print_history_price links
print_history_price_links = []


# Function to scrape links from a page
def scrape_links_from_page(url, latest_url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_links = soup.find_all("a", href=True)
    page_print_history_price_links = [urljoin(url, link_tag["href"]) for link_tag in all_links if
                                      "print_history_price" in link_tag["href"]]

    for link in page_print_history_price_links:
        if link == latest_url:
            return False
        print_history_price_links.append(link)

    return True


# Get the latest URL from the PrintHistoryLinks table
def get_latest_url():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT link FROM PrintHistoryLinks ORDER BY id DESC LIMIT 1")
    latest_url = cursor.fetchone()[0]
    conn.close()
    return latest_url


# Start with the base URL
page_url = base_url
latest_url = get_latest_url()

while True:
    if not scrape_links_from_page(page_url, latest_url):
        break
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")
    next_page_link = soup.find("a", rel="next")

    if next_page_link is not None:
        page_url = urljoin(page_url, next_page_link["href"])
    else:
        break

sorted_links = sorted(print_history_price_links, key=lambda x: int(x.split('/')[-1]))


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
        getDate = file_name[file_name.find(tmp) + len(tmp):].strip()
        date = int(re.search(r'\d+', getDate).group())

        if jan in getDate:
            month = 1
        elif feb in getDate:
            month = 2
        elif mar in getDate:
            month = 3
        elif apr in getDate:
            month = 4
        elif may in getDate:
            month = 5
        elif jun in getDate:
            month = 6
        elif jul in getDate:
            month = 7
        elif aug in getDate:
            month = 8
        elif sep in getDate:
            month = 9
        elif oct in getDate:
            month = 10
        elif nov in getDate:
            month = 11
        elif dec in getDate:
            month = 12
        else:
            return None

        year = int(re.search(r'\d{4}', getDate).group()) - 543
        x = datetime(year, month, date).date()
        dataDate = x.strftime("%Y-%m-%d")
        return dataDate
    else:
        return None


# Function to scrape and process data from a given URL
def process_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    h1_element = soup.find('h1')
    h1_text = h1_element.get_text(strip=True) if h1_element else None
    file_name = processFileName(h1_text)
    print(file_name)

    db_connection_out = sqlite3.connect('data.db')
    cursor_out = db_connection_out.cursor()

    # Update the PrintHistoryLinks table with the h1 text
    update_query = "UPDATE PrintHistoryLinks SET file_name = ? WHERE link = ?"
    cursor_out.execute(update_query, (h1_text, url))
    db_connection_out.commit()

    nonferrous_metals = soup.find_all('table')[5]
    nonferrous_metals_values = nonferrous_metals.find_all('td')

    nonferrous_metals_all_values_list = []
    for nonferrous_metals_value in nonferrous_metals_values:
        h1_tag = nonferrous_metals_value.find('h1')
        if h1_tag:
            value = h1_tag.text.strip()
            value_without_dash = re.sub(r'(\.-|\.$)', '', value)
            nonferrous_metals_all_values_list.append(value_without_dash)

    price_value = []
    subcategories_value = []
    for value in nonferrous_metals_all_values_list:
        try:
            float_value = float(value)
            price_value.append(float_value)
        except ValueError:
            subcategories_value.append(value)

    columns = ['ชนิดสินค้า', 'ราคา / Price']
    df_nonferrous_metals = pd.DataFrame(list(zip(subcategories_value, price_value)), columns=columns)
    df_nonferrous_metals['ประเภทโลหะที่มีค่าสูง / Nonferrous metals'] = 'Nonferrous metals'
    df_nonferrous_metals = df_nonferrous_metals[
        ['ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ชนิดสินค้า', 'ราคา / Price']]
    df_nonferrous_metals = df_nonferrous_metals.reset_index(drop=True)

    # Filter the DataFrame to include only specified items
    items_to_include = ['อลูมิเนียมกระป๋องโค้ก', 'อลูมิเนียมแผ่นเพจ', 'อลูมิเนียมฉากขอบใหม่', 'อลูมิเนียมล้อแม็กช์']
    df_filtered = df_nonferrous_metals[df_nonferrous_metals['ชนิดสินค้า'].isin(items_to_include)]

    df_filtered.to_sql(name=file_name, con=db_connection_out, if_exists='replace', index=False)
    db_connection_out.commit()
    cursor_out.close()
    db_connection_out.close()


# Process new URLs and update the database
for link in sorted_links:
    process_url(link)
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT OR IGNORE INTO PrintHistoryLinks (link) VALUES (?)''', (link,))
    conn.commit()
    conn.close()

print("New URLs have been processed and added to the database.")


def remove_duplicates_and_reset_ids():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Remove duplicates based on file_name
    cursor.execute('''DELETE FROM PrintHistoryLinks
                      WHERE rowid NOT IN (
                          SELECT MIN(rowid)
                          FROM PrintHistoryLinks
                          GROUP BY file_name
                      )''')

    # Create a new table with the same structure
    cursor.execute('''CREATE TABLE PrintHistoryLinks_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        link TEXT UNIQUE,
                        file_name TEXT
                    )''')

    # Copy data from the old table to the new table
    cursor.execute('''INSERT INTO PrintHistoryLinks_new (link, file_name)
                      SELECT link, file_name FROM PrintHistoryLinks ORDER BY id''')

    # Drop the old table
    cursor.execute('''DROP TABLE PrintHistoryLinks''')

    # Rename the new table to the original name
    cursor.execute('''ALTER TABLE PrintHistoryLinks_new RENAME TO PrintHistoryLinks''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Call the function to remove duplicates and reset the IDs
remove_duplicates_and_reset_ids()

