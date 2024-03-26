import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load your data from the CSV file
data = pd.read_csv('cleanData.csv')

# Convert date column to datetime object, specifying dayfirst=True to silence the warning
data['date'] = pd.to_datetime(data['date'], dayfirst=True)

# Perform regression analysis
X = data['date'].astype('int64').values.reshape(-1, 1)  # Convert date to numerical values
y = data['price'].values.reshape(-1, 1)

model = LinearRegression()
model.fit(X, y)

# Predict prices for the dates in the dataset
predicted_prices = model.predict(X)

# Plotting
plt.scatter(data['date'], data['price'], color='blue', label='Actual Prices')
plt.plot(data['date'], predicted_prices, color='red', label='Predicted Prices')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Regression Analysis: อลูมิเนียมล้อแม็กซ์')
plt.legend()
plt.xticks(rotation=45)
plt.show()
