import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import RandomizedSearchCV
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor

# Load preprocessed data containing 'price' and 'export' columns
data = pd.read_csv('preprocess_data.csv', usecols=['update_date', 'price', 'export'])

# Convert 'update_date' to datetime format and set it as the index
data['update_date'] = pd.to_datetime(data['update_date'])
data.set_index('update_date', inplace=True)

# Define the minimum and maximum dates from the update_date column
min_date = data.index.min()
max_date = data.index.max()

# Define the date ranges for training and testing based on the extracted dates
train_start_date = min_date
train_end_date = '2023-12-29'  # Specify an end date manually if needed
test_start_date = '2024-01-03'
test_end_date = max_date

# Filter the data for training and testing sets
train_data = data.loc[train_start_date:train_end_date]
test_data = data.loc[test_start_date:test_end_date]

# Optionally, scale the data using MinMaxScaler
# (Remember to fit the scaler only on the training data)
scaler = MinMaxScaler()
train_data_scaled = scaler.fit_transform(train_data)
test_data_scaled = scaler.transform(test_data)

# Define the number of time steps for LSTM
n_steps = 30  # Assuming you want to use the last 30 days' data to predict the next month

# Prepare data for LSTM with 'export' as a feature
X_train, y_train = [], []
for i in range(n_steps, len(train_data_scaled)):
    X_train.append(np.hstack((train_data_scaled[i - n_steps:i, :], train_data_scaled[i, 1:])))
    y_train.append(train_data_scaled[i, 0])  # Assuming 'price' is the first column (index 0)

X_train, y_train = np.array(X_train), np.array(y_train)


# Function to create LSTM model with 'export' as a feature
def create_model(units=50, dropout_rate=0.2):
    model = Sequential([
        LSTM(units=units, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
        Dropout(dropout_rate),
        LSTM(units=units, return_sequences=True),
        Dropout(dropout_rate),
        LSTM(units=units),
        Dropout(dropout_rate),
        Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


# Create KerasRegressor for RandomizedSearchCV
model = KerasRegressor(build_fn=create_model, epochs=100, batch_size=32, verbose=0)

# Define hyperparameters to tune
param_dist = {
    'units': [50, 100, 150],
    'dropout_rate': [0.2, 0.3, 0.4]
}

# Perform random search for hyperparameter tuning
random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist, cv=3, n_iter=5, verbose=2)
random_search.fit(X_train, y_train)

# Get best hyperparameters
best_params = random_search.best_params_
print("Best Hyperparameters:", best_params)

# Train the final model with best hyperparameters
final_model = create_model(units=best_params['units'], dropout_rate=best_params['dropout_rate'])
final_model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)

# Save the final model
final_model.save('final_model_with_export.h5')

# Optionally, evaluate the final model on the test data
# Evaluate the model on the test set
# X_test, y_test preparation is needed
# test_loss = final_model.evaluate(X_test, y_test)
# print("Test Loss:", test_loss)
