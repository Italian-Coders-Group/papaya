from .TicTacToe import TicTacToe
from core.commandSystem import Command
from core.abc.server import AbstractServer
from core.database.database import Database
from core.dataclass.PapGame import PapGame
from core.dataclass.PapUser import PapUser
from core.dataclass import utils as gameUtils
from core.exception import *
from discord import Message, File
from core.utils import embed, getColor
from PIL import Image
import io
import os
from core.fileSystem import File as localFile
from core import utils
import requests
from .gameUtils import check_for_win


# TODO: REDO ENTIRE GAMESYSTEM DUE TO DATASTUFF CHANGES


# @Command
# async def imageTest(server: AbstractServer, msg: Message):
#     test = embed(
#         title='image',
#         content='test',
#         color=getColor(random=True)
#     )
#     file = File(requests.get('http://localhost:6060/tictactoe/test').text.replace('"', ''), filename='image.png')
#     test.set_image(url='attachment://image.png')
#     await msg.channel.send(file=file, embed=test)


@Command
async def ttt(server: AbstractServer, msg: Message):
	try:

		if msg.mentions:
			server.GetDatabase().makeGameRequest(
				discordID=msg.author.id,
				discordID2=msg.mentions[0].id,
				channelID=msg.channel.id,
				gametype='tic tac toe'
			)

		gameID = gameUtils.getRandomGameID([msg.author.id, msg.mentions[0].id] if msg.mentions else [msg.author.id, 0])
		player1 = msg.author
		player2 = None if not msg.mentions else msg.mentions[0]
		newGame = TicTacToe(player1=player1, player2=player2, data=None, gameID=gameID)
		live = 0

		if not msg.mentions:
			server.GetDatabase().initStatsForUserInGuild(msg.author.id, 'tic tac toe')
			live = 1
		else:
			live = 2

		server.GetDatabase().setGame(
			PapGame(
				gameID=gameID,
				gameType='tic tac toe',
				userIDs=[msg.author.id, msg.mentions[0].id] if msg.mentions else [msg.author.id, 0],
				gameData=newGame.getData(),
				live=live
			)
		)

		if not msg.mentions:
			tttContent = f'This game is between {msg.author.mention} and our AI'
		else:
			tttContent = f'This game is between {msg.author.mention} and {msg.mentions[0].mention}. Please wait until your opponent accept the game.'

		tttEmbed = embed(
			title='New tic tac toe Game.',
			content=tttContent,
			color=getColor(random=True)
		)
		await msg.channel.send(embed=tttEmbed)

	except GameRequestAlreadyLive:
		await msg.channel.send('GameRequestAlreadyLive')


@Command
async def draw(server: AbstractServer, msg: Message):
	try:
		gameData: PapGame = server.GetDatabase().getLiveGameForUserForGametype(discordID=msg.author.id, gameType="tic tac toe")
		still_live = True

		resumeGame = TicTacToe(player1=None, player2=None, data=gameData, gameID=gameData.gameID)
		resumeGameID = gameData.gameID
		userIDs = gameData.userIDs

		if resumeGame.turn.user != msg.author.id:
			await msg.channel.send("Ehi bud it's not your turn yet")
		else:
			params = msg.content.split()
			pos = params[1]
			code = resumeGame.makeMove(pos)

			if code == 3:
				await msg.channel.send("That position is invalid, try again")
			elif code == 0:
				await msg.channel.send("The game is still going on")
			elif code == 1:
				await msg.channel.send(f"Congrats {msg.author.mention} you won")
				for userid in userIDs.split(','):
					if userid == msg.author.id:
						server.GetDatabase().saveStatsForUserInGuild(
							userID=str(userid),
							loss=True,
							gameType='tic tac toe')
					else:
						server.GetDatabase().saveStatsForUserInGuild(
							userID=str(userid),
							win=True,
							gameType='tic tac toe')
				still_live = False
			elif code == 10:
				await msg.channel.send("Sorry but you lost and our AI WON, ggs")
				server.GetDatabase().saveStatsForUserInGuild(
					userID=msg.author.id,
					loss=True,
					gameType='tic tac toe')
				still_live = False
			elif code == 100:
				await msg.channel.send("This is a tie")
				for userid in userIDs.split(','):
					server.GetDatabase().saveStatsForUserInGuild(
						userID=str(userid),
						tie=True,
						gameType='tic tac toe')
				still_live = False

			drawEmbed = embed(
				title="Tic Tac Toe",
				content="X: Player1 \tO: Player2",
				color=getColor(random=True)
			)
			file = File(f'{os.getcwd()}/modules/tic_tac_toe/src/tictactoe_images/{resumeGameID}.png', filename='test.png')
			drawEmbed.set_image(url=f'attachment://test.png')
			# drawEmbed.add_field(name="game_status", value={'Still live' if still_live else 'Ended'}, inline=False)
			await msg.channel.send(file=file, embed=drawEmbed)
			updateGame = PapGame(
				gameData.gameID,
				[int(username) for username in (gameData.userIDs.replace(',', ' ').split(' '))],
				resumeGame.getData(),
				gameData.gameType,
				still_live
			)
			server.GetDatabase().setGame(
				updateGame
			)
	except GameNotFound:
		await msg.channel.send(f"There is no game for you bud.")


# @Command
# async def tttstats(server: AbstractServer, msg: Message):
# 	user = server.GetDatabase().getStatsForUserInGuild(msg.author.id)
# 	await msg.channel.send(f"Here are your stats. Wins: {user[3]}. Losses: {user[4]}. Ties: {user[5]}")
# 	print(user)

# @Command
# async def testbase(server: AbstractServer, msg: Message):
#     buffer = io.BytesIO()
#     image = Image.open(f"{os.getcwd()}/modules/tic_tac_toe/src/x.png")
#     image.save(buffer, "PNG")
#     buffer.seek(0)
#     await msg.channel.send(file=File(buffer, "testBase.png"))


@Command
async def grid(server: AbstractServer, msg: Message):

	games = [['o', 'o', 'o'],
	         ['x', 'x', 'x'],
	         ['x', 'x', 'x']]

	print(check_for_win(games, 'o'))


# @Command
# async def get_state(server: AbstractServer, msg: Message):
#     await msg.channel.send(d.get(server.guild.id)[0].get_vs())
