import discord
from .Player import Player
from itertools import cycle
from games.abc.baseGame import BaseGame
import io
import os
from PIL import Image
from .Grid import Grid
from core import utils
# from core.database import get_game_id


def check_for_win(grid, sign):
    """
    Questo dovrebbe essere la ricerca per i punti dato il segno che ha il giocatore.

    dovrebbe essere chiamata tipo Game.check_for_win(player1.sign) o qualcosa del genere
    :param grid:
    :param sign:
    :return:
    """
    # x = 0
    # y = 0
    # save_pos_x = []
    # save_pos_y = []
    # valid_sign = False
    # sign_counter = 0
    # for x in range(self.grid.width):
    #     for y in range(self.grid.height):
    #         if sign_counter > 1:
    #             if utils.check_distance(save_pos_x[sign_counter - 2], save_pos_y[sign_counter - 2], x - 1, y - 2):
    #                 valid_sign = True
    #             else:
    #                 sign_counter -= 1
    #                 save_pos_x[sign_counter].pop()
    #                 save_pos_y[sign_counter].pop()
    #
    #         if self.grid[x][y] == sign:
    #             sign_counter += 1
    #             save_pos_x.append(x)
    #             save_pos_y.append(y)
    return ((grid[0][0] == sign and grid[0][1] == sign and grid[0][2] == sign) or
            (grid[1][0] == sign and grid[1][1] == sign and grid[1][2] == sign) or
            (grid[2][0] == sign and grid[2][1] == sign and grid[2][2] == sign) or
            (grid[0][2] == sign and grid[1][2] == sign and grid[2][2] == sign) or
            (grid[0][1] == sign and grid[1][1] == sign and grid[2][1] == sign) or
            (grid[0][0] == sign and grid[1][0] == sign and grid[2][0] == sign) or
            (grid[0][0] == sign and grid[1][1] == sign and grid[2][2] == sign) or
            (grid[0][2] == sign and grid[1][1] == sign and grid[2][0] == sign))


class Game(BaseGame):

    def __init__(self, player1: discord.Member, player2: discord.Member):
        """
        A ogni game verrà associato un ID automatico, ma forse questo è meglio farlo in BaseGame (non ne ho idea)

        Che contiene:

        Guild_ID | Game_ID | Player1 | Player 2 | Result (campo riempito solo alla fine del game)
        """
        self.buffer = io.BytesIO()
        self.player1 = Player(player1, "x")
        self.player2 = Player(player2, "o")
        self.players = cycle([self.player1, self.player2])
        self.turn = self.processTurn("data")
        # self.grid = Grid(3, 3)

    def processTurn(self, data):
        return next(self.players)

    def get_vs(self):
        return f"{self.player1} vs {self.player2}"

    """
    Questi sono test per una specie di "traduzione" tra IA e PIL.
    
    Non so ancora come verrà fatta ma vorrei cominciare a sviluppare il gioco con un "linguaggio" che anche la IA 
    potrà usare, così non dobbiamo usare metodi diversi se sta giocando la IA o un altro player
    
    """

    def base(self):
        """
        Questo metodo prende una base.png e la salva nel buffer. La base devo decidere quanto sarà grande.

        Per semplicità dei tools userò Aseprite come editor, perché ci si lavora bene con i pixel e il software è
        intuitivo AF.

        :return:
        """
        image = Image.open(f"{os.getcwd()}\\modusigns\\tic_tac_toe\\src\\test_base.png")
        image.save(self.buffer, "PNG")
        return self.buffer.seek(0)
