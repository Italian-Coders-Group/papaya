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
    engaged = False
    gameChek = server.GetDatabase().getLiveGameForUser(msg.author.id) or server.GetDatabase().getLiveGameForUser(
        msg.mentions[0].id) if \
        msg.mentions else False
    # mentionCheck = server.GetDatabase().getLiveGameForUser(msg.mentions[0].id)
    acceptCheck = server.GetDatabase().checkAccept(msg.author.id) or server.GetDatabase().checkAccept(msg.mentions[
                                                                                                          0].id) if \
        msg.mentions else False

    if gameChek or acceptCheck:
        engaged = True

    if not engaged:
        pvp = True
        if (not msg.mentions) or (msg.mentions[0].id in [781540733173366794, 485434957129580545]):
            pvp = False

            tttEmbed = embed(
                title="New tic tac toe Game.",
                content=f"This game is between {msg.author} and our AI",
                color=getColor(random=True)
            )

            await msg.channel.send(embed=tttEmbed)
            player1 = msg.author
            player2 = None
            newGame = Game(player1=player1, player2=player2)
            server.GetDatabase().setGame(
                PapGame(
                    gameUtils.getRandomGameID([player1.id, 0]),
                    "tic tac toe",
                    [msg.author.id, 0],
                    newGame.getData(),
                    True
                )
            )
        if pvp:
            accept = server.GetDatabase().makeAccept(msg.mentions[0].id, msg.channel.id)
            player1 = msg.author
            player2 = msg.mentions[0]
            newGame = Game(player1=player1, player2=player2)

            server.GetDatabase().setGame(
                PapGame(
                    gameUtils.getRandomGameID([player1.id, player2.id]),
                    "tic tac toe",
                    [msg.author.id, msg.mentions[0].id],
                    newGame.getData(),
                    False
                )
            )
            if accept:
                await msg.channel.send(f"Please wait until {msg.mentions[0]} accepts the game.")
            else:
                await msg.channel.send(f"There was a problem with the accept")

    else:
        await msg.channel.send("Game cannot be made, someone is already engaged in another game or has an invitation")


@Command
async def draw(server: AbstractServer, msg: Message):

    gameData = server.GetDatabase().getLiveGameForUser(userID=msg.author.id, gameType="tic tac toe")

    still_live = True

    if not gameData:
        await msg.channel.send("No games for you bud")
        return

    resumeGame = Game(data=gameData[0])
    resumeGameID = gameData[0].gameID

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
        if code == 10:
            await msg.channel.send("Sorry but our AI WON, ggs")
            still_live = False
        if code == 100:
            await msg.channel.send("This is a tie")
            still_live = False

        # drawEmbed = embed(
        #     title="Tic Tac Toe",
        #     content="X: Player1 \tO: Player2",
        #     color=getColor(random=True)
        # )
        # drawEmbed.set_image(url=f"https://papayabot.xyz/papayabot/games/imagesToSend/{resumeGameID}.png")
        # await msg.channel.send(embed=drawEmbed)

    server.GetDatabase().setGame(
        PapGame(
            gameData[0].gameID,
            gameData[0].gameType,
            [x for x in gameData[0].userIDs],
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
    image = Image.open(f"{os.getcwd()}/modules/tic_tac_toe/src/x.png")
    image.save(buffer, "PNG")
    buffer.seek(0)
    await msg.channel.send(file=File(buffer, "testBase.png"))


@Command
async def grid(server: AbstractServer, msg: Message):
    games = [['x', 'x', 'o'], ['o', 'x', 'x'], ['x', 'o', 'o']]
    test = check_for_win(games, 'x')

    print(test)


@Command
async def get_state(server: AbstractServer, msg: Message):
    await msg.channel.send(d.get(server.guild.id)[0].get_vs())
