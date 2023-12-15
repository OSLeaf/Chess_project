import tensorflow as tf
from tensorflow import keras
from hexapawn import Board
import numpy as np
import random


class NeuralNetwork():

    def __init__(self, network) -> None:
        self.network = keras.models.load_model(network)

    def predict(self, board: Board):
        q = self.network.predict(np.array([board.toNetworkInput()]), verbose = 0)
        masked_output = [ 0 for x in range(0,28)]
        for m in board.generateMoves():
            m_idx = board.getNetworkOutputIndex(m)
            masked_output[m_idx] = q[0][0][m_idx]
        best_idx = np.argmax(masked_output)
        sel_move = board.getreverseNetworkOutputIndex(best_idx)
        board.applyMove(sel_move)

class Quesser():

    def __init__(self) -> None:
        pass

    def predict(self, board: Board):
        moves = board.generateMoves()
        m = moves[random.randint(0, len(moves)-1)]
        board.applyMove(m)