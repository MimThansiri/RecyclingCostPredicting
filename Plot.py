import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime

# Load the data
data = pd.read_csv('cleanData.csv')

# Convert 'date' column to datetime objects
data['date'] = pd.to_datetime(data['date'], format='%d-%m-%Y')

# Prepare the data
X_datetime = data['date']
y = data['price'].values

# Convert datetime to floating-point timestamps for model fitting (optional)
X_timestamp = X_datetime.apply(datetime.datetime.timestamp).values.reshape(-1, 1)

# Fit linear regression model
model = LinearRegression()
model.fit(X_timestamp, y)

# Predictions
y_pred = model.predict(X_timestamp)

# Plot
plt.scatter(X_datetime, y, color='blue', label='Data Points')
plt.plot(X_datetime, y_pred, color='red', label='Linear Regression')

plt.title('Linear Regression of Price over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
