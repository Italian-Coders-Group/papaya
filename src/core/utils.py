import traceback
from typing import Any, List, Union, KeysView, ItemsView, Tuple, Callable
import math

import discord
from discord import Embed, Color


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


def getColor(RGB: str) -> Color:
	"""
	Converts a string of R,G,B values to a discord Color object
	:param RGB: the color
	:return: color obj
	"""
	rgb = RGB.split(',')
	r: int = int( rgb[0] )
	g: int = int( rgb[1] )
	b: int = int( rgb[2] )
	return discord.colour.Color.from_rgb(r, g, b)


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


def placeHolderFunc(ph0=None, ph1=None):
	""" Just a placeholder for functions that require a function """
	pass
