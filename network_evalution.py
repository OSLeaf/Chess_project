import tensorflow as tf
from tensorflow import keras
import numpy as np
from hexapawn import Board
import random


model = keras.models.load_model('networks/supervised_model.keras')

def fst(a):
    return a[0]

# white == random player
# black == network
def rand_vs_net(board):
    record = []
    while(not fst(board.isTerminal())):
        if(board.turn == Board.WHITE):
            moves = board.generateMoves()
            m = moves[random.randint(0, len(moves)-1)]
            board.applyMove(m)
            record.append(m)
        else:
            q = model.predict(np.array([board.toNetworkInput()]))
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
    terminal, winner = board.isTerminal()
    return winner

# white random player
# black random player
def rand_vs_rand(board):
    while(not fst(board.isTerminal())):
        moves = board.generateMoves()
        m = moves[random.randint(0, len(moves)-1)]
        board.applyMove(m)
    terminal, winner = board.isTerminal()
    return winner

def net_vs_net(board: Board):
    while(not fst(board.isTerminal())):
        q = model.predict(np.array([board.toNetworkInput()]))
        masked_output = [ 0 for x in range(0,28)]
        for m in board.generateMoves():
            m_idx = board.getNetworkOutputIndex(m)
            masked_output[m_idx] = q[0][0][m_idx]
        best_idx = np.argmax(masked_output)
        sel_move = board.getreverseNetworkOutputIndex(best_idx)
        board.applyMove(sel_move)
    terminal, winner = board.isTerminal()
    return winner

def net_vs_rand(board: Board):
    while(not fst(board.isTerminal())):
        if (board.turn == board.WHITE):
            q = model.predict(np.array([board.toNetworkInput()]))
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
    terminal, winner = board.isTerminal()
    return winner


whiteWins = 0
blackWins = 0

for i in range(0,100):
    board = Board()
    board.setStartingPosition()
    moves = board.generateMoves()
    m = moves[random.randint(0, len(moves)-1)]
    board.applyMove(m)
    winner = rand_vs_net(board)
    if(winner == board.WHITE):
        whiteWins += 1
    if(winner == board.BLACK):
        blackWins += 1

all = whiteWins + blackWins
print("Rand vs Net: "+str(whiteWins/all) + "/"+str(blackWins/all))


whiteWins = 0
blackWins = 0

for i in range(0,100):
    board = Board()
    board.setStartingPosition()
    moves = board.generateMoves()
    m = moves[random.randint(0, len(moves)-1)]
    board.applyMove(m)
    winner = rand_vs_rand(board)
    if(winner == board.WHITE):
        whiteWins += 1
    if(winner == board.BLACK):
        blackWins += 1

all = whiteWins + blackWins
print("Rand vs Rand: "+'{0:.2f}'.format(whiteWins/all) + "/"+'{0:.2f}'.format(blackWins/all))

whiteWins = 0
blackWins = 0

for i in range(0,100):
    board = Board()
    board.setStartingPosition()
    winner = net_vs_net(board)
    if(winner == board.WHITE):
        whiteWins += 1
    if(winner == board.BLACK):
        blackWins += 1

all = whiteWins + blackWins
print("Net vs Net: "+'{0:.2f}'.format(whiteWins/all) + "/"+'{0:.2f}'.format(blackWins/all))

whiteWins = 0
blackWins = 0

for i in range(0,100):
    board = Board()
    board.setStartingPosition()
    winner = net_vs_rand(board)
    if(winner == board.WHITE):
        whiteWins += 1
    if(winner == board.BLACK):
        blackWins += 1

all = whiteWins + blackWins
print("Net vs Rand: "+'{0:.2f}'.format(whiteWins/all) + "/"+'{0:.2f}'.format(blackWins/all))