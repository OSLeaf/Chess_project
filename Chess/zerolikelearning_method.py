from MCST import MCTS
from Edges_and_nodes import Node, Edge
from chess_board import ML_Board
from output_dic import OUTPUTINDEX, REVERSEINDEX, INDEX
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tqdm import tqdm
import chess
from training_boards import TRAINING_BOARDS

class ReinfLearn():

    def __init__(self, turn_amount):
        #How many turns is the game played
        self.turn_amount = turn_amount

        #Setting starting position of the game
        self.g = ML_Board()


    def playGame(self, model1, model2):

        # the next three arrays collect the
        # positions, associated move probabilities
        # from the MCT search and the final outcome
        # for the game that we play
        positionsData = []
        moveProbsData = []
        valuesData = []

        # we play until we hit a final state
        while((not self.g.is_game_over()  and self.g.fullmove_number < self.turn_amount)):
            if self.g.turn == chess.WHITE:
                model = model1[0]
                #Do not let older models dictate learning parameters
                learn = model1[1]
            else:
                model = model2[0]
                #Do not let older models dictate learning parameters
                learn = model1[1]
            # Save the current position
            if learn:
                positionsData.append(np.array([self.g.convert_to_input().reshape(14, 64)]))

            # setup the MCT search
            rootEdge = Edge(None, None)
            rootEdge.N = 1
            rootNode = Node(self.g, rootEdge)
            mctsSearcher = MCTS(model, 20)
            moveProbs, min_prob = mctsSearcher.search(rootNode)

            # Mask illegal moves to 0 and sift all probabilities to positive.
            outputVec = np.array([ 0.0 for _ in range(INDEX)])
            for (move, prob) in moveProbs:
                move_idx = OUTPUTINDEX[str(move)]
                outputVec[move_idx] = prob - min_prob

            #Make sure that the probabilities sum to 1 and save it
            s = np.sum(outputVec)
            outputVec = np.array([x / s for x in outputVec])
            if learn:
                moveProbsData.append(outputVec)
            # in order to explore enough positions interpret the result of the MCT search
            # as a multinomial distribution and randomly select (w.r.t. the probabilites) a move
            try:
                rand_idx = np.random.multinomial(1, outputVec)
                nextMove = REVERSEINDEX[np.argmax(rand_idx)]
            except:
                rand_idx = np.argmax(outputVec)
                nextMove = REVERSEINDEX[rand_idx]
                
            self.g.push_san(nextMove)

            #Make a assumption that white wins untill proven otherwise at the end of the game.
            if learn:
                if(self.g.turn == chess.WHITE):
                    valuesData.append(1)
                else:
                    valuesData.append(-1)

        # we have reached a final state
        outcome = self.g.outcome()

        #If white won we do not need to change anything as it was an assumption. If black wins the values should be flipped and in case of a draw the value should be 0
        for i in range(0, len(moveProbsData)):
            if(outcome):
                if(outcome.winner == chess.WHITE):
                    valuesData[i] = valuesData[i] * 1.0
                elif(outcome.winner == chess.BLACK):
                    valuesData[i] = valuesData[i] * -1.0
                else:
                    valuesData[i] = valuesData[i] * 0.0
            else:
                if(self.g.final_calc() > 0):
                    valuesData[i] = valuesData[i] * (float(self.g.final_calc() * 100))
                elif(self.g.final_calc() < 0):
                    valuesData[i] = valuesData[i] * (float(self.g.final_calc() * 100))
                else:
                    valuesData[i] = valuesData[i] * 0.0

        #Remember to reset the board!
        self.g.reset()

        return positionsData, moveProbsData, valuesData
        
def main(load_path, save_path):
    #Load the training model and start iteration count
    model = keras.models.load_model(load_path + '.keras')
    modelVector = [model]
    ite = 0
    errors = 0

    #Train until told otherwise!
    while True:
        print("Training Iteration: " + str(ite))
        learner = ReinfLearn(40)
        allPos = []
        allMovProbs = []
        allValues = []
        #try:
        for j in tqdm(range(0, 1)):
            #Last three game played against earlier networks
            if j > 20:
                model2 = modelVector[np.random.randint(0, len(modelVector))]
                enemylearn = False
            else:
                model2 = model
                enemylearn = True

            #Played twice once with black and once with white
            for i in [((model, True) ,(model2, enemylearn)), ((model2, enemylearn), (model, True))]:
                pos, movProbs, values = learner.playGame(i[0], i[1])
                allPos += pos
                allMovProbs += movProbs
                allValues += values

        npPos = np.array(allPos)
        npProbs = np.array(allMovProbs)
        npVals = np.array(allValues)

        model.fit(npPos,[npProbs, npVals], epochs = 4, batch_size = 32, verbose = 0)
        '''except:
            f = open("log.txt", "a")
            f.write(str(errors) + ": " +str(ite) + "\n")
            errors += 1'''

        #Save every 20 iteration and make it a potential enemy network
        if(ite%200 == 0):
            model.save(save_path + str(ite) + '.keras')
            modelVector.append(keras.models.load_model(save_path + str(ite) + '.keras'))
        ite += 1

if __name__ == "__main__":
    main('Chess/networks/sd_deep3_1035', 'Chess/networks/d3_')
