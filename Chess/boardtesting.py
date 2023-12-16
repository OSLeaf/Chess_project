import chess
import numpy as np
from chess_board import ML_Board

def convert_to_int(board):
    indices = '♚♛♜♝♞♟⭘♙♘♗♖♕♔'
    unicode = board.unicode()
    return [
        [indices.index(c)-6 for c in row.split()]
        for row in unicode.split('\n')
    ]

def convert_to_input1(board):
    returnlist = []
    i = convert_to_int(board)

    #8*8 vector for every piece type and color
    for l in range(-6, 7):
        for j in i:
            [returnlist.append(1) if (x == l and x != 0) else returnlist.append(0) for x in j]

    #8*8 plane of 1 or 0 to note the turn
    if (g.turn == chess.WHITE):
        t = 1
    else:
        t = 0
    for _ in range(8*8):
        returnlist.append(t)

    #8*8 for every castlingright
    castling = [0, 0, 0, 0]
    if bool(board.castling_rights & chess.BB_H1):
        castling[0] = 1
    if bool(board.castling_rights & chess.BB_A1):
        castling[1] = 1
    if bool(board.castling_rights & chess.BB_H8):
        castling[2] = 1
    if bool(board.castling_rights & chess.BB_A8):
        castling[3] = 1
    for i in castling:
        for _ in range(8*8):
            returnlist.append(i)

    print(returnlist)
    print(np.array(returnlist).shape)

def convert_to_input2(board):
    returnlist = []
    i = convert_to_int(board)

    #8*8 vector for every piece type and color
    for l in range(-6, 7):
        temp = []
        for j in i:
            temp.append([1 if (x == l and x != 0) else 0 for x in j])
        returnlist.append(temp)

    #8*8 plane of 1 or 0 to note the turn
    if (g.turn == chess.WHITE):
        t = 1
    else:
        t = 0
    temp = []
    for _ in range(8):
        temp.append([t for _ in range(8)])
    returnlist.append(temp)

    #8*8 for every castlingright
    castling = [0, 0, 0, 0]
    if bool(board.castling_rights & chess.BB_H1):
        castling[0] = 1
    if bool(board.castling_rights & chess.BB_A1):
        castling[1] = 1
    if bool(board.castling_rights & chess.BB_H8):
        castling[2] = 1
    if bool(board.castling_rights & chess.BB_A8):
        castling[3] = 1
    for i in castling:
        temp = []
        for _ in range(8):
            temp.append([i for _ in range(8)])
        returnlist.append(temp)

    print(returnlist)
    print(np.array(returnlist).shape)

def convert_to_input3(board):
    returnlist = []
    i = convert_to_int(board)

    #8*8 vector for every piece type and color
    for l in range(-6, 7):
        temp = []
        for j in i:
            [temp.append(1) if (x == l and x != 0) else temp.append(0) for x in j]
        returnlist.append(temp)

    #8*8 plane of 1 or 0 to note the turn
    temp = []
    if (g.turn == chess.WHITE):
        t = 1
    else:
        t = 0
    for _ in range(8*8):
        temp.append(t)
    returnlist.append(temp)

    #8*8 for every castlingright
    castling = [0, 0, 0, 0]
    if bool(board.castling_rights & chess.BB_H1):
        castling[0] = 1
    if bool(board.castling_rights & chess.BB_A1):
        castling[1] = 1
    if bool(board.castling_rights & chess.BB_H8):
        castling[2] = 1
    if bool(board.castling_rights & chess.BB_A8):
        castling[3] = 1
    for i in castling:
        temp = []
        for _ in range(8*8):
            temp.append(i)
        returnlist.append(temp)

    print(returnlist)
    print(np.array(returnlist).shape)

g = chess.Board()

'''for i in g.generate_legal_moves():
    print(i)

g.push_san("a2a4")
print("   ")

for i in g.generate_legal_moves():
    print(i)

g.push_san("b7b5")
print("   ")

for i in g.generate_legal_moves():
    print(i)

g.push_san("e2e3")
g.push_san("h7h6")
g.push_san("f1b5")
g.push_san("h6h5")
g.push_san("g1f3")
g.push_san("h5h4")
print("   ")
print("   ")
print("   ")
print(g)
for i in g.generate_legal_moves():
    print(i)
g.push_san("e1g1")
print(g)'''

convert_to_input1(g)
g.push_san("e2e3")
g.push_san("e7e6")
g.push_san("e1e2")
g.push_san("e8e7")
convert_to_input2(g)

l = ML_Board()

print(0.0874128341674804 + 0.026323556900024414 + 0.027813196182250977 + 0.0253298282623291 + 0.028309106826782227 + 0.02682018280029297 + 0.02582693099975586 + 0.0298001766204834 + 0.02880692481994629 + 0.02930307388305664 + 0.025826454162597656 - 0.3759770393371582)