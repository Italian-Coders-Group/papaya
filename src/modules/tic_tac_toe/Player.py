import os
from games.abc.basePlayer import BasePlayer


class Player(BasePlayer):

    def __init__(self, user, symbol):
        """
        Sarebbe utile storare nel db un Player_ID con un Guild_ID così da poter sperimentare con ledearboards o altro.

        Anche per vedere la storia dei game di un giocatore, anche questo forse è meglio metterlo in BasePlayer



        :param user:
        :param symbol:
        """

        self.user = user.id
        # sybol can be either X or O

        self.symbol = symbol

