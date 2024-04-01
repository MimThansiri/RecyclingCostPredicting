import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read CSV file into DataFrame, specifying thousands parameter
df = pd.read_csv('final_data.csv', thousands=',')

# Renaming the desired column
df.rename(columns={"('ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ราคา / หน่วย')": "price of aluminum can"}, inplace=True)

# Select desired columns
desired_columns = ["price of aluminum can", 'Set_Price', 'USD_Price', 'import', 'export', 'gdp', 'cpi']

selected_df = df[desired_columns]

# Calculate correlation matrix
correlation_matrix = selected_df.corr()

# Rename rows and columns with variable names
correlation_matrix = correlation_matrix.rename(index=dict(zip(correlation_matrix.index, desired_columns)),
                                               columns=dict(zip(correlation_matrix.columns, desired_columns)))

# Display or save the correlation matrix
print("Correlation Matrix:")
print(correlation_matrix)

# If you want to save the correlation matrix to a file
correlation_matrix.to_csv('correlation_matrix.csv')

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

# Save the heatmap as an image file
plt.savefig('heatmap_aluminum_can.png', dpi=300, bbox_inches='tight')

plt.show()
