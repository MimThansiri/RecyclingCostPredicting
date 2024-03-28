import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3


# Function to create a new column in the PrintHistoryLinks table
def add_column():
    db_connection = sqlite3.connect('RecyclingCost.db')
    cursor_col = db_connection.cursor()

    # Define the SQL query to add the file_name column to the PrintHistoryLinks table
    alter_query = "ALTER TABLE PrintHistoryLinks ADD COLUMN file_name TEXT"

    # Execute the query
    cursor_col.execute(alter_query)

    # Commit the changes
    db_connection.commit()

    # Close the cursor and connection
    cursor_col.close()
    db_connection.close()


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
    db_connection_out = sqlite3.connect('RecyclingCost.db')
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
    # print(nonferrous_metals)

    nonferrous_metals_title = nonferrous_metals.find_all('th')
    # print(nonferrous_metals_title)

    # nonferrous_metals_table_title = [title.text for title in nonferrous_metals_title]
    # print(nonferrous_metals_table_title)

    main_title = nonferrous_metals_title[0].text.strip()
    # print(main_title)

    subcategories = nonferrous_metals_title[1].text.strip()
    price = nonferrous_metals_title[2].text.strip()

    nonferrous_metals_values = nonferrous_metals.find_all('td')
    # print(nonferrous_metals_values)

    import re
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

    # Print str type list - sub
    # print("Subcategories values:")
    # for value in subcategories_value:
    # print(value)

    # Print float type list - price
    # print("\nPrice values:")
    # for value in price_value:
    # print(value)

    # Create a DataFrame with MultiIndex
    df_nonferrous_metals = pd.DataFrame(index=subcategories_value, columns=pd.MultiIndex.from_tuples(
        [(main_title, subcategories), (main_title, price)]))
    # Fill the DataFrame with values
    df_nonferrous_metals[(main_title, subcategories)] = subcategories_value
    df_nonferrous_metals[(main_title, price)] = price_value
    df_nonferrous_metals = df_nonferrous_metals.reset_index(drop=True)
    # Display the DataFrame
    # print(df_nonferrous_metals)

    # Create a connection to the SQLite database (if the database doesn't exist, it will be created)
    # db_connection = sqlite3.connect('WasteSQL.db')
    db_connection = sqlite3.connect('RecyclingCost.db')

    # Save the DataFrame to the database
    df_nonferrous_metals.to_sql(name=file_name, con=db_connection, if_exists='replace', index=False)

    # Close the connection
    db_connection.close()


# Add the file_name column to the PrintHistoryLinks table
add_column()

# Connect to the SQLite database
db_connection_outer = sqlite3.connect('RecyclingCost.db')

# Create a cursor object to execute SQL queries
cursor = db_connection_outer.cursor()

# Define the SQL query to retrieve URLs from the PrintHistoryLinks table
query = "SELECT link FROM PrintHistoryLinks"

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
