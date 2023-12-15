from hexapawn_board import Board
import copy
import numpy as np

class Edge():
    def __init__(self, move, parentNode):
        self.parentNode = parentNode
        self.move = move
        self.N = 0
        self.W = 0
        self.Q = 0
        self.P = 0

class Node():
    def __init__(self, board: Board, parentEdge: Edge):
        self.board = board
        self.parentEdge = parentEdge
        self.childEdgeNode = []

    def expand(self, network):
        moves = self.board.generateMoves()
        for m in moves:
            child_board = copy.deepcopy(self.board)
            child_board.applyMove(m)
            child_edge = Edge(m, self)
            child_node = Node(child_board, child_edge)
            self.childEdgeNode.append((child_edge, child_node))
        q = network.predict(np.array([self.board.toNetworkInput()]), verbose = 0)
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


