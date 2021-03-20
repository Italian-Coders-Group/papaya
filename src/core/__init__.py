import modules
from typing import Dict

from discord import Client, Message, Reaction, Member

from .database.database import Database
from . import server
from . import utils
# import commandSystem, as it should be already up and running before the bot starts
from . import commandSystem
from .dataclass.PapGame import PapGame
from .eventSystem import EventSystem, Events
from .exception import GameRequestNotFound
from .logging import get_logger
from .utils import embed, getColor

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
		self.client.event( self.on_reaction_add )
		self.client.event( self.on_reaction_remove )
		self.database = Database()
		modules.initializeGames()

	def run( self, token: str ):
		""" Run the bot, its a blocking call """
		if token is None:
			raise ValueError( 'Passed None instead of the token!' )
		self.client.run( token )

	def initLoggingAndRun( self, token: str, filename: str ):
		""" Initialize logging and run the bot, its a blocking call """
		if token is None:
			raise ValueError( 'Passed None instead of the token!' )
		if filename is None:
			raise ValueError( 'Passed None instead of the filename!' )
		logging.init_logging( filename )
		self.client.run( token )

	async def on_ready( self ):
		"""	Called when the bot is ready to process incoming messages """
		logger.info( f'{self.client.user}: Ready.' )
		logger.info( f'The bot is currently in {len( self.client.guilds )} guilds.')

	async def on_ready( self ):
		"""	Called when the bot is ready to process incoming messages """
		logger.info( f'{self.client.user}: Ready.' )
		logger.info( f'The bot is currently in {len( self.client.guilds )} guilds.')

	async def on_reaction_add( self, reaction: Reaction, user: Member ):
		""" Called when an user reacts to a message """
		if reaction.message.author == self.client.user:
			return
		guild = reaction.message.guild.id
		await self.servers[ guild ].handleReactionAdd(reaction, user)

	async def on_reaction_remove( self, reaction: Reaction, user: Member ):
		""" Called when an user remove a reaction from a message """
		if reaction.message.author == self.client.user:
			return
		guild = reaction.message.guild.id
		await self.servers[ guild ].handleReactionRemove( reaction, user )

	async def on_message( self, msg: Message ):
		"""
		Called when a message arrives
		:param msg: the discord.Message obj
		"""

		# don't permit to use echo to get permission elevation
		# don't respond to other bots
		if msg.author.bot or msg.author == self.client.user:
			if 'echo' not in msg.content.split( ' ' )[ 0 ]:
				return

		# add the guild to the tracked server if it doesn't exist
		if msg.guild.id not in self.servers.keys():
			if msg.guild in self.client.guilds:
				logger.info( f'Got message from new guild "{msg.guild.name}", adding it!' )
				self.servers[ msg.guild.id ] = server.Server( msg.guild )
			else:
				logger.warning( f'Got message form unknown guild {msg.guild.name}, ignoring.' )
				return

		# reloads the server instances and modules
		if msg.content == '$$reload' and msg.author.id in utils.getAuthors()():
			logger.warning(f'[RELOAD] reload issued in {msg.guild.name} by {msg.author.name}!')
			logger.info('[RELOAD] reloading!')
			await msg.channel.send('Reloading!')
			# clear all servers
			self.servers.clear()
			# reload modules
			import defaultCommands
			import moduleUtils
			try:
				# utils may be imported by the command system, reload it first
				moduleUtils.reload( utils )
				# reload command system _BEFORE_ everything else
				moduleUtils.reload( commandSystem )
				moduleUtils.reload( defaultCommands )
				commandSystem.init()
				# reload the rest
				moduleUtils.reload( server )
				await EventSystem.INSTANCE.invoke( Events.Reload )
			except Exception as e:
				logger.error(f"[RELOAD] uncaught exception caught, can't complete reload!", exc_info=e)
				await msg.channel.send( embed=utils.getTracebackEmbed(e) )
			else:
				logger.info('[RELOAD] reload complete!')
				await msg.channel.send('Reloaded!')
		else:
			# call the right handler for the server
			await self.servers[ msg.guild.id ].handleMsg( msg )

		# MR EDIT (RE-EDIT BY ENDER CUZ IT BROKE) ~~ MR RE-EDIT CUZ ENDER BROKE IT BY RE-EDITING CUZ I BROKE IT ~~ STILL NOT WORKING CAUSE DB STUFF
		try:
			acceptList: list = self.database.getGuild(msg.guild.id).getGameRequest(msg.author.id)
			accepted: bool

			if (acceptList[3] == msg.channel.id) and ("accept" in msg.content):
				self.database.getGuild(msg.guild.id).delGameRequest(msg.author.id)
				accepted = True
			elif (acceptList[3] == msg.channel.id) and ("deny" in msg.content):
				self.database.getGuild(msg.guild.id).delGameRequest(msg.author.id)
				accepted = False

			if acceptList:
				if accepted:
					acceptedEmbed = embed(
						title="Game accepted. Prepare",
						content=f"This game is between {msg.author.mention} and his opponent TODO: get actual names, ty",
						color=getColor(RGB="0,255,0")
					)
					await msg.channel.send(embed=acceptedEmbed)
					game = self.database.getGuild(msg.guild.id).getGamesForUser(msg.author.id)[0]
					self.database.getGuild(msg.guild.id).setGame(
						PapGame(
							gameID=game.gameID,
							gameType=game.gameType,
							userIDs=PapGame.serializeUsers(game.userIDs),
							gameData=PapGame.serializeGameData(game.gameData),
							live=True
						)
					)
				else:
					deniedEmbed = embed(
						title="Game denied.",
						content="This game is cancelled.",
						color=getColor(RGB="255,0,0")
					)
					await msg.channel.send(embed=deniedEmbed)
		except GameRequestNotFound:
			pass