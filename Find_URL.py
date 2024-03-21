import requests
from bs4 import BeautifulSoup
import sqlite3

# Base URL of the main page
base_url = "https://wongpanit.com/list_history_price/"

# List to store all print_history_price links
print_history_price_links = []

# Loop through the page numbers
for page_num in range(1, 1491, 10):
    # Construct the URL for the current page
    main_page_url = base_url + str(page_num)

    # Send a GET request to the current page
    response = requests.get(main_page_url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all links on the page
    all_links = soup.find_all("a", href=True)

    # Filter the links that contain "print_history_price"
    page_print_history_price_links = [
        link["href"] for link in all_links if "print_history_price" in link["href"]
    ]

    # Extend the list of print_history_price links
    print_history_price_links.extend(page_print_history_price_links)

# Print all print_history_price links
# for link in print_history_price_links:
#     # print(link)

len(print_history_price_links)

# Connect to the SQLite database
conn = sqlite3.connect('WasteSQL.db')
cursor = conn.cursor()

# Create a table to store the links
cursor.execute('''CREATE TABLE IF NOT EXISTS PrintHistoryLinks (
                    id INTEGER PRIMARY KEY,
                    link TEXT
                )''')

# Insert each link into the table
for link in print_history_price_links:
    cursor.execute('''INSERT INTO PrintHistoryLinks (link) VALUES (?)''', (link,))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Links have been saved to the database.")
