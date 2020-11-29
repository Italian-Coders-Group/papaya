from PIL import Image, ImageDraw, ImageFile
import os
import discord
from discord.ext import commands


class pil_test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        await ctx.send("ERR")


def setup(client):
    client.add_cog(pil_test(client))