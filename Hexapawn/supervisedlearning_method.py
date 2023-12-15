from hexapawn_board import Board
import tensorflow as tf
from tensorflow import keras
import numpy as np

def main(path):
    model = keras.models.load_model(path)

    inputData = np.load("Hexapawn/trainingdata/positions.npy")
    policyOutcomes = np.load("Hexapawn/trainingdata/moveprobs.npy")
    valuesOutcomes = np.load("Hexapawn/trainingdata/outcomes.npy")

    model.fit(inputData, [policyOutcomes, valuesOutcomes], epochs=512, batch_size=16, verbose = 0)
    model.save('Hexapawn/networks/supervised_model.keras')

if __name__ == "__main__":
    main("Hexapawn/networks/random_model.keras")