import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# Load the trained model
model = load_model('final_model.h5')

# Load the preprocessed test data containing 'price' and 'export' columns
test_data = pd.read_csv('preprocess_data.csv', usecols=['update_date', 'price', 'export'])

# Convert 'update_date' to datetime format and set it as the index
test_data['update_date'] = pd.to_datetime(test_data['update_date'])
test_data.set_index('update_date', inplace=True)

# Define the date range for the test data
test_start_date = '2022-07-13'
test_end_date = '2024-03-23'

# Filter the test data based on the specified date range
test_data = test_data.loc[test_start_date:test_end_date]

# Scale the 'price' column using MinMaxScaler
scaler = MinMaxScaler()
price_data = np.array(test_data['price']).reshape(-1, 1)
price_data_scaled = scaler.fit_transform(price_data)

# Replace the 'price' column in the test data with the scaled 'price' data
test_data_scaled = test_data.copy()
test_data_scaled['price'] = price_data_scaled

# Define the number of time steps for LSTM
n_steps = 30  # Assuming you want to use the last 30 days' data to predict the next month

# Prepare the test data for LSTM
X_test, y_test = [], []
for i in range(n_steps, len(test_data_scaled)):
    X_test.append(test_data_scaled.iloc[i - n_steps:i].values)  # Using 'price' and 'export' as features
    y_test.append(test_data_scaled.iloc[i, 0])  # Assuming 'price' is the first column (index 0)

X_test, y_test = np.array(X_test), np.array(y_test)

# Make predictions using the trained model
predictions = model.predict(X_test)

# Reshape predictions to match the expected shape for inverse transformation
predictions = predictions.reshape(-1, 1)

# Inverse transform the predicted values to the original scale
predictions_transformed = scaler.inverse_transform(predictions)

# Print or use the predictions as needed
print(predictions_transformed)

# Extract actual prices from the test data
actual_prices = test_data['price'].values[n_steps:]

# Compare predicted prices with actual prices
mse = np.mean((predictions_transformed.flatten() - actual_prices) ** 2)
mae = np.mean(np.abs(predictions_transformed.flatten() - actual_prices))
print("Mean Squared Error (MSE):", mse)
print("Mean Absolute Error (MAE):", mae)

# Plotting predicted prices against actual prices
plt.figure(figsize=(10, 6))
plt.plot(test_data.index[n_steps:], actual_prices, label='Actual Prices')
plt.plot(test_data.index[n_steps:], predictions_transformed, label='Predicted Prices')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Actual vs. Predicted Prices')
plt.legend()
plt.show()
