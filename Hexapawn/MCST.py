import math
from Edges_and_nodes import Edge, Node
from hexapawn_board import Board
import random


class MCTS():
    def __init__(self, network):
        self.network = network
        self.rootNode = None
        self.tau = 1.0
        self.c_puct = 1.0

    def uctValues(self, edge: Edge, parentN):
        return self.c_puct * edge.P *(math.sqrt(parentN) / (1+ edge.N))
    
    def select(self, node: Node):
        if(node.isLeaf()):
            return node
        else:
            maxUctChild = None
            maxUctValue = -100000000
            for edge, child_node in node.childEdgeNode:
                uctVal = self.uctValues(edge, node.parentEdge.N)
                val = edge.Q
                if ( node.board.turn == Board.BLACK ):
                    val = -edge.Q
                uctValChild = val + uctVal
                if ( uctValChild > maxUctValue ):
                    maxUctChild = child_node
                    maxUctValue = uctValChild
            if (maxUctChild == None):
                raise ValueError("could not identify child with best uct value")
            else:
                return self.select(maxUctChild)
            
    def expandAndEvaluate(self, node: Node):
        terminal, winner = node.board.isTerminal()
        if(terminal == True):
            v = 0.0
            if (winner == Board.WHITE):
                v = 1.0
            else:
                v = -1.0
            self.backpropagate(v, node.parentEdge)
        else:
            v = node.expand(self.network)
            self.backpropagate(v, node.parentEdge)

    def backpropagate(self, v, edge: Edge):
        edge.N += 1
        edge.W += v
        edge.Q = edge.W / edge.N
        if(edge.parentNode != None):
            if(edge.parentNode.parentEdge != None):
                self.backpropagate(v, edge.parentNode.parentEdge)

    def search(self, rootNode: Node):
        self.rootNode = rootNode
        _ = self.rootNode.expand(self.network)
        for i in range(0, 100):
            selected_node = self.select(rootNode)
            self.expandAndEvaluate(selected_node)
        n_sum = 0
        moveProbs = []
        for (edge, _) in rootNode.childEdgeNode:
            n_sum += edge.N
        for (edge, node) in rootNode.childEdgeNode:
            prob = (edge.N ** (1 / self.tau)) / (n_sum ** (1 / self.tau))
            moveProbs.append((edge.move, prob, edge.N, edge.Q))
        return moveProbs

