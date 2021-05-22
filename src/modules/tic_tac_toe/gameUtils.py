from typing import List, Dict, Tuple


def check_for_win(grid: List[ List ], sign: str) -> bool:
	"""
	Questo dovrebbe essere la ricerca per i punti dato il segno che ha il giocatore.

	dovrebbe essere chiamata tipo Game.check_for_win(player1.sign) o qualcosa del genere
	:param grid:
	:param sign:
	:return:
	"""
	return ((grid[0][0] == sign and grid[0][1] == sign and grid[0][2] == sign) or
	        (grid[1][0] == sign and grid[1][1] == sign and grid[1][2] == sign) or
	        (grid[2][0] == sign and grid[2][1] == sign and grid[2][2] == sign) or
	        (grid[0][2] == sign and grid[1][2] == sign and grid[2][2] == sign) or
	        (grid[0][1] == sign and grid[1][1] == sign and grid[2][1] == sign) or
	        (grid[0][0] == sign and grid[1][0] == sign and grid[2][0] == sign) or
	        (grid[0][0] == sign and grid[1][1] == sign and grid[2][2] == sign) or
	        (grid[0][2] == sign and grid[1][1] == sign and grid[2][0] == sign))


def from1Dto2D(move: int):
	table: Dict[str, tuple] = {
		'1': (0, 0),
		'2': (0, 1),
		'3': (0, 2),
		'4': (1, 0),
		'5': (1, 1),
		'6': (1, 2),
		'7': (2, 0),
		'8': (2, 1),
		'9': (2, 2)
	}
	return table[str(move)]


def from2Dto1D(pos: tuple):
	table: Dict[Tuple[int, int], int] = {
		(0, 0): 1,
		(0, 1): 2,
		(0, 2): 3,
		(1, 0): 4,
		(1, 1): 5,
		(1, 2): 6,
		(2, 0): 7,
		(2, 1): 8,
		(2, 2): 9
	}
	return table[pos]