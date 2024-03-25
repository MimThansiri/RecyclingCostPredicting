import requests
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urljoin
import os

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


# Scrape links from the main page
scrape_links_from_page(base_url)

# Loop through the page numbers and scrape print history links
for page_num in range(1, 1491, 10):
    page_url = base_url + str(page_num)
    scrape_links_from_page(page_url)

# Extract and sort the numerical values following 'https://wongpanit.com/print_history_price/'
sorted_links = sorted(print_history_price_links, key=lambda x: int(x.split('/')[-1]))

# Create SQLite database file if it doesn't exist
db_filename = 'RecyclingCost.db'
if not os.path.exists(db_filename):
    conn = sqlite3.connect(db_filename)
    conn.close()

# Connect to the SQLite database
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Create a table to store the links if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS PrintHistoryLinks (
                    id INTEGER PRIMARY KEY,
                    link TEXT UNIQUE
                )''')

# Insert each link into the table
for link in enumerate(sorted_links, start=1):
    cursor.execute('''INSERT OR IGNORE INTO PrintHistoryLinks (id, link) VALUES (?, ?)''', link)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Links have been saved to the database ordered by the numerical values")
