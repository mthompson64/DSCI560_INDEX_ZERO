# Import necessary libraries
import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import os

# Fitting the ANN to the Training set
def create_model(X_train, y_train, batch_size, epochs):
    # create ANN model
    model = Sequential()
    # Defining the first layer of the model
    model.add(Dense(
        units=5, input_dim=X_train.shape[1], kernel_initializer='normal', activation='relu'))

    # Defining the Second layer of the model
    model.add(Dense(units=5, kernel_initializer='normal', activation='relu'))

    # The output neuron is a single fully connected node
    # Since we will be predicting a single number
    model.add(Dense(1, kernel_initializer='normal'))

    # Compiling the model
    model.compile(loss='mean_squared_error', optimizer='adam')

    # Fitting the ANN to the Training set
    model.fit(X_train, y_train, batch_size=batch_size,
              epochs=epochs, verbose=0)

    return model

# Save model to JSON and weights
def save_model(model, path):
    # Make sure the base path exists
    if not os.path.exists(path):
        os.makedirs(path)
    json_path = os.path.join(path, "ANN_model.json")
    weights_path = os.path.join(path, "ANN_model.h5")

    # Save model in json form
    model_json = model.to_json()

    with open(json_path, 'w') as json_file:
        json_file.write(model_json)
        json_file.close()

    # Save model weights to HDF5
    model.save_weights(weights_path)
    print("Saved model to disk")

# Load model from JSON and weights
def load_model(json_path, weights_path):
    # Load json and use model
    with open(json_path, "r") as json_file:
        loaded_model_json = json_file.read()
        json_file.close()

    loaded_model = model_from_json(loaded_model_json)

    # Load weights into the model
    loaded_model.load_weights(weights_path)
    print("Loaded model from disk")

    return loaded_model
