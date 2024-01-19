from stockfish import Stockfish
from chess_board import ML_Board
import numpy as np
import os
import glob
import time
import random
from pprint import pprint

stockfish = Stockfish(path=r"E:\Koulu\Chess_project\stockfish\stockfish-windows-x86-64-avx2.exe")

#save
def findNextIdx():
    files = (glob.glob(r"E:\Koulu\Chess_project\stockfish\games\*.npy"))
    if (len(files) == 0):
        return 1 #if no files, return 1
    highestIdx = 0
    for f in files:
        file = f
        currIdx = file.split("movesAndPositions")[-1].split(".npy")[0]
        highestIdx = max(highestIdx, int(currIdx))
    return int(highestIdx)+1

def saveData(gPos, gProb, gVal):
    movesAndPositions = np.array([gPos, gProb, gVal], dtype=object)
    nextIdx = findNextIdx()
    np.save(f"stockfish/games/movesAndPositions{nextIdx}.npy", movesAndPositions)


def mineGames():
    """mines numGames games of moves"""
    MAX_MOVES = 80 #don't continue games after this number
    it = 0
    while True:
        print(it)
        currentGameMoves = []
        board = ML_Board()
        stockfish.set_position(currentGameMoves)

        gPos = []
        gProb = []
        gVal = []

        for i in range(MAX_MOVES):
            #randomly choose from those 3 moves
            gPos.append(board.convert_to_input())
            gVal.append(stockfish.get_evaluation()['value'])
            moves = stockfish.get_top_moves(100)
            
            tempProb = []
            for i in moves:
                tempProb.append([i["Move"], i["Centipawn"]])
            gProb.append(tempProb)

            #if less than 3 moves available, choose first one, if none available, exit
            if (len(moves) == 0):
                print("game is over")
                break
            elif (len(moves) == 1):
                move = moves[0]["Move"]
            elif (len(moves) == 2):
                move = random.choices(moves, weights=(80, 20), k=1)[0]["Move"]
            elif (len(moves) == 3):
                move = random.choices(moves, weights=(80, 15, 5), k=1)[0]["Move"]
            elif (len(moves) == 4):
                move = random.choices(moves, weights=(70, 15, 10, 5), k=1)[0]["Move"]
            elif (len(moves) == 5):
                move = random.choices(moves, weights=(70, 10, 10, 5, 5), k=1)[0]["Move"]
            elif (len(moves) == 6):
                move = random.choices(moves, weights=(65, 10, 10, 5, 5, 5), k=1)[0]["Move"]
            else:
                nums = range(0, 7)
                move = moves[random.choices(nums, weights=(30, 20, 15, 10, 10, 10, 5), k=1)[0]]["Move"]

            board.push_san(move)
            currentGameMoves.append(move)
            stockfish.set_position(currentGameMoves)
            if (board.is_game_over()):
                print("game is over")
                break
        saveData(gPos, gProb, gVal)
        it += 1

mineGames()