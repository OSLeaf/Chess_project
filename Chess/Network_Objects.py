import tensorflow as tf
from tensorflow import keras
from chess_board import ML_Board
import numpy as np
from Edges_and_nodes import Node, Edge
from MCST import MCTS
from output_dic import OUTPUTINDEX, REVERSEINDEX, INDEX

class NeuralNetwork():

    def __init__(self, network) -> None:
        self.network = keras.models.load_model(network)

    def predict(self, board: ML_Board):
        '''rootEdge = Edge(None, None)
        rootEdge.N = 1
        rootNode = Node(board, rootEdge)
        mctsSearcher = MCTS(self.network, 10)
        moveProbs, min_Q = mctsSearcher.search(rootNode)

        outputVec = [ 0.0 for x in range(INDEX)]
        for (move, prob) in moveProbs:
            move_idx = OUTPUTINDEX[str(move)]
            outputVec[move_idx] = prob
        
        nextMove = REVERSEINDEX[np.argmax(outputVec)]
        board.push_san(nextMove)'''
        #print(board)
        
        q = self.network.predict(np.array([board.convert_to_input()]), verbose = 0)
        masked_output = [ 0 for x in range(INDEX)]
        for m in board.generate_legal_moves():
            m_idx = OUTPUTINDEX[str(m)]
            masked_output[m_idx] = q[0][0][m_idx]
        best_idx = np.argmax(masked_output)
        sel_move = REVERSEINDEX[best_idx]
        board.push_san(sel_move)
        #print(board)

class Quesser():

    def __init__(self) -> None:
        pass

    def predict(self, board: ML_Board):
        list = []
        for m in board.generate_legal_moves():
            list.append(m)
        m = list[np.random.randint(0, len(list))]
        board.push(m)
        #print(board)


'''a = keras.models.load_model("Chess/networks/test0.keras")
g = ML_Board()
c = a.predict(np.array([g.convert_to_input()]), verbose = 0)
b = []
for i in range(INDEX):
    b.append(c[0][0][i])
print(len(b))'''