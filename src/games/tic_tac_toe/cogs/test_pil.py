from PIL import Image, ImageDraw, ImageFile
import os
import io
import discord
import ctypes
from modules.tic_tac_toe.Game import Game
from discord.ext import commands


class pil_test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx, challenger: discord.Member):
        game = Game(ctx.message.author, challenger)

        await ctx.send(f"Games between: {game.player1.username} and {game.player2.username}")


def setup(client):
    client.add_cog(pil_test(client))