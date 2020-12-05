import os
from games.abc.basePlayer import BasePlayer


class Player(BasePlayer):

    def __init__(self, user, symbol):
        self.user = user.id
        # sybol can be either X or O

        self.symbol = symbol

