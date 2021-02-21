import discord
from .Player import Player
from .AI import AI
from itertools import cycle
from games.abc.baseGame import BaseGame
import io
import os
from PIL import Image, ImageDraw
from .Grid import Grid
from core import utils
from core.dataclass import PapGame
# from core.database import get_game_id


def check_for_win(grid, sign):
    """
    Questo dovrebbe essere la ricerca per i punti dato il segno che ha il giocatore.

    dovrebbe essere chiamata tipo Game.check_for_win(player1.sign) o qualcosa del genere
    :param grid:
    :param sign:
    :return:
    """
    return ((grid[0][0] == sign and grid[0][1] == sign and grid[0][2] == sign) or
            (grid[1][0] == sign and grid[1][1] == sign and grid[1][2] == sign) or
            (grid[2][0] == sign and grid[2][1] == sign and grid[2][2] == sign) or
            (grid[0][2] == sign and grid[1][2] == sign and grid[2][2] == sign) or
            (grid[0][1] == sign and grid[1][1] == sign and grid[2][1] == sign) or
            (grid[0][0] == sign and grid[1][0] == sign and grid[2][0] == sign) or
            (grid[0][0] == sign and grid[1][1] == sign and grid[2][2] == sign) or
            (grid[0][2] == sign and grid[1][1] == sign and grid[2][0] == sign))


def get_coords(inputValue: str):

    possible_coords = {
        "tl": (0, 0),
        "11": (0, 0),
        "topleft": (0, 0),
        "t": (0, 1),
        "top": (0, 1),
        "12": (0, 1),
        "tr": (0, 2),
        "topright": (0, 2),
        "13": (0, 2),
        "ml": (1, 0),
        "middleleft": (1, 0),
        "midleft": (1, 0),
        "21": (1, 0),
        "mid": (1, 1),
        "middle": (1, 1),
        "22": (1, 1),
        "mr": (1, 2),
        "middleright": (1, 2),
        "midright": (1, 2),
        "23": (1, 2),
        "bl": (2, 0),
        "bottomleft": (2, 0),
        "31": (2, 0),
        "bottom": (2, 1),
        "b": (2, 1),
        "32": (2, 1),
        "br": (2, 2),
        "bottomright": (2, 2),
        "33": (2, 2)
    }

    for key in possible_coords.keys():
        if inputValue == key:
            return possible_coords[key]


class Game(BaseGame):

    def __init__(self, player1: discord.Member = None, player2: discord.Member = None, data: dict = None):
        """
        Cheks if the game is new or loaded from DB

        Creates a new game if no data is passed, otherwise it parses the data provided.
        """

        if data is None:
            self.player1 = Player(player1.id, Image.open(f"{os.getcwd()}/modules/tic_tac_toe/src/x.png"), "x")
            self.player2 = Player(player2.id, Image.open(f"{os.getcwd()}/modules/tic_tac_toe/src/o.png"),
                                  "o") if player2 is not None else AI(Image.open(f"{os.getcwd()}/modules/tic_tac_toe/src/o.png"), "o")
            self.grid = [['', '', ''], ['', '', ''], ['', '', '']]
            self.turn = self.player2 if self.player2.user != "AI" else self.player1
        else:
            self.parseData(data)

        self.players = cycle([self.player1, self.player2])
        print(f"Initial grid {self.grid}")

    def compile_image(self):
        buffer = io.BytesIO()

        base_grid = Image.new("RGB", (156, 156), (255, 255, 255))
        draw = ImageDraw.Draw(base_grid)

        draw.line([50, 0, 50, 155], fill=(0, 0, 0), width=3)
        draw.line([103, 0, 103, 155], fill=(0, 0, 0), width=3)
        draw.line([0, 50, 155, 50], fill=(0, 0, 0), width=3)
        draw.line([0, 103, 155, 103], fill=(0, 0, 0), width=3)

        x = self.player1.symbol
        o = self.player2.symbol
        spacer = 53

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):

                if cell == 'x':
                    base_grid.paste(x, (i * spacer, j * spacer), x)
                    print(f"Cell [{i}][{j}] is X")

                if cell == 'o':
                    base_grid.paste(o, (i * spacer, j * spacer), o)
                    print(f"Cell [{i}][{j}] is O")

        print(f"Latest Grid: {self.grid}")
        base_grid.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    def makeMove(self, pos):
        old_board = self.compile_image()
        posX, posY = get_coords(pos)
        if self.grid[posY][posX] == "":
            self.grid[posY][posX] = self.turn.sign
        else:
            return old_board, 3
        hasWon = check_for_win(self.grid, self.turn.sign)
        new_board = self.compile_image()
        if not hasWon:
            self.processTurn()
            code = 0
        else:
            code = 1

        return new_board, code

    def processTurn(self):
        return next(self.players)

    def get_vs(self):
        return f"{self.player1} vs {self.player2}"

    def getData(self):
        data = {
            "player1ID": self.player1.user,
            "player2ID": self.player2.user,
            "currentTurn": self.turn.user,
            "grid": self.grid
        }
        return data

    def parseData(self, data: PapGame):
        gameData = data.gameData
        print(gameData)
        self.player1 = Player(gameData["player1ID"], Image.open(f"{os.getcwd()}/modules/tic_tac_toe/src/x.png"), "x")
        if gameData["player2ID"] == "AI":
            self.player2 = AI(Image.open(f"{os.getcwd()}/modules/tic_tac_toe/src/o.png"), "o")
        else:
            self.player2 = Player(gameData["player2ID"], Image.open(f"{os.getcwd()}/modules/tic_tac_toe/src/o.png"),
                                  "o")

        if gameData["currentTurn"] == gameData["player1ID"]:
            self.turn = Player(gameData["player1ID"], Image.open(f"{os.getcwd()}/modules/tic_tac_toe/src/x.png"),
                               "x")
        else:
            self.turn = Player(gameData["player2ID"], Image.open(f"{os.getcwd()}/modules/tic_tac_toe/src/o.png"),
                               "o")
        # else:
        #     self.turn = AI(Image.open(f"{os.getcwd()}\\modules\\tic_tac_toe\\src\\o.png"), "o")

        self.grid = gameData["grid"]

    """
    Questi sono test per una specie di "traduzione" tra IA e PIL.
    
    Non so ancora come verrà fatta ma vorrei cominciare a sviluppare il gioco con un "linguaggio" che anche la IA 
    potrà usare, così non dobbiamo usare metodi diversi se sta giocando la IA o un altro player
    
    """