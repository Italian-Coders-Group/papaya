import math
import traceback
from typing import Any, List, Union, KeysView, ItemsView, Tuple, Callable
from random import choice
import string

import discord
from discord import Embed, Color


def color_palette():
	"""
	Returns a random color from a Papaya fruit palette.
	:return: Random str("r,g,b") from papaya fruit palette
	"""
	colors = [
		"246,125,35",
		"253,150,58",
		"255,168,62",
		"186,163,49",
		"160,157,51"
	]
	return choice(colors)


def getAuthors() -> Callable[[], Tuple[int, int]]:
	def authors() -> Tuple[int, int]:
		# ENDER, MR
		return 350938367405457408, 326436392940863499
	return authors


def embed(title: str, content: str, color: Color) -> Embed:
	"""
	Creates an embed from its data
	:param title: title of the embed
	:param content: the content of the embed, only text
	:param color: the color of the line of the embed
	:return: the embed
	"""
	data = Embed(
		color=color,
		title=title,
		description=content,
		type='rich_embed'
	)
	return data


def getColor(RGB: str = "255, 255, 255", random: bool = False) -> Color:
	"""
	Converts a string of R,G,B values to a discord Color object
	:param random:
	:param RGB: the color
	:return: color obj
	"""

	if random:
		rgb = color_palette().split(',')

	else:
		rgb = RGB.split(',')

	r: int = int( rgb[0] )
	g: int = int( rgb[1] )
	b: int = int( rgb[2] )
	returnColor = discord.colour.Color.from_rgb(r, g, b)

	return returnColor


def getTracebackEmbed( exc: Exception ) -> Embed:
	"""
	Create an embed from an exception object
	:param exc: the exception to transform
	:return: the final Embed
	"""
	prettyExc = ''.join( traceback.format_exception( type( exc ), exc, exc.__traceback__ ) )
	print( prettyExc )
	return embed(
		title='Uncaught Exception!',
		content=prettyExc,
		color=discord.Color.red()
	)


def copyList(tocopy: Union[ List, KeysView, ItemsView] ) -> List[Any]:
	"""
	Copies an iterable to another list
	:param tocopy: itarable to copy
	:return: the copied list
	"""
	return [ x for x in tocopy]


def check_distance(x0, y0, x1, y1):
	"""
	Utility I guess

	:param x0:
	:param y0:
	:param x1:
	:param y1:
	:return:
	"""
	distance = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
	if distance == 1:
		return True


def genRandomString( size: int = 5) -> str:
	"""
	Generates a random string of the given size
	:param size:
	:return: String
	"""
	chars = string.ascii_letters + string.digits

	return ''.join(choice(chars) for _ in range(size))


def placeHolderFunc(ph0=None, ph1=None):
	""" Just a placeholder for functions that require a function """
	pass
