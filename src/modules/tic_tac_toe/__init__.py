from .Game import Game
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
async def playttt(server: AbstractServer, msg: Message):
    newGame = Game(msg.author, msg.mentions[0])
    await msg.channel.send(embed=embed("New Game", f"This game is between { await newGame.player1.getUser()} and "
                                             f"{await newGame.player2.getUser()}", getColor("255,0,0")))
    if server.guild.id not in d.keys():
        d[server.guild.id] = []
    d[server.guild.id].append(newGame)

    print(d)


@Command
async def viewgames(server: AbstractServer, msg: Message):
    server_games = d.get(server.guild.id)
    await msg.channel.send(f"Current Games in this server: {server_games}")


@Command
async def testbase(server: AbstractServer, msg: Message):
    buffer = io.BytesIO()
    image = Image.open(f"{os.getcwd()}\\modules\\tic_tac_toe\\src\\test_base.png")
    image.save(buffer, "PNG")
    buffer.seek(0)
    await msg.channel.send(file=File(buffer, "testBase.png"))


@Command
async def grid(server: AbstractServer, msg: Message):
    games = d.get(server.guild.id)
    await msg.channel.send(games[0].grid)