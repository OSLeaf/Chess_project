import math
import chess
from Edges_and_nodes import Edge, Node
import time


class MCTS():
    def __init__(self, network, search_calls):
        self.network = network
        self.rootNode = None
        self.tau = 1.0
        self.c_puct = 1.0
        self.seach_calls = search_calls

    def uctValues(self, edge: Edge, parent: Edge):
        return self.c_puct * edge.P *(math.sqrt(parent.N) / (1 + edge.N))
    
    def select(self, node: Node):
        if(node.isLeaf()):
            return node
        else:
            maxUctChild = None
            maxUctValue = -100000000
            for edge, child_node in node.childEdgeNode:
                uctVal = self.uctValues(edge, node.parentEdge)
                val = edge.Q
                if ( node.board.turn == chess.BLACK):
                    val = -edge.Q
                if (uctVal != None):
                    childUctVal = val + uctVal
                if ( childUctVal > maxUctValue ):
                    maxUctChild = child_node
                    maxUctValue = childUctVal
            if (maxUctChild == None):
                raise ValueError("could not identify child with best uct value")
            else:
                return self.select(maxUctChild)
            
    def expandAndEvaluate(self, node: Node):
        terminal = node.board.is_game_over()
        if terminal:
            if (node.board.outcome().winner == chess.WHITE):
                v = 1.0
            elif (node.board.outcome().winner == chess.BLACK):
                v = -1.0
            else:
                v = 0
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
        #First expansion
        self.rootNode = rootNode
        _ = self.rootNode.expand(self.network)

        #Select and search the best avenue of seach self.seach_calls times
        for i in range(self.seach_calls):
            selected_node = self.select(rootNode)
            self.expandAndEvaluate(selected_node)

        #Return the Q (average reward) values of each edge
        moveProbs = []
        min_prob = rootNode.childEdgeNode[0][0].Q
        for (edge, _) in rootNode.childEdgeNode:
            moveProbs.append((edge.move, edge.Q))
            if edge.Q < min_prob:
                min_prob = edge.Q
        return moveProbs, min_prob

