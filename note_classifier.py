import json
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow.keras as keras
import matplotlib.pyplot as plt


DATASET_PATH = "./Notas/data.json"

def load_data(dataset_path):
  with open(dataset_path, "r") as fp:
    data = json.load(fp)
    
  #convert lists into numpy arrays
  inputs = np.array(data["mfcc"])
  targets = np.array(data["labels"])
  
  print("Data succesfully loaded!")
  
  return inputs, targets


def plot_history(history):
  
  fig, axs = plt.subplots(2)
  
  # create the accuracy subplots
  axs[0].plot(history.history["acc"], label="train accuracy")
  axs[0].plot(history.history["val_acc"], label="test accuracy")
  axs[0].set_ylabel("Accuracy")
  axs[0].legend(loc="lower right")
  axs[0].set_title("Accuracy eval")
  
   # create the error subplots
  axs[1].plot(history.history["loss"], label="train error")
  axs[1].plot(history.history["val_loss"], label="test error")
  axs[1].set_ylabel("Error")
  axs[1].set_xlabel("Epoch")
  axs[1].legend(loc="upper right")
  axs[1].set_title("Error eval")
  
  plt.show()
  


if __name__ == "__main__":
  #load data
  inputs, targets = load_data(DATASET_PATH)
  #split data into train and test sets
  inputs_train, inputs_test, targets_train, targets_test = train_test_split(inputs,
                                                                            targets,
                                                                            test_size=0.3)
  #build the network architecture

  model = keras.Sequential([
    # input layer
    keras.layers.Flatten(input_shape=(1, 40)),
    #1st hidden layer, relu = rectified linear unit. Relu - Better convergence, reduced likelihood of vanishing gradient
    keras.layers.Dense(1024, activation="relu",  kernel_regularizer=keras.regularizers.l2(0.001)),
    keras.layers.Dropout(0.3),
    #2st hidden layer
    keras.layers.Dense(512, activation="relu",  kernel_regularizer=keras.regularizers.l2(0.001)),
    keras.layers.Dropout(0.3),
    #3st hidden layer
    keras.layers.Dense(256, activation="relu", kernel_regularizer=keras.regularizers.l2(0.001)),
    keras.layers.Dropout(0.3),
    #4st hidden layer
    keras.layers.Dense(64, activation="relu", kernel_regularizer=keras.regularizers.l2(0.001)),
    keras.layers.Dropout(0.3),  
    # output layer, 12 neurons because we have 6 outputs ("C4", "C5", "D4", "D5", "E4", "E5")
    # softmax its a activation function, that normalize the values for us.
    keras.layers.Dense(12, activation="softmax"),
    
  ])
  
  #compile network
  optimiser = keras.optimizers.Adam(learning_rate=0.0001)
  model.compile(optimizer=optimiser,
                loss="sparse_categorical_crossentropy",
                metrics=["accuracy"])
  model.summary()
  
  #train network
  history = model.fit(inputs_train, targets_train,
            validation_data=(inputs_test, targets_test),
            batch_size=32,
            epochs=100)
  
  #plot the accuracy and eror over the epochs
  plot_history(history)