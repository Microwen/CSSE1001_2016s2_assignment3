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

        self._simpleplayer = SimplePlayer()
        self._simplestausbar = SimpleStatusBar(self._master)
        self._simplestausbar.pack(side = tk.BOTTOM)

        self._topframe = tk.Frame(master)
        self._topframe.pack(side = tk.TOP)

        self._reset = tk.Button(self._topframe, text = 'Reset Status', command = self.reset)
        self._reset.pack()


    def new_game(self):
        if self._grid_view.is_resolving():
            messagebox.showinfo(title="Resolving", message="The grid view is resolving")
        else:
            self._game.reset()
            self._grid_view.draw()

            self._simpleplayer.reset_score()
            self._simplestausbar.set_score(self._simpleplayer.get_score())

            self._simpleplayer.reset_swaps()
            self._simplestausbar.set_swap(self._simpleplayer.get_swaps())

    def quit(self):
        ans = messagebox.askokcancel('Exit', "Do you want to quit?")
        if ans:
            self._master.destroy()

    def reset(self):
        if self._grid_view.is_resolving():
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
        self._status.pack(ipadx= 100)

        self._score = tk.Label(self._status, text = SCORE_FORMAT.format(0))
        self._score.pack(side = tk.LEFT)

        self._swap = tk.Label(self._status, text = SWAPS_FORMAT.format('∞',0))
        self._swap.pack(side = tk.RIGHT)

    def set_score(self,score):
        self._score.config(text = SCORE_FORMAT.format(score))

    def set_swap(self,swap):
        self._swap.config(text = SWAPS_FORMAT.format('∞',swap))

class Character(object):
    def __init__(self,max_health):
        self._max_health = max_health
        self._health = max_health

    def get_max_health(self):
        return self._max_health

    def get_health(self):
        return self._health

    def lose_health(self, amount):
        self._health -= amount

        if self._health < 0:
            self._health = 0

    def gain_health(self, amount):
        self._health += amount

        if self._health > self._max_health:
            self._health = self._max_health

    def reset_health(self):
        self._health = self._max_health

class Enemy(Character):
    def __init__(self, type, max_health, attack):
        super().__init__(max_health)
        self._type = type
        self._attack = attack

    def set_attack(self,attack):
        self._attack = attack
        if self._attack[1]>300:
            self._attack[0] = 300

    def get_attack(self):
        return self._attack

    def get_type(self):
        return self._type

    def attack(self):
        return random.randint(self._attack[0],self._attack[1])

class Player(Character):
    def __init__(self, max_health, swaps_per_turn, base_attack):
        super().__init__(max_health)
        self._swaps_per_turn = swaps_per_turn
        self._swaps_left = swaps_per_turn
        self._base_attack = base_attack

    def get_swaps_per_turn(self):
        return self._swaps_per_turn

    def record_swap(self):
        self._swaps_left -= 1
        if self._swaps_left < 0:
            self._swaps_left = 0
        return self._swaps_left

    def get_swaps(self):
        return self._swaps_left

    def reset_swaps(self):
        self._swaps_left = self._swaps_per_turn

    def attack(self, runs,defender_type):
        list1 = []
        for i in runs:
            tile = str(i[i.find_dominant_cell()])
            tile = tile[6:len(tile)-2]
            damage = len(i)*i.get_max_dimension()*self._base_attack

            list1.append((tile,damage))
        return list1

class VersusStatusBar(tk.Frame):
    """
    Manage the statusbar.
    """
    def __init__(self,master):
        super().__init__(master)
        #Frame 1
        self._frame1 = tk.Frame(self)
        self._frame1.pack(side = tk.TOP)
        self._level = tk.Label(self._frame1, text = LEVEL_FORMAT.format(1))
        self._level.pack()
        #Player and enemy health
        self._phmax = 0
        self._ehmax = 0
        self._phealth = 0
        self._ehealth = 0
        #Frame 2
        self._frame2 = tk.Frame(master,pady = 20)
        self._frame2.pack(side = tk.BOTTOM, fill = tk.BOTH)
        #LHS Frame
        self._phframe = tk.Frame(self._frame2)
        self._phframe.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1)
        #Player health info
        self.text_ph = tk.Label(self._phframe, text = \
            HEALTH_FORMAT.format(int(self._phealth)))
        self.text_ph.pack(side = tk.LEFT, pady = 5)
        #Player health bar
        self._ph = tk.Label(self._phframe, bg = 'green')
        self._ph.pack(side = tk.LEFT, ipadx = 100, pady = 5)
        self._phrest = tk.Label(self._phframe, bg = 'green')
        self._phrest.pack(side = tk.LEFT, ipadx = 0, pady = 5)
        #RHS Frame
        self._ehframe = tk.Frame(self._frame2)
        self._ehframe.pack(side = tk.RIGHT, fill = tk.BOTH, expand = 1)
        #Enemy health info
        self.text_eh = tk.Label(self._ehframe, text = \
            HEALTH_FORMAT.format(int(self._ehealth)))
        self.text_eh.pack(side = tk.RIGHT, pady = 5)
        #Enemy health bar
        self._eh = tk.Label(self._ehframe, bg = 'red')
        self._eh.pack(side = tk.RIGHT,ipadx = 100, pady = 5)
        self._ehrest = tk.Label(self._ehframe, bg = 'red')
        self._ehrest.pack(side = tk.RIGHT,ipadx = 0, pady = 5)
        #Swaps info
        self._swaps_per_turn = None
        self._swaps = tk.Label(self._frame2, text = SWAPS_LEFT_FORMAT.format(\
            self._swaps_per_turn, self._swaps_per_turn))
        self._swaps.pack()

    def set_pmax(self, max):
        self._phmax = max
        
    def set_emax(self,max):
        self._ehmax = max

    def set_swaps_per_turn(self,total):
        self._swaps_per_turn = total

    def set_swaps(self, swaps):
        self._swaps.config(text = SWAPS_LEFT_FORMAT.format(\
            self._swaps_per_turn, swaps))

    def set_level(self, current):
        self._level.config(text = LEVEL_FORMAT.format(current))

    def set_ph(self, curnt_health):
        rest = self._phmax - curnt_health
        rest = (rest/self._phmax)*100
        self._phealth = curnt_health
        health = 100 - rest
        #base info above
        self.text_ph.config(text = HEALTH_FORMAT.format(int(self._phealth)))
        self._ph.pack(side = tk.LEFT, ipadx = health, pady = 5)
        self._phrest.pack(side = tk.LEFT, ipadx = rest, pady = 5)
        if rest == 0:
            self._phrest.config(bg = 'green')
        else:
            self._phrest.config(bg = 'grey')
        if health == 0:
            self._ph.config(bg = 'grey')
        else:
            self._ph.config(bg = 'green')

    def set_eh(self, curnt_health):
        rest = self._ehmax - curnt_health
        rest = (rest/self._ehmax)*100
        self._ehealth = curnt_health
        health = 100 - rest
        #base info above
        self.text_eh.config(text = HEALTH_FORMAT.format(int(self._ehealth)))
        self._eh.pack(side = tk.RIGHT, ipadx = health, pady = 5)
        self._ehrest.pack(side = tk.RIGHT, ipadx = rest, pady = 5)
        if rest == 0:
            self._ehrest.config(bg = 'red')
        else:
            self._ehrest.config(bg = 'grey')
        if health == 0:
            self._eh.config(bg = 'grey')
        else:
            self._eh.config(bg = 'red')

class ImageTileGridView(TileGridView):
    def draw_tile_sprite(self, xy_pos, tile, selected):
        """Draws the sprite for the given tile at given (x, y) position.

        TileGridView.undraw_tile_sprite(TileGridView, (int, int), Tile, bool)
                                                                    -> None"""
        colour = tile.get_colour()
        width, height = self._calculate_tile_size(xy_pos, selected)
        x, y = xy_pos
        return self.create_rectangle(
            x - width, y - height, x + width, y + height, fill=colour)

class SinglePlayerTileApp(SimpleTileApp):
    def __init__(self,master):
        self._master = master
        self._master.title('Tile Game - Level 1')
        self._game = SimpleGame()

        self._game.on('swap', self._handle_swap)
        self._game.on('score', self.attack_enemy)

        self._grid_view = TileGridView(
            master, self._game.get_grid(),
            width=GRID_WIDTH, height=GRID_HEIGHT, bg='black')
        self._grid_view.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        menubar = tk.Menu(self._master,tearoff = 0)
        master.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)

        filemenu.add_command(label="New Game", command = self.new_game)
        filemenu.add_command(label="Exit", command=self.quit)
        self._statusbar = VersusStatusBar(self._master)
        self._statusbar.pack(side = tk.BOTTOM)
        self._player = Player(PLAYER_BASE_HEALTH,SWAPS_PER_TURN,PLAYER_BASE_ATTACK)
        self._statusbar.set_pmax(self._player.get_max_health())
        self._statusbar.set_ph(self._player.get_health())
        self._enemy = Enemy("type",ENEMY_BASE_HEALTH,(ENEMY_ATTACK_DELTA,ENEMY_BASE_ATTACK))
        self._statusbar.set_emax(self._enemy.get_max_health())
        self._statusbar.set_eh(self._enemy.get_health())

        #base info
        self._level_count = 1
        self.base_attack = 5
        self._statusbar.set_swaps_per_turn(self._player.get_swaps_per_turn())
        self._statusbar.set_swaps(self._player.get_swaps())
        #


    def die(self):
        self._game.reset()
        self._grid_view.draw()

        self._enemy.set_attack((ENEMY_ATTACK_DELTA,ENEMY_BASE_ATTACK))
        self._level_count = 1
        self.base_attack = 5

        self._player.gain_health(self._player.get_max_health())
        self.set_player_h(self._player.get_health())

        self._enemy.gain_health(self._enemy.get_max_health())
        self.set_enemy_h(self._enemy.get_health())

        self._player.reset_swaps()
        self._statusbar.set_swaps(self._player.get_swaps())

    def new_game(self):
        if self._grid_view.is_resolving():
            messagebox.showinfo(title="Resolving", message="The grid view is resolving")
        else:
            self._game.reset()
            self._grid_view.draw()

            self._enemy.set_attack((ENEMY_ATTACK_DELTA,ENEMY_BASE_ATTACK))
            self._level_count = 1
            self.base_attack = 5

            self._player.gain_health(self._player.get_max_health())
            self.set_player_h(self._player.get_health())

            self._enemy.gain_health(self._enemy.get_max_health())
            self.set_enemy_h(self._enemy.get_health())

            self._player.reset_swaps()
            self._statusbar.set_swaps(self._player.get_swaps())

    def next_level(self):
        self._level_count += 1
        self.refresh_level()
        self._game.reset()
        self._grid_view.draw()
        self.base_attack += 2
        self._enemy.set_attack((self._enemy.get_attack()[0],self._enemy.get_attack()[1]+40))

        self._player.gain_health(self._player.get_max_health())
        self.set_player_h(self._player.get_health())

        self._enemy.gain_health(self._enemy.get_max_health())
        self.set_enemy_h(self._enemy.get_health())

        self._player.reset_swaps()
        self._statusbar.set_swaps(self._player.get_swaps())

    def set_enemy_h(self,health):
        self._statusbar.set_eh(health)

    def set_player_h(self,health):
        self._statusbar.set_ph(health)

    def refresh_level(self):
        self._master.title('Tile Game - Level {}'.format(self._level_count))
        self._statusbar.set_level(self._level_count)

    def attack_player(self, damage):
        self._player.lose_health(damage)
        self.set_player_h(self._player.get_health())
        if self._player.get_health() == 0:
            messagebox.showinfo(title="Die!Die!Die!", message="Congratulation,You Die!")
            self.die()

    def _handle_swap(self, from_pos, to_pos):
        """
        Run when a swap on the grid happens.
        """
        self._player.record_swap()
        self._statusbar.set_swaps(self._player.get_swaps())
        if self._player.get_swaps() == 0:
            self.attack_player(int(self._enemy.attack()))
            self._player.reset_swaps()
            self._statusbar.set_swaps(self._player.get_swaps())

    def attack_enemy(self, score):
        """
        Attack Enemy.
        """
        self._enemy.lose_health((score)/self.base_attack)
        self.set_enemy_h(self._enemy.get_health())
        if self._enemy.get_health() == 0:
            self.next_level()

def task1():
    # Add task 1 GUI code here
    root = tk.Tk()
    app = SimpleTileApp(root)
    root.mainloop()
def task2():
    # Add task 2 GUI code here
    root = tk.Tk()
    app = SinglePlayerTileApp(root)
    root.mainloop()

def task3():
    # Add task 3 GUI code here
    pass

def main():
    # Choose relevant task to run
    task2()


################################################################################
# Write your code above - NOTE you should define a top-level
# class (the application) called Breakout
################################################################################
if __name__ == '__main__':
    main()
