import copy
import numpy as np
from chess_board import ML_Board
import time

class Edge():
    def __init__(self, move, parentNode):
        self.parentNode = parentNode
        self.move = move
        self.N = 0
        self.W = 0
        self.Q = 0
        self.P = 0

class Node():
    def __init__(self, board: ML_Board, parentEdge: Edge):
        self.board = board
        self.parentEdge = parentEdge
        self.childEdgeNode = []

    def expand(self, network):
        moves = self.board.generate_legal_moves()
        for m in moves:
            child_board = copy.deepcopy(self.board)
            child_board.push(m)
            child_edge = Edge(m, self)
            child_node = Node(child_board, child_edge)
            self.childEdgeNode.append((child_edge, child_node))
        #start_time = time.time()  
        q = network.predict(np.array([self.board.convert_to_input()]), verbose = 0)
        #print("--- %s seconds ---" % (time.time() - start_time))
        prob_sum = 0
        for (edge,_) in self.childEdgeNode:
            m_idx = self.board.getNetworkOutputIndex(edge.move)
            edge.P = q[0][0][m_idx]
            prob_sum += edge.P
        for (edge,_) in self.childEdgeNode:
            edge.P /= prob_sum
        v = q[1][0][0]
        return v
    
    def isLeaf(self) -> bool:
        return self.childEdgeNode == []


