import os
from PIL import Image


class AI:

    def __init__(self, symbol: Image, sign: str):
        """
        Sarebbe utile storare nel db un Player_ID con un Guild_ID così da poter sperimentare con ledearboards o altro.

        Anche per vedere la storia dei game di un giocatore, anche questo forse è meglio metterlo in BasePlayer



        :param user:
        :param symbol:
        """

        self.user = "AI"
        self.sign = sign

        self.symbol = symbol
        print(f"{user} has symbol {type(symbol)}")

