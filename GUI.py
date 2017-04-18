from tkinter import *
import threading

class GUI_Thread (threading.Thread):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.eventWaitingUserInput = threading.Event()
        self.eventWaitingUserInput.clear()
        self.moveList = []
        self.start()

    def run(self):
        self.root = Tk()

        red_man_img = PhotoImage(file="images/red_man.png")
        red_king_img = PhotoImage(file="images/red_king.png")
        black_man_img = PhotoImage(file="images/blue_man.png")
        black_king_img = PhotoImage(file="images/blue_king.png")
        empty_img = PhotoImage(file="images/empty.png")
        unused_img = PhotoImage(file="images/unused.png")

        self.imageMapping = {'r': red_man_img,
                        'b': black_man_img,
                        'R': red_king_img,
                        'B': black_king_img,
                        '.': empty_img,
                        'unused': unused_img
                        }

        self.lstObject = []
        self.setupBoard(self.board)
        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)

        self.root.mainloop()

    def onClosing(self):
        self.root.quit()



    def setupBoard(self, board):

        if board[0][0] == '.':
            self.remainder = 1
        else:
            self.remainder = 0

        for row in range(8):
            self.lstObject.append([])
            for col in range(8):
                if (col + row) % 2 == self.remainder:
                    self.lstObject[row].append(ButtonWrapper(self.root, row, col, board[row][col], self.moveList, self.imageMapping))
                else:
                    self.lstObject[row].append(Label(self.root, image=self.imageMapping['unused']))
                    self.lstObject[row][col].grid(column=col, row=row)

        self.buttonOK = Button(self.root, text='OK', command=self.buttonOK_onClick).grid(column=8, row=0)

    def getUserInput(self):

        del self.moveList[:]
        self.eventWaitingUserInput.set()
        while self.eventWaitingUserInput.is_set():
            pass

        return self.moveList

    def updateBoard(self, board):
        for row in range(8):
            for col in range(8):
                if (col + row) % 2 == self.remainder:
                    self.lstObject[row][col].type = board[row][col]
                    self.lstObject[row][col].updateImage()

    def buttonOK_onClick(self):
        self.eventWaitingUserInput.clear()



class ButtonWrapper:

    def __init__(self, root, row, col, type, moveList, imageMapping):

        self.button = Button(root, command=self.onClick)
        self.button.grid(column=col, row=row)
        self.col = col
        self.row = row
        self.type = type
        self.moveList = moveList
        self.imageMapping = imageMapping
        self.updateImage()


    def onClick(self):
        self.moveList.append((self.row, self.col))

    def updateImage(self):
        self.button['image'] = self.imageMapping[self.type]



