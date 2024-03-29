# -*- coding: utf-8 -*-
"""DNN_CBR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W6oBaAjcLHHmDmxJEn0jqaje3rBb1ocM
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
# from matplotlib.ticker import MaxNLocator
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from sklearn.model_selection import train_test_split
# from google.colab import files
# !pip install shap
# import shap

files.upload()
data = pd.read_csv("data_CBR.csv", sep=";")
dataset = data.values

np.take(dataset,np.random.permutation(dataset.shape[0]),axis=0,out=dataset)
input_data = dataset[:,0:6]
output_data = dataset[: ,6:9]
input_train, input_validation, output_train, output_validation = train_test_split(input_data, output_data, test_size=0.2)

def build_model():
  model = keras.Sequential([
    layers.Dense(3, activation="relu", input_shape=[6]),
    layers.Dense(8, activation="sigmoid"),
    layers.Dense(2),
    layers.Dense(3)])
  optimizer = tf.keras.optimizers.RMSprop(0.001)
  model.compile(loss="mse", optimizer=optimizer, metrics=["msle"])
  return model
model = build_model()
epochs = 6000
history = model.fit(input_train, output_train, epochs=epochs, validation_data=(input_validation, output_validation), verbose=0)
model.summary()

plt.plot(history.history["loss"], "r--", color="red", linewidth=1)
plt.plot(history.history["val_loss"], "r--", color="blue", linewidth=1)
plt.xlabel("Epoch")
plt.ylabel("Loss (Mean Squared Error)")
plt.legend(["Training", "Validation"], loc="upper right")
plt.grid(False)
if np.max(history.history["loss"]) > np.max(history.history["val_loss"]):
  max = np.max(history.history["loss"])
else:
  max = np.max(history.history["val_loss"])
def roundBy(max, base=10):
    return int(base * round(float(max)/base))
max = roundBy(max)
plt.ylim(0,max)
plt.xlim(0,epochs)
plt.gca().yaxis.set_major_formatter(ticker.EngFormatter())
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

plt.plot(history.history["msle"], "r--", color="red", linewidth=1)
plt.plot(history.history["val_msle"], "r--", color="blue", linewidth=1)
plt.xlabel("Epoch")
plt.ylabel("Mean Squared Logarithmic Error")
plt.legend(["Training", "Validation"], loc="upper right")
plt.grid(False)
if np.max(history.history["msle"]) > np.max(history.history["val_msle"]):
  max = np.max(history.history["msle"])
else:
  max = np.max(history.history["val_msle"])
def roundBy(max, base=10):
    return int(base * round(float(max)/base))
max = roundBy(max)
plt.ylim(0,max)
plt.xlim(0,epochs)
plt.gca().yaxis.set_major_formatter(ticker.EngFormatter())
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

explainer = shap.DeepExplainer(model, input_train)
shap_values = explainer.shap_values(input_validation)
shap.summary_plot(shap_values[0], plot_type = "bar", feature_names=["D10", "D30", "D50", "D60", "Cu", "Cc"], color="darkviolet")

shap.initjs()
shap.force_plot(explainer.expected_value[0].numpy(), shap_values[0][0], features=["D10", "D30", "D50", "D60", "Cu", "Cc"])

shap.decision_plot(explainer.expected_value[0].numpy(), shap_values[0][0], features=input_train[0,:], feature_names=["D10", "D30", "D50", "D60", "Cu", "Cc"])

shap.decision_plot(explainer.expected_value[0].numpy(), shap_values[0][0], features=input_validation[0,:], feature_names=["D10", "D30", "D50", "D60", "Cu", "Cc"])

shap.plots._waterfall.waterfall_legacy(explainer.expected_value[0].numpy(), shap_values[0][0], feature_names=["D10", "D30", "D50", "D60", "Cu", "Cc"])

#Case_Study
D10, D30, D50, D60 = 0.171, 0.462, 1.081, 1.445
Cu = D60/D10
Cc = (D30*D30)/(D10*D60)
results_size = np.zeros((1, 3))
results = np.zeros_like(results_size, dtype=float)
results[0, :] = model.predict(np.array([[D10, D30, D50, D60, Cu, Cc]]))
results = results[0]
print("The maximum dry unit weight is " + str(round(results[0],3)) + " kN/m3")
print("The optimum moisture content is " + str(round(results[1],3)) + " %")
print("The California bearing ratio is " + str(round(results[2],3)) + " %")
