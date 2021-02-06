from typing import Coroutine, Dict, Awaitable, List

from discord import Message

from core.abc.server import AbstractServer


insult = ['scemo', 'stupido', 'idiota', 'stronzo', 'stupid', 'idiot']


class CommandList:

	__Commands: Dict[str, Coroutine] = {}

	async def echo( self, server: AbstractServer, msg: Message ):
		echoed: str = msg.content.replace('echo', '', 1)
		txt = echoed.split(' ')
		if echoed == '':
			echoed = 'missing text!'
		elif ( "i'm" in txt ) and _isInsult(txt):
			echoed = 'i know'
		elif ( "sono" in echoed ) and _isInsult(txt):
			echoed = "lo so"
		await msg.channel.send( echoed )

	async def hello( self, server: AbstractServer, msg: Message ):
		await msg.channel.send( 'hello there!' )

	async def pprefix( self, server: AbstractServer, msg: Message ):
		prefix: str = msg.content[8:].strip()
		if len( prefix ) > 4:
			await msg.channel.send(f'prefix too long! maximum lenght is 4.')
		elif len( prefix ) == 0:
			await msg.channel.send( f'prefix too short! minimum lenght is 1.' )
		else:
			server.secondaryPrefix[msg.author.id] = prefix
			await msg.channel.send(f'personal prefix changed to "{prefix}"')

	# INSTANCE METHODS: NOT COMMANDS

	def Command( self, func: Coroutine[ Awaitable[int], AbstractServer, Message ], cname: str = None ):
		"""
		The @decorator for commands
		:param func: coroutine to mark as command
		:param cname: usually None, used to set the command name
		"""
		name = func.__code__.co_name.lower()
		self.__Commands[ name if cname is None else cname ] = func
		return func

	def getOrDefault( self, item: str, default: Coroutine[ Awaitable[int], AbstractServer, Message ] ) -> Coroutine[ Awaitable[ int ], AbstractServer, Message ]:
		"""
		Get the specified command or if not found, returns the one given on default
		:param item: the item to get
		:param default: fallback coroutine
		:return: the command or the default coroutine
		"""
		if item in self.__Commands.keys():
			return self.__Commands.get( item )
		else:
			return getattr( self, item, default )


instance: CommandList = CommandList()


def Command( func: Coroutine[ Awaitable[ int ], AbstractServer, Message ], cname: str = None ):
	"""
	The @decorator for commands
	:param func: coroutine to mark as command
	:param cname: usually None, used to set the command name
	"""
	return instance.Command(func, cname)


def getOrDefault( item: str, default: Coroutine[ Awaitable[ int ], AbstractServer, Message ] ) -> Coroutine[ Awaitable[ int ], AbstractServer, Message ]:
	"""
	Get the specified command or if not found, returns the one given on default
	:param item: the item to get
	:param default: fallback coroutine
	:return: the command or the default coroutine
	"""
	return instance.getOrDefault(item, default)


def _isInsult(txt: List[str]) -> bool:
	for i in txt:
		if i in insult:
			return True
	return False
