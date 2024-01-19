from chess_board import ML_Board
from Network_Objects import NeuralNetwork, Quesser
import chess
import numpy as np
from training_boards import TRAINING_BOARDS

def Evaluate(game_amount, network1 = None, network2 = None):

    whiteWins = 0
    blackWins = 0
    draws = 0

    for i in range(0,game_amount):
        startingposition = list('rnbqbnrppppppppPPPPPPPPRNBQBNRp1')
        np.random.shuffle(startingposition)
        first_row = startingposition[:8]
        second_row = startingposition[8:16]
        third_row = startingposition[16:24]
        forth_row = startingposition[24:]
        #board = ML_Board('k7/pp6/' + ''.join(str(element) for element in first_row) + '/' + ''.join(str(element) for element in second_row) + '/' + ''.join(str(element) for element in third_row) + '/' + ''.join(str(element) for element in forth_row) + '/6PP/7K w KQkq - 0 1')
        board = ML_Board()
        for i in range(0, 10):
            l = []
            for m in board.generate_legal_moves():
                l.append(m)
            np.random.shuffle(l)
            m = l[0]
            board.push(m)
        '''boards = TRAINING_BOARDS
        np.random.shuffle(TRAINING_BOARDS)
        board = ML_Board(boards[0])'''

        while((not board.is_game_over() and not board.material_count_under_seven() and board.fullmove_number < 40)):
            if (board.turn == chess.WHITE):
                network1.predict(board)
            else:
                network2.predict(board)

        outcome = board.outcome()
        if(outcome):
            print(outcome)
            if(outcome.winner == chess.WHITE):
                whiteWins += 1
            elif(outcome.winner == chess.BLACK):
                blackWins += 1
            else:
                draws += 1
        else:
            if(board.final_calc() > 0):
                print(str(board.final_calc()))
                whiteWins += 1
            elif(board.final_calc() < 0):
                print(str(board.final_calc()))
                blackWins += 1
            else:
                draws += 1

    all = whiteWins + blackWins + draws
    
    print("Player1 vs Player2: "+'{0:.2f}'.format(whiteWins/all) + "/"+'{0:.2f}'.format(draws/all) + "/"+'{0:.2f}'.format(blackWins/all))

def main():
    #Model names: Quesser(), NeuralNetwork('Chess/networks/model_it??.keras')

    #Evaluate(100, network1=NeuralNetwork('Chess/networks/k280.keras'), network2=Quesser() )
    #Evaluate(100, network1=NeuralNetwork('Chess/networks/t180.keras'), network2=Quesser() )
    #Evaluate(100, network2=NeuralNetwork('Chess/networks/sd_deep2_500.keras'), network1=Quesser() )
    Evaluate(50, network1=NeuralNetwork('Chess/networks/sd_deep2_500.keras'), network2=NeuralNetwork('Chess/networks/sd_deep4_1035.keras') )
    #Evaluate(50, network2=NeuralNetwork('Chess/networks/sd_deep_500.keras'), network1=NeuralNetwork('Chess/networks/sd_deep_500.keras') )
    #Evaluate(100, network1=Quesser(), network2=NeuralNetwork('Chess/networks/GPT2_it100.keras') )
    

if __name__ == "__main__":
    main()