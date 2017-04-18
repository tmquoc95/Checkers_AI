
import copy
import random
import math
import GUI

# ======================== Class Player =======================================
class Player:
    def __init__(self, str_name):
        self.str = str_name
        self.firstTime = False

    def __str__(self):
        return self.str


    # Student MUST implement this function
    # The return value should be a move that is denoted by a list of tuples
    def nextMove(self, state):
        if not self.firstTime:
            self.firstTime = True
            self.gui = GUI.GUI_Thread(state)
        else:
            self.gui.updateBoard(state)

        result = []

        result = self.gui.getUserInput()
        return result

