import tensorflow as tf
from tensorflow import keras
import numpy as np
from hexapawn import Board
import random

def rand_vs_net(board, network, _):
    record = []
    while(not board.isTerminal()[0]):
        if(board.turn == Board.WHITE):
            moves = board.generateMoves()
            m = moves[random.randint(0, len(moves)-1)]
            board.applyMove(m)
            record.append(m)
        else:
            q = network.predict(np.array([board.toNetworkInput()]), verbose = 0)
            masked_output = [ 0 for x in range(0,28)]
            for m in board.generateMoves():
                m_idx = board.getNetworkOutputIndex(m)
                masked_output[m_idx] = q[0][0][m_idx]
            best_idx = np.argmax(masked_output)
            sel_move = None
            for m in board.generateMoves():
                m_idx = board.getNetworkOutputIndex(m)
                if(best_idx == m_idx):
                    sel_move = m
            board.applyMove(sel_move)
            record.append(sel_move)
    _, winner = board.isTerminal()
    return winner

def rand_vs_rand(board, temp, temp2):
    while(not board.isTerminal()[0]):
        moves = board.generateMoves()
        m = moves[random.randint(0, len(moves)-1)]
        board.applyMove(m)
    _, winner = board.isTerminal()
    return winner

def net_vs_net(board: Board, network1, network2):
    while(not board.isTerminal()[0]):
        if (board.turn == board.WHITE):
            q = network1.predict(np.array([board.toNetworkInput()]), verbose = 0)
        else:
            q = network2.predict(np.array([board.toNetworkInput()]), verbose = 0)
        masked_output = [ 0 for x in range(0,28)]
        for m in board.generateMoves():
            m_idx = board.getNetworkOutputIndex(m)
            masked_output[m_idx] = q[0][0][m_idx]
        best_idx = np.argmax(masked_output)
        sel_move = board.getreverseNetworkOutputIndex(best_idx)
        board.applyMove(sel_move)
    _, winner = board.isTerminal()
    return winner

def net_vs_rand(board: Board, network, _):
    while(not board.isTerminal()[0]):
        if (board.turn == board.WHITE):
            q = network.predict(np.array([board.toNetworkInput()]), verbose = 0)
            masked_output = [ 0 for x in range(0,28)]
            for m in board.generateMoves():
                m_idx = board.getNetworkOutputIndex(m)
                masked_output[m_idx] = q[0][0][m_idx]
            best_idx = np.argmax(masked_output)
            sel_move = None
            for m in board.generateMoves():
                m_idx = board.getNetworkOutputIndex(m)
                if(best_idx == m_idx):
                    sel_move = m
            board.applyMove(sel_move)
        else:
            moves = board.generateMoves()
            m = moves[random.randint(0, len(moves)-1)]
            board.applyMove(m)
    _, winner = board.isTerminal()
    return winner

def Evaluate(game_amount, function, network1 = None, network2 = None):

    whiteWins = 0
    blackWins = 0

    for i in range(0,game_amount):
        board = Board()
        board.setStartingPosition()
        winner = function(board, network1, network2)
        if(winner == board.WHITE):
            whiteWins += 1
        if(winner == board.BLACK):
            blackWins += 1

    all = whiteWins + blackWins
    
    print("Player1 vs Player2: "+'{0:.2f}'.format(whiteWins/all) + "/"+'{0:.2f}'.format(blackWins/all))

def main():
    supervised = keras.models.load_model('networks/supervised_model.keras')
    unsupervised = keras.models.load_model('networks/model_it10.keras')

    Evaluate(100, net_vs_net, unsupervised, supervised)
    Evaluate(100, net_vs_rand, unsupervised)
    Evaluate(100, net_vs_rand, supervised)
    Evaluate(100, rand_vs_net, unsupervised)
    Evaluate(100, rand_vs_net, supervised)

if __name__ == "__main__":
    main()