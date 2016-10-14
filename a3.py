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
import socket, time
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

        self._reset = tk.Button(self._topframe, 
                                text = 'Reset Status', 
                                command = self.reset)
        self._reset.pack()


    def new_game(self):
        """
        Start a new game, reset score and also swaps player made to zero.
        """
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
        """
        Quit the Game.
        """
        ans = messagebox.askokcancel('Exit', "Do you want to quit?")
        if ans:
            self._master.destroy()

    def reset(self):
        """
        Reset the score and swaps.
        """
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
    """
    Manage the player info.
    """
    def __init__(self):
        """
        Constructor(SimplePlayer)
        """
        self._score = 0
        self._swap = 0

    def add_score(self, score):
        """
        Add score of player and return it.

        SimplePlayer.add_score(SimplePlayer, int) -> int
        """
        self._score += score
        return self._score
    def get_score(self):
        """
        Return the current score of player.

        SimplePlayer.get_score(SimplePlayer) -> int
        """
        return self._score

    def reset_score(self):
        """
        Reset player's score to zero.

        SimplePlayer.reset_score(SimplePlayer)
        """
        self._score = 0

    def record_swap(self):
        """
        Add 1 to swap when method be called and return the current swaps.

        SimplePlayer.record_swap(SimplePlayer) -> int
        """
        self._swap += 1
        return self._swap
    def get_swaps(self):
        """
        Return the number of swaps player made.

        SimplePlayer.get_swaps(SimplePlayer) -> int
        """
        return self._swap
    def reset_swaps(self):
        self._swap = 0

class SimpleStatusBar(tk.Frame):
    """
    Displayer the base information of player.
    """
    def __init__(self, master):
        """
        Constructor(tk.Frame, SimpleTileApp)
        """
        super().__init__(master)
        self._status = tk.Frame(self)
        self._status.pack(ipadx= 100)

        self._score = tk.Label(self._status, text = SCORE_FORMAT.format(0))
        self._score.pack(side = tk.LEFT)

        self._swap = tk.Label(self._status, text = "Swap {} made".format(0))
        self._swap.pack(side = tk.RIGHT)

    def set_score(self,score):
        """
        Set the score of status bar.

        SimpleStatusBar.set_score(SimpleStatusBar, int)
        """
        self._score.config(text = SCORE_FORMAT.format(score))

    def set_swap(self,swap):
        """
        Set the swap of status bar.

        SimpleStatusBar.set_swap(SimpleStatusBar, int)
        """
        self._swap.config(text = "Swap {} made".format(swap))

class Character(object):
    """
    Manage all the character in the game.
    """
    def __init__(self,max_health):
        """
        Constructor(Character, int)
        """
        self._max_health = max_health
        self._health = max_health

    def get_max_health(self):
        """
        Return the max health of an character.

        Character.get_max_health(Character) -> int
        """
        return self._max_health

    def get_health(self):
        """
        Return current health of an character.

        Character.get_health(Character) -> int
        """
        return self._health

    def lose_health(self, amount):
        """
        Make an character lose health.

        Character.lose_health(Character, int)
        """
        self._health -= amount

        if self._health < 0:
            self._health = 0

    def gain_health(self, amount):
        """
        Increase an character health.

        Character.gain_health(Character, int)
        """
        self._health += amount

        if self._health > self._max_health:
            self._health = self._max_health

    def reset_health(self):
        """
        Reset the character health to the max.

        Character.reset_health(Character)
        """
        self._health = self._max_health

class Enemy(Character):
    """
    Manage the Enemy base info.
    """
    def __init__(self, type, max_health, attack):
        """
        Constructor(Character, str, int, int)
        """
        super().__init__(max_health)
        self._type = type
        self._attack = attack

    def set_attack(self,attack):
        """
        Set attack of Enemy.

        Enemy.set_attackh(Character, int)
        """
        self._attack = attack
        if self._attack[1]>300:
            self._attack[0] = 300

    def get_attack(self):
        """
        Return the attack value of Enemy.

        Enemy.get_attack(Character) -> int
        """
        return self._attack

    def set_type(self, type):
        """
        Set the type of Enemy.

        Enemy.set_type(Character, str)
        """
        self._type = type

    def get_type(self):
        """
        Return the type of Enemy.

        Enemy.get_type(Character) -> str
        """
        return self._type

    def attack(self):
        """
        Return a random value of damage Enemy may make.

        Enemy.attackh(Character) -> int
        """
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
            damage = len(i) * i.get_max_dimension() * self._base_attack
            list1.append((tile,damage))
        return list1

class VersusStatusBar(tk.Frame):
    """
    Visualize the statusbar.
    """
    def __init__(self,master):
        """
        Constructor(tk.Frame, SinglePlayerTileApp)
        """
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
        self._ph = tk.Canvas(self._phframe, width = 100, height = 20)
        self._ph.pack(side = tk.LEFT)
        self._phbar = self._ph.create_rectangle(0,0,100,20, fill = 'green')
        #RHS Frame
        self._ehframe = tk.Frame(self._frame2)
        self._ehframe.pack(side = tk.RIGHT, fill = tk.BOTH, expand = 1)
        #Enemy health info
        self.text_eh = tk.Label(self._ehframe, text = \
            HEALTH_FORMAT.format(int(self._ehealth)))
        self.text_eh.pack(side = tk.RIGHT, pady = 5)
        #Enemy health bar
        self._eh = tk.Canvas(self._ehframe, width = 100, height = 20)
        self._eh.pack(side = tk.RIGHT)
        self._ehbar = self._eh.create_rectangle(0,0,100,20, fill = 'red')
        #Swaps info
        self._swaps_per_turn = None
        self._swaps = tk.Label(self._frame2, text = SWAPS_LEFT_FORMAT.format(\
            self._swaps_per_turn, self._swaps_per_turn))
        self._swaps.pack(ipadx = 20)

    def set_pmax(self, max):
        """
        Set Player's health to value max.

        VersusStatusBar.set_pmax(tk.Frame, int)
        """
        self._phmax = max
        
    def set_emax(self,max):
        """
        Set Enemy's health to value max.

        VersusStatusBar.set_emax(tk.Frame, int)
        """
        self._ehmax = max

    def set_swaps_per_turn(self,total):
        """
        Set the value of swaps can use per turn

        VersusStatusBar.set_swaps_per_turn(tk.Frame, int)
        """
        self._swaps_per_turn = total

    def set_swaps(self, swaps):
        """
        Set the value of swaps can make.

        VersusStatusBar.set_swaps(tk.Frame, int)
        """
        self._swaps.config(text = SWAPS_LEFT_FORMAT.format(\
            self._swaps_per_turn, swaps))

    def set_level(self, current):
        """
        Set the current level.

        VersusStatusBar.set_level(tk.Frame, int)
        """
        self._level.config(text = LEVEL_FORMAT.format(current))

    def set_ph(self, curnt_health):
        """
        Set the Player current health value.

        VersusStatusBar.set_ph(tk.Frame, int)
        """
        rest = self._phmax - curnt_health
        rest = (curnt_health/self._phmax)*100
        self._phealth = int(curnt_health)
        #base info above
        self.text_ph.config(text = self._phealth)
        self._ph.coords(self._phbar,(0,0,rest,20))

    def set_eh(self, curnt_health):
        """
        Set the Enemy current health value.

        VersusStatusBar.set_eh(tk.Frame, int)
        """
        rest = self._ehmax - curnt_health
        rest = (curnt_health/self._phmax)*100
        self._ehealth = int(curnt_health)
        #base info above
        self.text_eh.config(text = self._ehealth)
        self._eh.coords(self._ehbar,(0,0,rest,20))

class ImageTileGridView(TileGridView):
    "Visualize the TileGrid."
    def __init__(self, master, grid, *args, width=GRID_WIDTH,
                 height=GRID_HEIGHT,
                 cell_width=GRID_CELL_WIDTH, cell_height=GRID_CELL_HEIGHT,
                 **kwargs):

        self._light_sky_blue = tk.PhotoImage(file = './images/light sky blue.gif')
        self._purple = tk.PhotoImage(file = './images/purple.gif')
        self._gold = tk.PhotoImage(file = './images/gold.gif')
        self._green = tk.PhotoImage(file = './images/green.gif')
        self._blue = tk.PhotoImage(file = './images/blue.gif')
        self._red = tk.PhotoImage(file = './images/red.gif')
        self._light_sky_blues = tk.PhotoImage(file = './images/light sky blues.gif')
        self._purples = tk.PhotoImage(file = './images/purples.gif')
        self._golds = tk.PhotoImage(file = './images/golds.gif')
        self._greens = tk.PhotoImage(file = './images/greens.gif')
        self._blues = tk.PhotoImage(file = './images/blues.gif')
        self._reds = tk.PhotoImage(file = './images/reds.gif')
        self._images = {'red':self._red,
                        'blue': self._blue,
                        'green':self._green,
                        'gold':self._gold,
                        'purple':self._purple,
                        'light sky blue':self._light_sky_blue}
        self._images_selected = {'red':self._reds,
                        'blue': self._blues,
                        'green':self._greens,
                        'gold':self._golds,
                        'purple':self._purples,
                        'light sky blue':self._light_sky_blues}
        super().__init__(master, grid, *args, width=GRID_WIDTH,
                 height=GRID_HEIGHT,
                 cell_width=GRID_CELL_WIDTH, cell_height=GRID_CELL_HEIGHT,
                 **kwargs)

    def return_image(self):
        return self._images

    def draw_tile_sprite(self, xy_pos, tile, selected):
        """Draws the sprite for the given tile at given (x, y) position.

        TileGridView.undraw_tile_sprite(TileGridView, (int, int), Tile, bool)
                                                                    -> None"""
        colour = tile.get_colour()
        x, y = xy_pos
        if selected:
            return self.create_image(x,y, 
                                     image = self._images_selected[colour])
        else:
            return self.create_image(x,y, 
                                     image = self._images[colour])

class SinglePlayerTileApp(SimpleTileApp):
    """
    Visualize the entire game.
    """
    def __init__(self,master):
        """
        Constructor(SinglePlayerTileApp, SimpleTileApp)
        """
        self._master = master
        self._master.title('Tile Game - Level 1')
        self._game = SimpleGame()

        self._game.on('swap', self._handle_swap)
        self._game.on('run', self._handle_runs)

        self._grid_view = ImageTileGridView(
            master, self._game.get_grid(),
            width=GRID_WIDTH, height=GRID_HEIGHT, bg='black')
        self._grid_view.pack(side=tk.TOP)


        self._canvas1 = tk.Canvas(master,width = 100, height = 100)
        self._canvas1.pack(side = tk.LEFT)
        self._canvas2 = tk.Canvas(master,width = 100, height = 100)
        self._canvas2.pack(side = tk.RIGHT)

        menubar = tk.Menu(self._master,tearoff = 0)
        master.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)

        filemenu.add_command(label="New Game", command = self.new_game)
        filemenu.add_command(label="Exit", command=self.quit)
        self._statusbar = VersusStatusBar(self._master)
        self._statusbar.pack(side = tk.BOTTOM)
        self._player = Player(PLAYER_BASE_HEALTH,
                              SWAPS_PER_TURN,
                              PLAYER_BASE_ATTACK)
        self._statusbar.set_pmax(self._player.get_max_health())
        self._statusbar.set_ph(self._player.get_health())
        self._defender_type = list(TILE_PROBABILITIES)
        self._enemy = Enemy(self._defender_type
                            [random.randint(0,len(self._defender_type)-1)],
                            ENEMY_BASE_HEALTH,
                            (ENEMY_ATTACK_DELTA,ENEMY_BASE_ATTACK))
        self._statusbar.set_emax(self._enemy.get_max_health())
        self._statusbar.set_eh(self._enemy.get_health())

        self._player_image = tk.PhotoImage(file = './images/player.gif')
        self._canvas1.create_image(50,50,
                                   image = self._player_image)
        self.image_enemy = self._canvas2.create_image(
            50,50,image = self._grid_view.return_image()
            [TILE_COLOURS[self._enemy.get_type()]])

        #base info
        self._level_count = 1
        self.base_attack = 3
        self._statusbar.set_swaps_per_turn(self._player.get_swaps_per_turn())
        self._statusbar.set_swaps(self._player.get_swaps())

    def die(self):
        """
        If Player die, reset all the entire game.
        """
        messagebox.showinfo(title="Die!Die!Die!", message="You died!")
        self._game.reset()
        self._grid_view.draw()

        self._player.gain_health(self._player.get_max_health())
        self.set_player_h(self._player.get_health())

        self._enemy.set_type(self._defender_type
                             [random.randint(0,len(self._defender_type)-1)])
        self._enemy.gain_health(self._enemy.get_max_health())
        self.set_enemy_h(self._enemy.get_health())

        self._player.reset_swaps()
        self._canvas2.itemconfig(self.image_enemy, image = 
                                 self._grid_view.return_image()
                                 [TILE_COLOURS[self._enemy.get_type()]])
        self._statusbar.set_swaps(self._player.get_swaps())

    def new_game(self):
        """
        Start a new game, reset all the entire game.
        """
        ans = messagebox.askokcancel('New game', "Do you want to START a new game?")
        if ans:
            self._game.reset()
            self._grid_view.draw()

            self._enemy.set_attack((ENEMY_ATTACK_DELTA,
                                    ENEMY_BASE_ATTACK))
            self._level_count = 1
            self.refresh_level()
            self.base_attack = 3

            self._player.gain_health(self._player.get_max_health())
            self.set_player_h(self._player.get_health())

            self._enemy.set_type(self._defender_type
                                 [random.randint(0,len(self._defender_type)-1)])
            self._enemy.gain_health(self._enemy.get_max_health())
            self.set_enemy_h(self._enemy.get_health())

            self._player.reset_swaps()
            self._canvas2.itemconfig(self.image_enemy, image = 
                                     self._grid_view.return_image()
                                     [TILE_COLOURS[self._enemy.get_type()]])
            self._statusbar.set_swaps(self._player.get_swaps())

    def next_level(self):
        """
        Start next level.
        """
        messagebox.showinfo(title="Congratulation", 
                            message="Level Completed, move to next level")
        self._level_count += 1
        self.refresh_level()
        self._game.reset()
        self._grid_view.draw()
        self.base_attack += 2
        self._enemy.set_attack(
            (self._enemy.get_attack()[0],
             self._enemy.get_attack()[1]+40))

        self._player.gain_health(self._player.get_max_health())
        self.set_player_h(self._player.get_health())

        self._enemy.set_type(
            self._defender_type[random.randint(0,len(self._defender_type)-1)])
        self._enemy.gain_health(self._enemy.get_max_health())
        self.set_enemy_h(self._enemy.get_health())

        self._player.reset_swaps()
        self._canvas2.itemconfig(self.image_enemy, 
                                 image = self._grid_view.return_image()
                                 [TILE_COLOURS[self._enemy.get_type()]])
        self._statusbar.set_swaps(self._player.get_swaps())

    def set_enemy_h(self,health):
        """
        Set Enemy health to the status bar.
        """
        self._statusbar.set_eh(health)

    def set_player_h(self,health):
        """
        Set Enemy health to the status bar.
        """
        self._statusbar.set_ph(health)

    def refresh_level(self):
        """
        Refresh status bar of level.
        """
        self._master.title('Tile Game - Level {}'.format(self._level_count))
        self._statusbar.set_level(self._level_count)

    def attack_player(self, damage):
        """
        Damage the player, if player health come to zero, Player die.

        SinglePlayerTileApp.attack_player(SinglePlayerTileApp, int)
        """
        self._player.lose_health(damage)
        self.set_player_h(self._player.get_health())
        if self._player.get_health() == 0:
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

    def _handle_runs(self, runs):
        """
        According to runs, damage the Enemy.
        """
        score = 0
        for i in self._player.attack(runs,self._enemy.get_type()):
            if i[0] == self._enemy.get_type():
                self.attack_player(i[1]/5)
            else:
                score += i[1]
        self._enemy.lose_health((score)/self.base_attack)
        self.set_enemy_h(self._enemy.get_health())
        if self._enemy.get_health() == 0:
            self.next_level()

class MultiTileGridView(ImageTileGridView):
    def __init__(self, master, grid, *args, width=GRID_WIDTH,
                 height=GRID_HEIGHT,
                 cell_width=GRID_CELL_WIDTH, cell_height=GRID_CELL_HEIGHT,
                 **kwargs):
        self._list_pos = []
        self._list_cell = []
        self._countp = 0
        super().__init__(master, grid, *args, width=GRID_WIDTH,
                 height=GRID_HEIGHT,
                 cell_width=GRID_CELL_WIDTH, cell_height=GRID_CELL_HEIGHT,
                 **kwargs)
    def draw(self):
        self.delete(tk.ALL)
        for pos, cell in self._grid:
            self._list_pos.append(pos)
            self._list_cell.append(cell)
        self.animation()
    def animation(self):
        if self._countp != len(self._list_pos):
            self.redraw_tile(self._list_pos[self._countp], selected=False, tile=self._list_cell[self._countp])
            self._countp+=1
            self._master.after(15, self.animation)

class MultiPlayerTileApp(SimpleTileApp):
    def __init__(self,master):

        self._ans = messagebox.askyesno('Server', "Play game as Server [Yes] or Client [No]?")
        self._server_ip = None
        if not self._ans:
            self._server_ip = input('Please entre server IP address: ')
            self._labeltop = tk.Label(master, text = "Connected: {}".format(self._server_ip))
            self._labeltop.pack()
        else:
            self._labeltop = tk.Label(master, text = "Unnonnected")
            self._labeltop.pack()
        self._master = master
        self._game = SimpleGame()

        #self._game.on('swap', self._handle_swap)
        self._game.on('score', self._handle_score)

        self._grid_view = MultiTileGridView(
            master, self._game.get_grid(),
            width=GRID_WIDTH, height=GRID_HEIGHT, bg='black')
        self._grid_view.pack()
        self._scorebar = ScoreBar(master)
        self._scorebar.pack(side = tk.TOP)
        self._score = Score(2000)
        self._scorebar.update_bar(self._score.get_score())
        menubar = tk.Menu(self._master,tearoff = 0)
        master.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)

        filemenu.add_command(label="Refresh", command = self.new_game)
        filemenu.add_command(label="Exit", command=self.quit)

        
        #Base info
        self._time = 1000
        self._decrease_per_time = 50
        self._port = 1996
        self._win = False
        self._level = 0
        #
        
        if self._ans:
        #Server part
            self._master.title("Server - Online")
            self._labeltop.config(text = "Connected")
            self._socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.bind(((''),self._port))
            self._socket.listen(1)
            self._tcpCliSock = None

            self._bottom_frame = tk.Frame(master)
            self._bottom_frame.pack(side = tk.BOTTOM)
            self.wait_client()
        else:
        #Client part
            self._master.title("Client - Connected to {}".format(self._server_ip))
            self._tcpCliSock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._tcpCliSock.connect((str(self._server_ip),self._port))
            self.wait_client()
            print('connected')

    def wait_client(self):
        if self._ans:
            print('waiting for connection...')
            self._tcpCliSock, addr = self._socket.accept()
            print('...connected from:', addr)
        self.decrease()

    def decrease(self):
        """
        Decrease the score per two seconds.
        """
        score = self._score.get_score() - self._decrease_per_time
        self._score.set_score(score)
        self._scorebar.update_bar(self._score.get_score())
        
        #Net Part
        if self._ans:
            print('receiving')
            try:
                data = self._tcpCliSock.recv(1024)
            except:
                self._labeltop.config(text = "Unconnected")
            print('received',data)
            type(data)
            print(data)
            try:
                if int(data) == 0:
                    self._win = True
                    messagebox.showinfo(title="Contragulation", message="You win")
                    self._tcpCliSock.close()
                else:
                    print('sending')
                    self._tcpCliSock.send(
                        str(self._score.get_score()).encode(encoding='utf_8'))
                    print('sent', self._score.get_score())
                    self._scorebar.update_bar2(int(data))
            except:
                pass
        else:
            print('sending')
            self._tcpCliSock.send(
                str(self._score.get_score()).encode(encoding='utf_8'))
            print('sent', self._score.get_score())
            print('receiving')
            try:
                data = self._tcpCliSock.recv(1024)
            except:
                self._labeltop.config(text = "Lost connection to server")
            print('received',data)
            try:
                if int(data) == 0:
                    self._win = True
                    messagebox.showinfo(title="Contragulation", 
                                        message="You win")
                    self._tcpCliSock.close()
                self._scorebar.update_bar2(int(data))
            except:
                pass
        self._level += 1
        if self._level == 10:
            self._time = 800
        elif self._level == 20:
            self._decrease_per_time = 80
        elif self._level == 40:
            self._decrease_per_time = 120
        elif self._level == 60:
            self._decrease_per_time = 200

        if int(self._score.get_score()) > int(self._scorebar.get_escore()):
            self._scorebar.config_canvas('winning')
        elif int(self._score.get_score()) < int(self._scorebar.get_escore()):
            self._scorebar.config_canvas('losing')
        else:
            self._scorebar.config_canvas('equal')
        #
        if self._score.get_score() > 0:
            if self._win:
                pass
            else:
                self._master.after(self._time,self.decrease)
        else:
            messagebox.showinfo(title="Sorry", message="You lose")
            self._tcpCliSock.send(str(0).encode(encoding='utf_8'))
            self._tcpCliSock.close()

    def _handle_score(self, score):
        self._score.set_score(self._score.get_score()+score)
        self._scorebar.update_bar(self._score.get_score())

    #Net Part
    def get_local_ip(self):
        return socket.gethostbyname(socket.gethostname())

class ScoreBar(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self._winning = tk.PhotoImage(file = './images/winning.gif')
        self._equal = tk.PhotoImage(file = './images/equal.gif')
        self._losing = tk.PhotoImage(file = './images/losing.gif')
        self._dic = {'winning':self._winning,
                     'equal':self._equal,
                     'losing':self._losing}
        self._frame1 = tk.Frame(self)
        self._frame1.pack(expand = True, fill = tk.BOTH)
        self._label1 = tk.Label(self._frame1, text = "You", fg="green")
        self._label1.pack(side = tk.LEFT)
        self._label2 = tk.Label(self._frame1, text = "Enemy", fg="red")
        self._label2.pack(side = tk.RIGHT)
        self._frame = tk.Frame(self)
        self._frame.pack(expand = True, fill = tk.BOTH)
        self._scorebar = tk.Canvas(self._frame, width = 300, height = 20)
        self._scorebar.pack(side = tk.LEFT)
        self._canvas = tk.Canvas(self, width = 100, height = 100)
        self._canvas.pack(side = tk.BOTTOM)
        self._status = self._canvas.create_image(50,50,image =self._equal)
        self._bar = self._scorebar.create_rectangle(0, 0, 300, 20, fill = 'green')
        self._scorebar2 = tk.Canvas(self._frame, width = 300, height = 20)
        self._scorebar2.pack(side = tk.RIGHT)
        self._bar2 = self._scorebar2.create_rectangle(0, 0, 300, 20, fill = 'red')
        self._score = None

    def config_canvas(self, status):
        self._canvas.itemconfig(self._status, image = self._dic[status])

    def update_bar(self,score):
        score = score/2000*300
        self._scorebar.coords(self._bar, (0, 0, score, 20))

    def update_bar2(self, score):
        score = score
        self._score = score
        self._scorebar2.coords(self._bar2, (0, 0, score/2000*300, 20))

    def get_escore(self):
        return self._score

class Score(object):
    def __init__(self,score):
        self._score = score
        self._score_max = score
    def get_score(self):
        return self._score
    def set_score(self, score):
        if score > self._score_max:
            self._score = self._score_max
        elif score < 0:
            self._score = 0
        else:
            self._score = score

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
    root = tk.Tk()
    app = MultiPlayerTileApp(root)
    root.mainloop()

def main():
    # Choose relevant task to run
    task1()


################################################################################
# Write your code above - NOTE you should define a top-level
# class (the application) called Breakout
################################################################################
if __name__ == '__main__':
    main()
