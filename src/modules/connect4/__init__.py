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


# TODO: the entire thing lmao


@Command
async def connect4(server: AbstractServer, msg: Message):

    await msg.channel.send('This is a connect 4 game test kinda thing')


@Command
async def put(server: AbstractServer, msg: Message):

    await msg.channel.send('Yikes this games does\'t work, sorry')


@Command
async def c4stats(server: AbstractServer, msg: Message):
    
    user = server.GetDatabase().getStatsForUserInGuild(msg.author.id)

    await msg.channel.send(f'Stats for you: Wins {user[3]}. Losses {user[4]}.  Ties {user[5]}.')