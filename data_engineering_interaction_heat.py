import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations

# Read CSV file into DataFrame, specifying thousands parameter
df = pd.read_csv('final_data.csv', thousands=',')

# Rename the desired column
df.rename(columns={"('ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ราคา / หน่วย')": "price of aluminum extrusion"}, inplace=True)

# Select desired columns
desired_columns = ["price of aluminum extrusion", 'Set_Price', 'USD_Price', 'import', 'export', 'gdp', 'cpi']

# Ensure the columns are numeric, coerce errors to NaN
df = df[desired_columns].apply(pd.to_numeric, errors='coerce')

# Calculate correlation matrix
correlation_matrix = df.corr()

# Initialize an empty DataFrame for interaction features
interaction_df = pd.DataFrame()

# Create heatmap with seaborn
plt.figure(figsize=(10, 8))
heatmap = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")

# Set title and labels
plt.title('Correlation Matrix of Selected Columns')
plt.xlabel('Variables')
plt.ylabel('Variables')

# Set x-axis and y-axis tick labels font size
heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=45, ha='right', fontsize=10)
heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=0, fontsize=10)

# Threshold for creating interaction features based on heatmap value
threshold = 0.5

# Create interaction features for pairs with correlation > threshold
for col1, col2 in combinations(desired_columns, 2):
    if correlation_matrix.loc[col1, col2] > threshold:
        interaction_df[f'{col1}_x_{col2}'] = df[col1] * df[col2]

# Save the interaction DataFrame to a CSV file if there are features
if not interaction_df.empty:
    interaction_df.to_csv('price_of_aluminum_extrusion_with_interaction_heat.csv', index=False)
    print("Interaction features saved to 'price_of_aluminum_extrusion_with_interaction_heat'")
else:
    print("No interaction features met the threshold criteria.")

