import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime  # Import datetime module

# Load the data
data = pd.read_csv('cleanData.csv')

# Prepare the data
X = data['date'].apply(lambda x: datetime.datetime.strptime(x, "%d-%m-%Y").timestamp()).values.reshape(-1, 1)
y = data['price'].values

# Fit linear regression model
model = LinearRegression()
model.fit(X, y)

# Predictions
y_pred = model.predict(X)

# Plot
plt.scatter(X, y, color='blue', label='Data Points')
plt.plot(X, y_pred, color='red', label='Linear Regression')

plt.title('Linear Regression of Price over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
