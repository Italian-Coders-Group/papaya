import traceback

import discord
from discord import Embed, Color


def embed(title: str, content: str, color: Color) -> Embed:
	data = Embed(
		color=color,
		title=title,
		description=content,
		type='rich_embed'
	)
	return data


def getColor(RGB: str) -> Color:
	rgb = RGB.split(',')
	r: int = int( rgb[0] )
	g: int = int( rgb[1] )
	b: int = int( rgb[2] )
	return discord.colour.Color.from_rgb(r, g, b)


def getTracebackEmbed( exc: Exception ) -> Embed:
	prettyExc = ''.join( traceback.format_exception( type( exc ), exc, exc.__traceback__ ) )
	print( prettyExc )
	return embed(
		title='Uncaught Exception!',
		content=prettyExc,
		color=discord.Color.red()
	)
