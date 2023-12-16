import chess

outputIndex = {}
reverseOutputIndex = {}

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
index = 0
for i in letters:
    for j in numbers:
        for k in letters:
            for h in numbers:
                from_square = i + str(j)
                to_square = k + str(h)
                if from_square != to_square:
                    outputIndex[from_square + to_square] = index
                    reverseOutputIndex[index] = from_square + to_square
                    index += 1
promotions = ['q', 'r', 'b', 'n']

for i in letters:
    for k in letters:
        for j in promotions:
            from_square = i + str(7)
            to_square = k + str(8)
            outputIndex[from_square + to_square + j] = index
            reverseOutputIndex[index] = from_square + to_square + j
            index += 1
            from_square = i + str(2)
            to_square = k + str(1)
            outputIndex[from_square + to_square + j] = index
            reverseOutputIndex[index] = from_square + to_square + j
            index += 1



class ML_Board(chess.Board):

    def makeIndexes(self):
        self.outputIndex = {}
        self.reverseOutputIndex = {}

        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        numbers = [1, 2, 3, 4, 5, 6, 7, 8]
        index = 0
        for i in letters:
            for j in numbers:
                for k in letters:
                    for h in numbers:
                        from_square = i + str(j)
                        to_square = k + str(h)
                        if from_square != to_square:
                            self.outputIndex[from_square + to_square] = index
                            self.reverseOutputIndex[index] = from_square + to_square
                            index += 1

    def getNetworkOutputIndex(self, move):
        return outputIndex[str(move)]
    
    def getreverseNetworkOutputIndex(self, move):
        return reverseOutputIndex[move]
    
    def final_calc(self, matrix):
        return sum([sum(i) for i in matrix])
    
    def material_count(self):
        temp = 0
        int_matrix = self.convert_to_int()
        for j in int_matrix:
            for i in j:
                if i != 0:
                    temp += 1
        if temp < 7:
            return self.final_calc(int_matrix)
        else:
            return -100
        


    def convert_to_int(self):
        indices = '♚♛♜♝♞♟⭘♙♘♗♖♕♔'
        unicode = self.unicode()
        return [
            [indices.index(c)-6 for c in row.split()]
            for row in unicode.split('\n')
        ]

    def convert_to_input(self):
        returnlist = []
        i = self.convert_to_int()

        #8*8 vector for every piece type and color
        for l in range(-6, 7):
            temp = []
            for j in i:
                temp.append([1 if (x == l and x != 0) else 0 for x in j])
            returnlist.append(temp)

        #8*8 plane of 1 or 0 to note the turn
        if (self.turn == chess.WHITE):
            t = 1
        else:
            t = 0
        temp = []
        for _ in range(8):
            temp.append([t for _ in range(8)])
        returnlist.append(temp)

        #8*8 for every castlingright
        castling = [0, 0, 0, 0]
        if bool(self.castling_rights & chess.BB_H1):
            castling[0] = 1
        if bool(self.castling_rights & chess.BB_A1):
            castling[1] = 1
        if bool(self.castling_rights & chess.BB_H8):
            castling[2] = 1
        if bool(self.castling_rights & chess.BB_A8):
            castling[3] = 1
        for i in castling:
            temp = []
            for _ in range(8):
                temp.append([i for _ in range(8)])
            returnlist.append(temp)
        return returnlist