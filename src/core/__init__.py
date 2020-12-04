from traceback import format_exception
from typing import List, Dict

from discord import Client, Message, Embed
import discord

from . import Server
from .logging import get_logger

logger = get_logger( 'BOT' )


class Bot:
	instance: 'Bot'
	client: Client
	servers: Dict[ int, Server.Server ]

	def __init__( self ):
		Bot.instance = self
		self.client = Client()
		self.client.event( self.on_ready )
		self.client.event( self.on_message )

	def run( self, token: str ):
		self.client.run(token)

	async def on_ready( self ):
		logger.info( f'{self.client.user}: Ready.' )
		logger.info( f'The bot is currently in {len( self.client.guilds )} guilds.')

	async def on_message( self, msg: Message ):
		if msg.guild.id not in self.servers.keys():
			if msg.guild in self.client.guilds:
				logger.info( f'Got message from new guild {msg.guild.name}, adding it!' )
				self.servers[ msg.guild.id ] = Server.Server()
			else:
				logger.warning( f'Got message form unknown guild {msg.guild.name}, ignoring.' )
				return

		self.servers[ msg.guild.id ].handleMsg( msg )
