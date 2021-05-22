# MR EDIT (RE-EDIT BY ENDER CUZ IT BROKE)
# MR RE-EDIT CUZ ENDER BROKE IT BY RE-EDITING CUZ I BROKE IT
# STILL NOT WORKING CAUSE DB STUFF
# EDER EDIT CUZ MR AND THE DB BROKE IT
from typing import Any, Dict

from discord import Message

from core import utils
from core.abc.database.guild import AbstractGuild
from core.abc.server import AbstractServer
from core.dataclass.PapGame import PapGame
from core.eventSystem import Listener
from core.exception import GameRequestNotFound


class AcceptSystem:

	@staticmethod
	@Listener
	async def onMessage( server: AbstractServer, msg: Message ):

		database: AbstractGuild = server.GetDatabase()

		try:
			acceptObj: Dict[str, Any] = database.getGameRequest( msg.author.id )
			accepted: bool = None

			if (acceptObj['channelID'] == msg.channel.id) and ("accept" in msg.content):
				database.delGameRequest(msg.author.id)
				accepted = True
			elif (acceptObj['channelID'] == msg.channel.id) and ("deny" in msg.content):
				database.delGameRequest(msg.author.id)
				accepted = False

			if accepted:
				acceptedEmbed = utils.embed(
					title="Game accepted. Prepare",
					content=f"This game is between {msg.author.mention} and his opponent TODO: get actual names, ty",
					color=utils.getColor(RGB="0,255,0")
				)
				await msg.channel.send(embed=acceptedEmbed)
				game = database.getGamesForUser(msg.author.id, gameType=acceptObj['gameType'])[0]
				database.setGame(
					PapGame(
						gameID=game.gameID,
						gameType=game.gameType,
						userIDs=game.userIDs,
						gameData=game.gameData,
						live=True
					)
				)
			elif accepted is not None:
				deniedEmbed = utils.embed(
					title="Game denied.",
					content="This game is cancelled.",
					color=utils.getColor(RGB="255,0,0")
				)
				await msg.channel.send(embed=deniedEmbed)
		except GameRequestNotFound:
			pass
