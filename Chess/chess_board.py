import chess
import numpy as np

class ML_Board(chess.Board):

    def __init__(self, fen = chess.STARTING_FEN) -> None:
        super().__init__(fen)
    
    def final_calc(self):
        matrix = self.bitboards_as_array()
        return int(np.sum([np.sum(i) for i in matrix[:6]])) - int(np.sum([np.sum(i) for i in matrix[6:]]))
    
    def material_count_under_seven(self):
        piece_count = np.sum([np.sum(i) for i in self.bitboards_as_array()])
        if piece_count < 7:
            return True
        else:
            return False

    def convert_to_input(self):
        #8*8 vector for every piece type and color
        returnlist = self.bitboards_as_array()

        #8*8 plane of 1 or 0 to note the turn
        if (self.turn == chess.WHITE):
            returnlist = np.concatenate((returnlist, np.ones((2, 8, 8))), axis=0)
        else:
            returnlist = np.concatenate((returnlist, np.zeros((2, 8, 8))), axis=0)
        return returnlist

    def bitboards_as_array(self) -> np.ndarray:
        bb = self.bitboards()
        bb = np.asarray(bb, dtype=np.uint64)[:, np.newaxis]
        s = 8 * np.arange(7, -1, -1, dtype=np.uint64)
        b = (bb >> s).astype(np.uint8)
        b = np.unpackbits(b, bitorder="little")
        return b.reshape(-1, 8, 8)
    
    def bitboards(self):
        black, white = self.occupied_co
        return np.array([
            black & self.pawns,
            black & self.knights,
            black & self.bishops,
            black & self.rooks,
            black & self.queens,
            black & self.kings,
            white & self.pawns,
            white & self.knights,
            white & self.bishops,
            white & self.rooks,
            white & self.queens,
            white & self.kings,
        ], dtype=np.uint64)
    
    def convert_to_int(board):
        indices = '♚♛♜♝♞♟⭘♙♘♗♖♕♔'
        unicode = board.unicode()
        return [
            [indices.index(c)-6 for c in row.split()]
            for row in unicode.split('\n')
        ]

'''g = ML_Board()
print(g.final_calc())
print(g.bitboards_as_array().shape)
print(g.convert_to_input().shape)
print(g.material_count_under_seven())
l = ML_Board('k7/8/8/pppp4/8/8/8/7k')
print(l.material_count_under_seven())'''