from discord import Message

from core.abc.server import AbstractServer
from core.commandSystem import Command
from core import utils


@Command
async def echo( server: AbstractServer, msg: Message ):
	""" sends the same message it received """
	echoed: str = msg.content.replace( 'echo', '', 1 )
	if echoed == '':
		echoed = 'missing text!'
	await msg.channel.send( echoed )


@Command
async def hello( server: AbstractServer, msg: Message ):
	""" say hello to the author """
	await msg.channel.send( 'hello there!' )


@Command
async def pprefix( server: AbstractServer, msg: Message ):
	""" changes the personal prefix """
	prefix: str = msg.content[ 8: ].strip()
	if len( prefix ) > 4:
		await msg.channel.send( f'prefix too long! maximum lenght is 4.' )
	elif len( prefix ) == 0:
		await msg.channel.send( f'prefix too short! minimum lenght is 1.' )
	else:
		server.secondaryPrefix[ msg.author.id ] = prefix
		user: 'PapUser' = server.GetDatabase().getUser( msg.author.id )
		user.personalPrefix = prefix
		server.GetDatabase().setUser( user )
		await msg.channel.send( f'personal prefix changed to "{prefix}"' )


@Command
async def savedata( server: AbstractServer, msg: Message ):
	if msg.author.id in utils.getAuthors()():
		server.GetDatabase().db.save()