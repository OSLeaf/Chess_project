OUTPUTINDEX = {}
REVERSEINDEX = {}

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
INDEX = 0
for i in letters:
    for j in numbers:
        for k in letters:
            for h in numbers:
                from_square = i + str(j)
                to_square = k + str(h)
                if from_square != to_square:
                    OUTPUTINDEX[from_square + to_square] = INDEX
                    REVERSEINDEX[INDEX] = from_square + to_square
                    INDEX += 1

promotions = ['q', 'r', 'b', 'n']
for i, _ in enumerate(letters):
    for j in promotions:
        for num in [('7', '8'), ('2', '1')]:
            from_square = letters[i] + str(num[0])
            to_squares = []
            if letters[i] != 'a':
                to_squares.append(letters[i - 1] + num[1])
            if letters[i] != 'h':
                to_squares.append(letters[i + 1] + num[1])
            to_squares.append(letters[i] + num[1])
            for to in to_squares:
                OUTPUTINDEX[from_square + to + j] = INDEX
                REVERSEINDEX[INDEX] = from_square + to + j
                INDEX += 1

#print(INDEX)
                