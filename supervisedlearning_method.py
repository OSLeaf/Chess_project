from hexapawn import Board
import tensorflow as tf
from tensorflow import keras
import numpy as np

model = keras.models.load_model("networks/random_model.keras")

inputData = np.load("trainingdata/positions.npy")
policyOutcomes = np.load("trainingdata/moveprobs.npy")
valuesOutcomes = np.load("trainingdata/outcomes.npy")

print(policyOutcomes.shape)

model.fit(inputData, [policyOutcomes, valuesOutcomes], epochs=512, batch_size=16)
model.save('networks/supervised_model.keras')