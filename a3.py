#!/usr/bin/env python3
################################################################################
#
#   CSSE1001/7030 - Assignment 3
#
#   Student Username: s4378702
#
#   Student Name: Youwen Mao
#
################################################################################

# VERSION 1.0.0

################################################################################
#
# The following is support code. DO NOT CHANGE.

from a3_support import *

# End of support code
################################################################################
# Write your code below
################################################################################

# Write your classes here (including import statements, etc.)

class SimpleTileApp(object):
    def __init__(self, master):
        """
        Constructor(SimpleTileApp, tk.Frame)
        """
        self._master = master

        self._game = SimpleGame()

        self._game.on('swap', self._handle_swap)
        self._game.on('score', self._handle_score)

        self._grid_view = TileGridView(
            master, self._game.get_grid(),
            width=GRID_WIDTH, height=GRID_HEIGHT, bg='black')
        self._grid_view.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # Add your code here

    def _handle_swap(self, from_pos, to_pos):
        """
        Run when a swap on the grid happens.
        """
        print("SimplePlayer made a swap from {} to {}!".format(from_pos, to_pos))

    def _handle_score(self, score):
        """
        Run when a score update happens.
        """
        print("SimplePlayer scored {}!".format(score))

def task1():
    # Add task 1 GUI code here
    pass

def task2():
    # Add task 2 GUI code here
    pass

def task3():
    # Add task 3 GUI code here
    pass

def main():
    # Choose relevant task to run
    task1()


################################################################################
# Write your code above - NOTE you should define a top-level
# class (the application) called Breakout
################################################################################
if __name__ == '__main__':
    main()
