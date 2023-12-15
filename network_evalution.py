from hexapawn import Board
from Network_Objects import NeuralNetwork, Quesser

def Evaluate(game_amount, network1 = None, network2 = None):

    whiteWins = 0
    blackWins = 0

    for i in range(0,game_amount):

        board = Board()
        board.setStartingPosition()

        while(not board.isTerminal()[0]):
            if (board.turn == board.WHITE):
                network1.predict(board)
            else:
                network2.predict(board)
        _, winner = board.isTerminal()

        if(winner == board.WHITE):
            whiteWins += 1
        if(winner == board.BLACK):
            blackWins += 1

    all = whiteWins + blackWins
    
    print("Player1 vs Player2: "+'{0:.2f}'.format(whiteWins/all) + "/"+'{0:.2f}'.format(blackWins/all))

def main():
    #Model names: Quesser(), NeuralNetwork('networks/supervised_model.keras'), NeuralNetwork('networks/model_it10.keras')

    Evaluate(100, Quesser(), NeuralNetwork('networks/supervised_model.keras'))
    Evaluate(100, Quesser(), NeuralNetwork('networks/model_it10.keras'))
    Evaluate(100, NeuralNetwork('networks/supervised_model.keras'), Quesser())
    Evaluate(100, NeuralNetwork('networks/model_it10.keras'), Quesser())
    Evaluate(100, NeuralNetwork('networks/supervised_model.keras'), NeuralNetwork('networks/model_it10.keras'))

if __name__ == "__main__":
    main()