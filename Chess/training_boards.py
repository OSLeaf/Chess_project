import random

TRAINING_BOARDS = []
TRAINING_BOARDS.append("8/3PP3/3k4/8/8/4K3/3pp3/8 w KQkq - 0 1")
TRAINING_BOARDS.append("k7/8/8/3pp3/3PP3/8/8/7K w KQkq - 0 1")
TRAINING_BOARDS.append("k7/8/8/1pp5/1PP5/8/8/7K w KQkq - 0 1")
TRAINING_BOARDS.append("k7/8/8/1pp5/5PP1/8/8/7K w KQkq - 0 1")
TRAINING_BOARDS.append("k7/8/8/2pppp2/2PPPP2/8/8/7K w KQkq - 0 1")
TRAINING_BOARDS.append("k7/8/2pppp2/2PPPP2/8/8/8/7K w KQkq - 0 1")
TRAINING_BOARDS.append("k7/8/8/8/2pppp2/2PPPP2/8/7K w KQkq - 0 1")
TRAINING_BOARDS.append("k7/8/8/3rr3/3RR3/8/8/7K w KQkq - 0 1")
TRAINING_BOARDS.append("k7/7P/8/3rr3/3RR3/8/p7/7K w KQkq - 0 1")
TRAINING_BOARDS.append("k7/7P/8/2rqqr2/2RQQR2/8/p7/7K w KQkq - 0 1")
TRAINING_BOARDS.append("8/8/rnbqkbnr/pppppppp/PPPPPPPP/RNBQKBNR/8/8 w KQkq - 0 1")

startingposition = list('rnbqbnrppppppppPPPPPPPPRNBQBNRp1')
random.shuffle(startingposition)
first_row = startingposition[:8]
second_row = startingposition[8:16]
third_row = startingposition[16:24]
forth_row = startingposition[24:]

TRAINING_BOARDS.append('kr6/pp6/' + ''.join(str(element) for element in first_row) + '/' + ''.join(str(element) for element in second_row) + '/' + ''.join(str(element) for element in third_row) + '/' + ''.join(str(element) for element in forth_row) + '/6PP/6RK w KQkq - 0 1')
TRAINING_BOARDS.append('kr6/' + ''.join(str(element) for element in first_row) + '/' + ''.join(str(element) for element in second_row) + '/8/8/' + ''.join(str(element) for element in third_row) + '/' + ''.join(str(element) for element in forth_row) + '/6RK w KQkq - 0 1')
TRAINING_BOARDS.append('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
TRAINING_BOARDS.append("8/PPPPPPPP/3k4/8/8/4K3/pppppppp/8 w KQkq - 0 1")