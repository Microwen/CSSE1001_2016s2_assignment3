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
from tkinter import messagebox

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

        menubar = tk.Menu(self._master,tearoff = 0)
        master.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Game", command = self.new_game)
        filemenu.add_command(label="Exit", command=self.quit)
        self._master.title("Simple Tile Game")
        self._master.geometry("600x600")
        self._simpleplayer = SimplePlayer()
        self._simplestausbar = SimpleStatusBar(self._master)
        self._simplestausbar.pack(side = tk.BOTTOM)
        self._topframe = tk.Frame(master)
        self._topframe.pack(side = tk.TOP)
        self._reset = tk.Button(self._topframe, text = 'Reset Status', command = self.reset)
        self._reset.pack()


    def new_game(self):
        if TileGridView.is_resolving:
            messagebox.showinfo(title="Resolving", message="The grid view is resolving")
        else:
            self._game.reset()
            self._grid_view.draw()

    def quit(self):
        ans = messagebox.askokcancel('Verify exit', "Really quit?")
        if ans:
            self._master.destroy()

    def reset(self):
        if TileGridView.is_resolving:
            messagebox.showinfo(title="Resolving", message="The grid view is resolving")
        else:
            self._simpleplayer.reset_score()
            self._simpleplayer.reset_swaps()
            self._simplestausbar.set_score(self._simpleplayer.get_score())
            self._simplestausbar.set_swap(self._simpleplayer.get_swaps())

    def _handle_swap(self, from_pos, to_pos):
        """
        Run when a swap on the grid happens.
        """
        self._simpleplayer.record_swap()
        self._simplestausbar.set_swap(self._simpleplayer.get_swaps())
        print("SimplePlayer made a swap from {} to {}!".format(from_pos, to_pos))

    def _handle_score(self, score):
        """
        Run when a score update happens.
        """
        self._simpleplayer.add_score(score)
        self._simplestausbar.set_score(self._simpleplayer.get_score())
        print("SimplePlayer scored {}!".format(score))

class SimplePlayer(object):
        def __init__(self):
            self._score = 0
            self._swap = 0
        def add_score(self, score):
            self._score += score
            print('add')
            return self._score
        def get_score(self):
            return self._score
        def reset_score(self):
            self._score = 0
        def record_swap(self):
            self._swap += 1
            return self._swap
        def get_swaps(self):
            return self._swap
        def reset_swaps(self):
            self._swap = 0

class SimpleStatusBar(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._status = tk.Frame(self)
        self._status.pack()
        self._score = tk.Label(self._status, text = 'Scores: 0')
        self._score.pack(side = tk.LEFT)
        self._swap = tk.Label(self._status, text = 'Swaps: 0')
        self._swap.pack(side = tk.RIGHT)

    def set_score(self,score):
        score = 'Scores: '+str(score)
        self._score.config(text = score)

    def set_swap(self,swap):
        swap = 'Swaps: '+str(swap)
        self._swap.config(text = swap)


class Character(object):
    def __init__(self,max_health):
        pass

    def get_max_health(self):
        pass

    def get_health(self):
        pass

    def lose_health(self, amount):
        pass

    def gain_health(self, amount):
        pass

    def reset_health(self):
        pass

class Enemy(Character):
    def __init__(self, type, max_health, attack):
        pass

    def get_type(self):
        pass

    def attack(self):
        pass

class Player(Character):
    def __init__(self, max_health, swaps_per_turn):
        pass

    def record_swap(self):
        pass

    def get_swaps(self):
        pass

    def reset_swaps(self):
        pass

    def attack(self, runs):
        pass

class VersusStatusBar(object):
    pass

class ImageTileGridView(object):
    pass

class SinglePlayerTileApp(object):
    pass

def task1():
    # Add task 1 GUI code here
    root = tk.Tk()
    app = SimpleTileApp(root)
    root.mainloop()
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
