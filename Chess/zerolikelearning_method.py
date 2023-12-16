from MCST import MCTS
from Edges_and_nodes import Node, Edge
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tqdm import tqdm
from chess_board import ML_Board
import chess
import time

class ReinfLearn():

    def __init__(self, model):
        self.model = model

    def playGame(self):

        # the next three arrays collect the
        # positions, associated move probabilities
        # from the MCT search and the final outcome
        # for the game that we play
        positionsData = []
        moveProbsData = []
        valuesData = []

        # set up a game with the starting position
        g = ML_Board()
        g.makeIndexes()

        # we play until we hit a final state
        while((not g.is_game_over() and g.material_count() == -100)):
            #print(g)
            #print("----------------")
            #start_time = time.time()
            # encode the current position to the
            # network input format
            positionsData.append(g.convert_to_input())
            # setup the MCT search
            rootEdge = Edge(None, None)
            rootEdge.N = 1
            rootNode = Node(g, rootEdge)
            mctsSearcher = MCTS(self.model)
            moveProbs = mctsSearcher.search(rootNode)
            # MCT search return move probabilities for
            # all legal moves. To get an output vector
            # we need to consider all (incl. illegal) moves
            # but mask illegal moves to a probability of zero
            outputVec = [ 0.0 for x in range(0, 4544)]
            for (move, prob, _, _) in moveProbs:
                move_idx = g.getNetworkOutputIndex(move)
                outputVec[move_idx] = prob
            # in order to explore enough positions
            # we interpret the result of the MCT search
            # as a multinomial distribution and randomly
            # select (w.r.t. the probabilites) a move
            rand_idx = np.random.multinomial(1, outputVec)
            idx = np.where(rand_idx==1)[0][0]
            nextMove = g.getreverseNetworkOutputIndex(idx)
            # now we iterate through all legal moves
            # in order to find the one corresponding
            # to the randomly selected index
            if(g.turn == chess.WHITE):
                valuesData.append(1)
            else:
                valuesData.append(-1)
            moveProbsData.append(outputVec)
            g.push_san(nextMove)
            #print("--- %s seconds --- for the whole thing ------------------------" % (time.time() - start_time))

        # we have reached a final state
        winner = g.outcome()
        if winner == None:
            if g.material_count() > 0:
                winner = chess.WHITE
            else:
                winner = chess.BLACK
        else:
            winner = g.outcome().winner
        for i in range(0, len(moveProbsData)):
            if(winner == chess.BLACK):
                valuesData[i] = valuesData[i] * -1.0
            if(winner == chess.WHITE):
                valuesData[i] = valuesData[i] * 1.0
        return (positionsData, moveProbsData, valuesData)
        
def main(path):
    model = keras.models.load_model(path)
    mctsSearcher = MCTS(model)
    learner = ReinfLearn(model)
    for i in (range(0, 11)):
        print("Training Iteration: " + str(i))
        allPos = []
        allMovProbs = []
        allValues = []
        for j in tqdm(range(0, 10)):
            pos, movProbs, values = learner.playGame()
            allPos += pos
            allMovProbs += movProbs
            allValues += values
        npPos = np.array(allPos)
        npProbs = np.array(allMovProbs)
        npVals = np.array(allValues)
        model.fit(npPos,[npProbs, npVals], epochs = 256, batch_size = 16, verbose = 0)
        if(i%10 == 0):
            model.save('Chess/networks/model_it' + str(i) + '.keras')

if __name__ == "__main__":
    main('Chess/networks/model_it0.keras')
