import os


class Player:

    def __init__(self, member_id, username, symbol):
        self.member_id = member_id
        self.username = username
        # sybol can be either X or O

        self.symbol = symbol