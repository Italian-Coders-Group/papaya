from .Game import Game, check_for_win
from core.commandList import Command
from core.abc.server import AbstractServer
from discord import Message, File
from core.utils import embed, getColor
from PIL import Image
import io
import os


game_list = []
# this json is temporary, it's only purpose is that to hold games, maybe even update them, yeah

"""
    Some example for the json i had in mind
    
    games = {
        server.guild.id: [
            {
                "id1 id2": gameobject
            },
            {
                "id1 id2": gameobject
            }
        ]
    }
"""
d = {}


def getKeyFromUser(guildId: int, userInput: int):

    if guildId not in d.keys():
        return 0, "Server not found"

    if not d[guildId]:
        return 1, "This server has no games running"

    gameDict: dict
    for i, gameDict in enumerate(d[guildId]):
        for key in gameDict.keys():
            ids = key.split(" ")
            if str(userInput) in ids:
                return 2, key, i

    return 3, "User not Found"


@Command
async def ttt(server: AbstractServer, msg: Message):
    newGame = Game(msg.author, msg.mentions[0])
    '''
    This is temporary, only for testing purposes.
    '''

    if server.guild.id not in d.keys():
        d[server.guild.id] = []

    localDict = {
        f"{msg.author.id} {msg.mentions[0].id}": newGame
    }
    for valueList in d.values():
        for x in valueList:
            for key in x.keys():
                ids = key.split(" ")
                for ID in ids:
                    for k in localDict.keys():
                        if ID in k.split(" "):
                            await msg.channel.send(
                                f"You cannot make this game, one or both contestant are already in another game")
                            print(d)
                            return
                # if key in localDict.keys():
                #     print(localDict.keys())
                #     await msg.channel.send(f"You cannot make this game, one or both contestant are already in another game")
                #     return

    d[server.guild.id].append(localDict)

    print(d)
    await msg.channel.send(embed=embed("New Game", f"This game is between {await newGame.player1.getUser()} and "
                                                   f"{await newGame.player2.getUser()}", getColor("255,0,0")))


@Command
async def draw(server: AbstractServer, msg: Message):
    if server.guild.id not in d.keys():
        await msg.channel.send("This server has no games running.")
    else:
        errorCode, key, i = getKeyFromUser(server.guild.id, msg.author.id)

        if errorCode == 2:
            game = d[server.guild.id][i][key]
        else:
            print(errorCode, key)

        if game.turn.user is not msg.author.id:
            await msg.channel.send("Ehi bud it's not your turn yet")
        else:
            params = msg.content.split()
            pos = params[1]
            newState, code = game.makeMove(pos)
            await msg.channel.send(file=File(newState, "game.png"))
            if code == 3:
                await msg.channel.send("That position is invalid, try again")
            if code == 0:
                await msg.channel.send("The game is still going on")
            if code == 1:
                await msg.channel.send(f"Congrats {msg.author.mention} you won")
                del d[server.guild.id][i][key]


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
