from typing import Dict

from discord import Message, Embed

from . import Rules


class Server:

	guildId: int
	roleRules: Dict[str, Rules]

	def __init__(self):
		pass

	def handleMsg( self, msg: Message ):
		pass

	def send( self, txt: str = None, embed: Embed = None ):
		pass
