from hexapawn import Board
import tensorflow as tf
from tensorflow import keras
import numpy as np

def main(path):
    model = keras.models.load_model(path)

    inputData = np.load("trainingdata/positions.npy")
    policyOutcomes = np.load("trainingdata/moveprobs.npy")
    valuesOutcomes = np.load("trainingdata/outcomes.npy")

    model.fit(inputData, [policyOutcomes, valuesOutcomes], epochs=512, batch_size=16, verbose = 0)
    model.save('networks/supervised_model.keras')

if __name__ == "__main__":
    main("networks/random_model.keras")