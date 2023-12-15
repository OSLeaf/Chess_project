from hexapawn_board import Board
from Network_Objects import NeuralNetwork, Quesser
import tkinter as tk
from PIL import Image, ImageTk

        
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        self.game = Board()
        self.game.setStartingPosition()
        self.models = [Quesser(), NeuralNetwork('Hexapawn/networks/supervised_model.keras'), NeuralNetwork('Hexapawn/networks/model_it10.keras')]
        self.idx = int(input("Which bot: \n"))


        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=600, height=600, borderwidth=0, highlightthickness=0)
        
        self.canvas.pack(side="top", fill="both", expand="true")
        self.cellwidth = 200
        self.cellheight = 200

        self.rect = {}
        self.oval = {}
        for column in range(3):
            for row in range(3):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="grey", tags="rect")
                self.oval[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="grey", tags="oval")
                #img = tk.PhotoImage(file='images/blackpawn.png')
                #self.canvas.create_image((300, 300), image=img, anchor='n')

        #Gamelogick:
        self.draw()
        self.fromsquare = None
        def callback(event):
            if not self.game.isTerminal()[0]:
                if self.fromsquare == None:
                    self.fromsquare = (event.x //200 + (event.y //200)*3)
                else:
                    self.game.applyMove((self.fromsquare, (event.x //200 + (event.y //200)*3)))
                    if not self.draw_and_check_end():
                        self.models[self.idx].predict(self.game)
                        self.draw_and_check_end()
                    self.fromsquare = None

        self.canvas.bind("<Button-1>", callback)

    def draw(self):
        self.canvas.itemconfig("rect", fill="grey")
        self.canvas.itemconfig("oval", fill="grey")
        for pos, val in enumerate(self.game.getPosition()):
            if val == self.game.BLACK:
                item_id = self.oval[pos//3,pos%3]
                self.canvas.itemconfig(item_id, fill="black")
            elif val == self.game.WHITE:
                item_id = self.oval[pos//3,pos%3]
                self.canvas.itemconfig(item_id, fill="white")

    def draw_and_check_end(self):
        self.draw()
        if self.game.isTerminal()[0]:
            print("Winner (1: white 2: black): " + str(self.game.isTerminal()[1]))
            self.after(2000, lambda: self.destroy())
        return self.game.isTerminal()[0]

if __name__ == "__main__":
    app = App()
    app.mainloop()