from typing import Dict
import importlib

from discord import Client, Message

from . import server
from .logging import get_logger
import modules

logger = get_logger( 'BOT' )


class Bot:
	instance: 'Bot'
	client: Client
	servers: Dict[ int, server.Server ] = {}

	def __init__( self ):
		Bot.instance = self
		self.client = Client()
		# register event listeners
		self.client.event( self.on_ready )
		self.client.event( self.on_message )
		modules.initializeGames()

	def run( self, token: str ):
		""" Run the bot, its blocking """
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
		# add the guild to the tracked server if it doesn't exist
		if msg.guild.id not in self.servers.keys():
			if msg.guild in self.client.guilds:
				logger.info( f'Got message from new guild "{msg.guild.name}", adding it!' )
				self.servers[ msg.guild.id ] = server.Server( msg.guild )
			else:
				logger.warning( f'Got message form unknown guild {msg.guild.name}, ignoring.' )
				return
		# don't permit to use echo to get elevation
		if msg.author == self.client.user:
			if 'echo' not in msg.content.split(' ')[0]:
				return
		# reloads the server instances and modules
		if msg.content == '$$reload':
			await msg.channel.send('Reloading!')
			self.servers.clear()
			import core.commandList
			import core.utils
			import modules
			importlib.reload( server )
			importlib.reload( core.utils )
			importlib.reload( core.commandList )
			modules.reloadGames()
			await msg.channel.send('Reloaded!')
		else:
			# call the right handler for the server
			await self.servers[ msg.guild.id ].handleMsg( msg )
