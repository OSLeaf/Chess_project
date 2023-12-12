from hexapawn import Board
import copy
import numpy as np

def minimax(board, depth, maximize):
    isTerminal, winner = board.isTerminal()
    if(isTerminal):
        if(winner == board.WHITE):
            return 1000
        if(winner == board.BLACK):
            return -1000
    moves = board.generateMoves()
    if(maximize):
        bestVal = -999999999999
        for move in moves:
            next = copy.deepcopy(board)
            next.applyMove(move)
            bestVal = max(bestVal, minimax(next, depth - 1, (not maximize)))
        return bestVal
    else:
        bestVal = 9999999999999
        for move in moves:
            next = copy.deepcopy(board)
            next.applyMove(move)
            bestVal = min(bestVal, minimax(next, depth - 1, (not maximize)))
        return bestVal          


def getBestMoveRes(board):
    bestMove = None
    bestVal = 1000000000
    if(board.turn == board.WHITE):
        bestVal = -1000000000
    for m in board.generateMoves():
        tmp = copy.deepcopy(board)
        tmp.applyMove(m)
        mVal = minimax(tmp, 30, tmp.turn == board.WHITE)
        if(board.turn == board.WHITE and mVal > bestVal):
            bestVal = mVal
            bestMove = m
        if(board.turn == board.BLACK and mVal < bestVal):
            bestVal = mVal
            bestMove = m
    return bestMove, bestVal

positions = []
moveProbs = []
outcomes = []

terminals = []

def visitNodes(board):
    term, _ = board.isTerminal()
    if(term):
        terminals.append(1)
        return
    else:
        bestMove, bestVal = getBestMoveRes(board)
        positions.append(board.toNetworkInput())
        moveProb = [ 0 for x in range(0,28) ]
        idx = board.getNetworkOutputIndex(bestMove)
        moveProb[idx] = 1
        moveProbs.append(moveProb)
        if(bestVal > 0):
            outcomes.append(1)
        if(bestVal == 0):
            outcomes.append(0)
        if(bestVal < 0):
            outcomes.append(-1)
        for m in board.generateMoves():
            next = copy.deepcopy(board)
            next.applyMove(m)
            visitNodes(next)

board = Board()
board.setStartingPosition()
visitNodes(board)

np.save("trainingdata/positions", np.array(positions))
np.save("trainingdata/moveprobs", np.array(moveProbs))
np.save("trainingdata/outcomes", np.array(outcomes))