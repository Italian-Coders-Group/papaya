from core.commandList import Command
from core.abc.server import AbstractServer
from core.database.database import Database
from core.dataclass import PapGame, PapUser, PapStats
from core.dataclass import utils as gameUtils
from discord import Message, File, Member
from core.utils import embed, getColor
from PIL import Image
import io
import os
from core.fileSystem import File as localFile
from core import utils


@Command
async def mystats(server: AbstractServer, msg: Message):
    warnMsg = False
    msgContent = msg.content.split(' ', 1)
    if len(msgContent) > 1:
        validGametype = server.GetDatabase().hasGametype(msgContent[1])
        if not validGametype[0]:
            gameType = "any"
            warnMsg = True
        else:
            gameType = msgContent[1]
    else:
        gameType = "any"
    user: PapStats = server.GetDatabase().getStatsForUserInGuild(msg.author.id, gameType)
    if warnMsg:
        await msg.channel.send(f"That is not a valid category. please look it up using command 'category'")
    else:
        await msg.channel.send(f"Your rank in {user.gameType} is {user.rank}")


@Command
async def stats(server: AbstractServer, msg: Message):
    warnMsg = False
    msgContent = msg.content.split(' ', 2)

    user = msgContent[1][3:-1]
    userName = msg.mentions[0]
    print(msgContent)
    if len(msgContent) > 1:
        validGametype = server.GetDatabase().hasGametype(msgContent[2])
        if not validGametype[0]:
            gameType = "any"
            warnMsg = True
        else:
            gameType = msgContent[2]
    else:
        gameType = "any"
    user: PapStats = server.GetDatabase().getStatsForUserInGuild(int(user), gameType)
    if warnMsg:
        await msg.channel.send(f"That is not a valid category. please look it up using command 'category'")
    else:
        await msg.channel.send(f"{userName}'s rank in {user.gameType} is {user.rank}")


@Command
async def category(server: AbstractServer, msg: Message):
    allGameTypes = server.GetDatabase().getGametypes()
    listEmbed = embed(
        title="Categories",
        content="\n".join(gameType for gameType in allGameTypes),
        color=getColor(RGB="255, 0, 0")
    )
    listEmbed.set_thumbnail(url="https://lh3.googleusercontent.com/proxy/iGs72HNJCfm445aBtT8dxVquNExB5imv0ynMdO_QrdDOpo-kZaUmQ9_2Dp81W56uTZCOFuVTmnsd-SXtj6essFtzN7aXrnil_TfFpk_jqYwVQNLxWFGfKZCF59JC0A-5_p0kLF5_M4HxBioZpQ")
    await msg.channel.send(embed=listEmbed)
