from .Game import Game, check_for_win
from .AI import AI
from core.commandList import Command
from core.abc.server import AbstractServer
from core.database.database import Database
from core.dataclass import PapGame, PapUser
from core.dataclass import utils as gameUtils
from discord import Message, File
from core.utils import embed, getColor
from PIL import Image
import io
import os
from core.fileSystem import File as localFile
from core import utils


@Command
async def ttt(server: AbstractServer, msg: Message):
    pvp = True
    if not msg.mentions or msg.mentions[0].id in [781540733173366794, 485434957129580545]:
        await msg.channel.send("You are going to play against our AI.")
        pvp = False
    player1 = msg.author
    player2 = msg.mentions[0] if pvp else None
    newGame = Game(player1=player1, player2=player2)

    server.GetDatabase().setGame(
        PapGame(
            gameUtils.getRandomGameID([player1.id, player2.id if pvp else 0]),
            "tic tac toe",
            [msg.author.id, msg.mentions[0].id] if pvp else [msg.author.id, "AI"],
            newGame.getData(),
            True
        )
    )

    await msg.channel.send(embed=embed("New Game", f"This game is between {newGame.player1.getUser()} and "
                                                   f"{newGame.player2.getUser()}", getColor("255,0,0")))


@Command
async def draw(server: AbstractServer, msg: Message):

    gameData = server.GetDatabase().getLiveGameForUser(msg.author.id)

    still_live = True

    if not gameData:
        await msg.channel.send("No games for you bud")
        return

    resumeGame = Game(data=gameData[0])

    if resumeGame.turn.user != msg.author.id:
        await msg.channel.send("Ehi bud it's not your turn yet")
    else:
        params = msg.content.split()
        pos = params[1]
        newState, code = resumeGame.makeMove(pos)
        await msg.channel.send(file=File(newState, "game.png"))
        if code == 3:
            await msg.channel.send("That position is invalid, try again")
        if code == 0:
            await msg.channel.send("The game is still going on")
        if code == 1:
            await msg.channel.send(f"Congrats {msg.author.mention} you won")
            still_live = False

    server.GetDatabase().setGame(
        PapGame(
            gameData[0].gameID,
            gameData[0].gameType,
            gameData[0].userIDs,
            resumeGame.getData(),
            still_live
        )
    )


@Command
async def tttstats(server: AbstractServer, msg: Message):
    user = server.GetDatabase().getStatsForUserInGuild(msg.author.id)
    await msg.channel.send(f"Here are your stats. Wins: {user[3]}. Losses: {user[4]}. Ties: {user[5]}")
    print(user)


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
    testAI = AI("x", "x")
    test = testAI.get_board_status(games)

    print(test)


@Command
async def get_state(server: AbstractServer, msg: Message):
    await msg.channel.send(d.get(server.guild.id)[0].get_vs())
