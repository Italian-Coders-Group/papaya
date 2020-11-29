from traceback import format_exception
from typing import List

from discord import Client, Message, Embed

from . import Server


class Bot:

	client: Client
	servers: List[Server]




	def handleMessage( self, msg: Message ):
		pass





