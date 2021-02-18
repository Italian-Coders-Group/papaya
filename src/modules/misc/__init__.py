from core.commandList import Command
from core.abc.server import AbstractServer
from core.database.database import Database
from core.dataclass import PapGame, PapUser
from core.dataclass import utils as gameUtils
from discord import Message, File
from core.utils import embed, getColor
from PIL import Image
import io
import os
from core.fileSystem import File as localFile
from core import utils


@Command
async def mystats(server: AbstractServer, msg: Message):
    msgContent = msg.content.split(" ")
    User = server.GetDatabase().getStatsForUserInGuild(msg.author.id, msgContent[1] if len(msgContent) > 1 else "any")
