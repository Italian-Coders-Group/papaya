from typing import Dict
import importlib

from discord import Client, Message

from .database.database import Database
from . import server
from . import utils
from .logging import get_logger
from .dataclass import PapGame
import modules

logger = get_logger( 'BOT' )


class Bot:
	instance: 'Bot'
	client: Client
	servers: Dict[ int, server.Server ] = {}
	database: Database

	def __init__( self ):
		Bot.instance = self
		self.client = Client()
		# register event listeners
		self.client.event( self.on_ready )
		self.client.event( self.on_message )
		self.database = Database()
		modules.initializeGames()


	def run( self, token: str ):
		""" Run the bot, its a blocking call """
		self.client.run(token)

	async def on_ready( self ):
		"""	Called when the bot is ready to process incoming messages """
		logger.info( f'{self.client.user}: Ready.' )
		logger.info( f'The bot is currently in {len( self.client.guilds )} guilds.')

	async def on_message( self, msg: Message ):
		"""
		Called when a message arrives
		:param msg: the discord.Message obj
		"""
		if (msg.author.id == 485434957129580545) or (msg.author.id == 781540733173366794):
			return
		from discord import TextChannel
		from discord import Guild
		msg.channel: TextChannel
		msg.guild: Guild
		# add the guild to the tracked server if it doesn't exist
		if msg.guild.id not in self.servers.keys():
			if msg.guild in self.client.guilds:
				logger.info( f'Got message from new guild "{msg.guild.name}", adding it!' )
				self.servers[ msg.guild.id ] = server.Server( msg.guild )
			else:
				logger.warning( f'Got message form unknown guild {msg.guild.name}, ignoring.' )
				return
		# don't permit to use echo to get permission elevation
		if msg.author == self.client.user:
			if 'echo' not in msg.content.split(' ')[0]:
				return
		# reloads the server instances and modules
		if msg.content == '$$reload' and msg.author.id in utils.getAuthors()():
			logger.warning(f'[RELOAD] reload issued in {msg.guild.name} by {msg.author.name}!')
			logger.info('[RELOAD] reloading!')
			await msg.channel.send('Reloading!')
			# clear all servers
			self.servers.clear()
			# reload modules
			import core.commandList
			import modules
			try:
				importlib.reload( server )
				importlib.reload( utils )
				importlib.reload( core.commandList )
				modules.reloadGames()
			except Exception as e:
				logger.error(f"[RELOAD] uncaught exception caught, can't complete reload!", exc_info=e)
				await msg.channel.send( embed=utils.getTracebackEmbed(e) )
			else:
				logger.info('[RELOAD] reload complete!')
				await msg.channel.send('Reloaded!')
		else:
			# call the right handler for the server
			await self.servers[ msg.guild.id ].handleMsg( msg )
		acceptList = self.database.getGuild(msg.guild.id).getAccept(msg.author.id)
		delAccept = False
		if not acceptList:
			pass
		elif (acceptList[2] == msg.channel.id) and ("accept" in msg.content):
			delAccept = self.database.getGuild(msg.guild.id).delAccept(msg.author.id)
			accepted = True
		elif (acceptList[2] == msg.channel.id) and ("deny" in msg.content):
			delAccept = self.database.getGuild(msg.guild.id).delAccept(msg.author.id)
			accepted = False
		else:
			pass

		if acceptList:
			if delAccept:
				if accepted:
					await msg.channel.send(f"Prepare, {msg.author} accepted the game")
					game = self.database.getGuild(msg.guild.id).getGamesForUser(msg.author.id)[0]
					self.database.getGuild(msg.guild.id).setGame(
						PapGame(
							gameID=game.gameID,
							gameType=game.gameType,
							userIDs=game.userIDs,
							gameData=game.gameData,
							live=True
						)
					)
				else:
					await msg.channel.send(f"Sorry, {msg.author} denied the , the game is not live")