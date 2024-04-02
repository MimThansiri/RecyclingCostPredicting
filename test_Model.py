import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# Load the trained model
model = load_model('finalja_model.h5')

# Load the preprocessed data containing 'price' and 'export' columns
preprocess_data = pd.read_csv('preprocess_data.csv', usecols=['update_date', 'price', 'export'])

# Convert 'update_date' to datetime format and set it as the index
preprocess_data['update_date'] = pd.to_datetime(preprocess_data['update_date'])
preprocess_data.set_index('update_date', inplace=True)

# Define the date range for the future predictions
future_start_date = '2024-03-25'
future_end_date = '2024-04-24'

# Create an empty DataFrame for future dates
future_dates = pd.date_range(start=future_start_date, end=future_end_date, freq='D')
future_data = pd.DataFrame(index=future_dates)

# Scale the 'price' column using MinMaxScaler
scaler = MinMaxScaler()
price_data = np.array(preprocess_data['price']).reshape(-1, 1)
price_data_scaled = scaler.fit_transform(price_data)

# Replace the 'price' column in the preprocess_data with the scaled 'price' data
preprocess_data['price'] = price_data_scaled

# Define the number of time steps for LSTM
n_steps = 30  # Assuming you want to use the last 30 days' data to predict the next month

# Prepare the data for LSTM
X_future = []
for i in range(n_steps, len(preprocess_data)):
    X_future.append(preprocess_data.iloc[i - n_steps:i].values)  # Using 'price' and 'export' as features

X_future = np.array(X_future)

# Make predictions using the trained model for existing data
predictions = model.predict(X_future)

# Reshape predictions to match the expected shape for inverse transformation
predictions = predictions.reshape(-1, 1)

# Inverse transform the predicted values to the original scale
predictions_transformed = scaler.inverse_transform(predictions)

# Print or use the predictions as needed
print(predictions_transformed)

# Now, let's predict for future dates
for i in range(len(future_dates)):
    last_n_days = preprocess_data[-n_steps:]
    last_n_days_reshaped = last_n_days.values.reshape((1, n_steps, 2))
    future_prediction = model.predict(last_n_days_reshaped)
    future_prediction_transformed = scaler.inverse_transform(future_prediction)
    print(future_prediction_transformed)
    # Append the prediction to the preprocess_data
    preprocess_data.loc[future_dates[i]] = [future_prediction[0, 0], np.nan]  # Assuming 'export' is the second column

# Plotting predicted prices against future dates
plt.figure(figsize=(10, 6))
plt.plot(preprocess_data.index, scaler.inverse_transform(preprocess_data['price'].values.reshape(-1, 1)),
         label='Predicted Prices')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Predicted Prices for Future Dates')
plt.legend()
plt.show()