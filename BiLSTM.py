import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import tensorflow as tf
keras = tf.keras

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
train_end_date = '2022-07-12'  # Specify an end date manually if needed
test_start_date = '2022-07-13'
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
n_steps = 30

# Prepare data for LSTM
X_train, y_train = [], []
for i in range(n_steps, len(train_data_scaled)):
    X_train.append(train_data_scaled[i - n_steps:i, :])  # Using 'price' and 'export' as features
    y_train.append(train_data_scaled[i, 0])  # Assuming 'price' is the first column (index 0)

X_train, y_train = np.array(X_train), np.array(y_train)

# Build the LSTM model with additional layers
model = Sequential([
    Bidirectional(LSTM(units=50, return_sequences=True), input_shape=(X_train.shape[1], X_train.shape[2])),
    Dropout(0.2),
    Bidirectional(LSTM(units=50, return_sequences=True)),
    Dropout(0.2),
    Bidirectional(LSTM(units=50, return_sequences=True)),  # Additional LSTM layer
    Dropout(0.2),
    Bidirectional(LSTM(units=50)),  # Additional LSTM layer
    Dropout(0.2),
    Dense(units=1)
])

# Compile the model with a different optimizer
opt = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=opt, loss='mean_squared_error')

# Define checkpoint to save the best model during training
checkpoint = ModelCheckpoint('best_model.h5', monitor='val_loss', verbose=1, save_best_only=True, mode='min')

# Define early stopping to stop training when the validation loss stops improving
early_stopping = EarlyStopping(monitor='val_loss', patience=10)

# Train the model with more epochs
history = model.fit(X_train, y_train, epochs=200, batch_size=32, validation_split=0.3, callbacks=[checkpoint])

# Save the final model
model.save('bilstm_model.h5')

# Optionally, evaluate the model on the test data
# Evaluate the model on the test set
# loss = model.evaluate(X_test, y_test)
# print("Test Loss:", loss)
