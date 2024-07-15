import pandas as pd
from itertools import combinations

# Read CSV file into DataFrame, specifying thousands parameter
df = pd.read_csv('final_data.csv', thousands=',')

# Rename the desired column
df.rename(columns={"('ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ราคา / หน่วย')": "price of aluminum extrusion"}, inplace=True)

# Select desired columns
desired_columns = ["price of aluminum extrusion", 'Set_Price', 'USD_Price', 'import', 'export', 'gdp', 'cpi']

# Ensure the columns are numeric, coerce errors to NaN
df = df[desired_columns].apply(pd.to_numeric, errors='coerce')

# Initialize an empty DataFrame for interaction features
interaction_df = pd.DataFrame()

# Create interaction features
for col1, col2 in combinations(desired_columns, 2):
    interaction_df[f'{col1}_x_{col2}'] = df[col1] * df[col2]

# Save the DataFrame with interaction features to a CSV file
interaction_df.to_csv('price_of_aluminum_extrusion_with_interaction.csv', index=False)

print("Interaction features saved to 'price_of_aluminum_extrusion_with_interaction.csv'")