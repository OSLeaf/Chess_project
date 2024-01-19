from chess_board import ML_Board
from Network_Objects import NeuralNetwork, Quesser
import tkinter as tk
import random
from training_boards import TRAINING_BOARDS
import numpy as np
        
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        startingposition = list('rnbqbnrppppppppPPPPPPPPRNBQBNRp1')
        random.shuffle(startingposition)
        first_row = startingposition[:8]
        second_row = startingposition[8:16]
        third_row = startingposition[16:24]
        forth_row = startingposition[24:]

        self.game = ML_Board('kr6/pp6/' + ''.join(str(element) for element in first_row) + '/' + ''.join(str(element) for element in second_row) + '/' + ''.join(str(element) for element in third_row) + '/' + ''.join(str(element) for element in forth_row) + '/6PP/6RK w KQkq - 0 1')
        
        boards = TRAINING_BOARDS
        np.random.shuffle(TRAINING_BOARDS)
        self.game = ML_Board(boards[0])
        self.game = ML_Board()

        self.models = [Quesser(), NeuralNetwork('Chess/networks/sd_deep4_1035.keras')]
        self.idx = int(input("Which bot: \n"))
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=800, height=800, borderwidth=0, highlightthickness=0)
        
        self.canvas.pack(side="top", fill="both", expand="true")
        self.cellwidth = 100
        self.cellheight = 100

        self.rect = {}
        self.oval = {}
        for column in range(8):
            for row in range(8):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="grey", tags="rect")
                self.oval[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="grey", tags="oval")
                #img = tk.PhotoImage(file='images/blackpawn.png')
                #self.canvas.create_image((300, 300), image=img, anchor='n')

        #Gamelogick:
        print(self.game)
        #self.models[self.idx].predict(self.game)
        self.draw()
        self.fromsquare = None
        def callback(event):
            if not self.game.is_game_over():
                if self.fromsquare == None:
                    self.fromsquare = (self.letters[event.x //100] + str(8 -(event.y //100)))
                else:
                    self.game.push_san(self.fromsquare + self.letters[event.x //100] + str(8 - (event.y //100)))
                    if not self.draw_and_check_end():
                        self.models[self.idx].predict(self.game)
                        self.draw_and_check_end()
                    self.fromsquare = None
                    print(self.game)

        self.canvas.bind("<Button-1>", callback)

    def draw(self):
        self.canvas.itemconfig("rect", fill="grey")
        self.canvas.itemconfig("oval", fill="grey")
        for pos1, val1 in enumerate(self.game.convert_to_int()):
            for pos2, val2 in enumerate(val1):
                if val2 < 0:
                    item_id = self.oval[pos1,pos2]
                    self.canvas.itemconfig(item_id, fill="black")
                elif val2 > 0:
                    item_id = self.oval[pos1,pos2]
                    self.canvas.itemconfig(item_id, fill="white")

    def draw_and_check_end(self):
        self.draw()
        if self.game.is_game_over():
            print("Winner (1: white 2: black): " + str(self.game.outcome().winner))
            self.after(2000, lambda: self.destroy())
        return self.game.is_game_over()

if __name__ == "__main__":
    app = App()
    app.mainloop()