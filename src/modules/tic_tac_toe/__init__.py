from .Game import Game, check_for_win
from core.commandList import Command
from core.abc.server import AbstractServer
from discord import Message, File
from core.utils import embed, getColor
from PIL import Image
import io
import os


game_list = []
d = {}


@Command
async def ttt(server: AbstractServer, msg: Message):
    newGame = Game(msg.author, msg.mentions[0])
    await msg.channel.send(embed=embed("New Game", f"This game is between { await newGame.player1.getUser()} and "
                                             f"{await newGame.player2.getUser()}", getColor("255,0,0")))
    '''
    This is temporary, only for testing purposes.
    '''
    if server.guild.id not in d.keys():
        d[server.guild.id] = []
    d[server.guild.id].append(newGame)

    print(d)


@Command
async def draw(server: AbstractServer, msg: Message):
    if server.guild.id not in d.keys():
        await msg.channel.send("You are not in any game :/")
    else:
        game = d[server.guild.id][0]

        if game.turn.id is not msg.author.id:
            await msg.channel.send("Ehi bud it's not your turn yet")
        else:
            params = msg.content.split()
            pos = list(params[1])
            newState = game.makeMove(int(pos[0]), int(pos[1]))
            await msg.channel.send(file=File(newState, "game.png"))


@Command
async def viewgames(server: AbstractServer, msg: Message):
    server_games = d.get(server.guild.id)
    await msg.channel.send(f"Current Games in this server: {server_games}")


@Command
async def testbase(server: AbstractServer, msg: Message):
    buffer = io.BytesIO()
    image = Image.open(f"{os.getcwd()}\\modules\\tic_tac_toe\\src\\x.png")
    image.save(buffer, "PNG")
    buffer.seek(0)
    await msg.channel.send(file=File(buffer, "testBase.png"))


@Command
async def grid(server: AbstractServer, msg: Message):
    games = [["x", "o", "x"], ["x", "x", "o"], ["x", "o", "x"]]
    has_won = True if check_for_win(games, "x") else False
    print(has_won )


@Command
async def get_state(server: AbstractServer, msg: Message):
    await msg.channel.send(d.get(server.guild.id)[0].get_vs())
