from typing import List, Dict, Tuple


def check_for_win(grid: List[ List ], sign: str) -> bool:
	"""
	Questo dovrebbe essere la ricerca per i punti dato il segno che ha il giocatore.

	dovrebbe essere chiamata tipo Game.check_for_win(player1.sign) o qualcosa del genere
	:param grid:
	:param sign:
	:return:
	"""
	if grid[0][0] == sign and grid[0][1] == sign and grid[0][2] == sign:
		return True, [1, 2, 3]
	elif grid[1][0] == sign and grid[1][1] == sign and grid[1][2] == sign:
		return True, [4, 5, 6]
	elif grid[2][0] == sign and grid[2][1] == sign and grid[2][2] == sign:
		return True, [7, 8, 9]
	elif grid[0][2] == sign and grid[1][2] == sign and grid[2][2] == sign:
		return True, [3, 6, 9]
	elif grid[0][1] == sign and grid[1][1] == sign and grid[2][1] == sign:
		return True, [2, 5, 8]
	elif grid[0][0] == sign and grid[1][0] == sign and grid[2][0] == sign:
		return True, [1, 4, 7]
	elif grid[0][0] == sign and grid[1][1] == sign and grid[2][2] == sign:
		return True, [1, 5, 9]
	elif grid[0][2] == sign and grid[1][1] == sign and grid[2][0] == sign:
		return True, [3, 5, 7]
	else:
		return False, []


def from1Dto2D(move: int):
	table: Dict[str, tuple] = {
		1: (0, 0),
		2: (0, 1),
		3: (0, 2),
		4: (1, 0),
		5: (1, 1),
		6: (1, 2),
		7: (2, 0),
		8: (2, 1),
		9: (2, 2)
	}
	return table[move]


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


def positionToPixel(pos: tuple):
	table: Dict[Tuple[int, int], Tuple[int, int, int, int]] = {
		(0, 0): (0, 0, 49, 49),
		(0, 1): (53, 0, 102, 49),
		(0, 2): (106, 0, 155, 49),
		(1, 0): (0, 53, 49, 102),
		(1, 1): (53, 53, 102, 102),
		(1, 2): (106, 53, 155, 102),
		(2, 0): (0, 106, 49, 155),
		(2, 1): (53, 106, 102, 155),
		(2, 2): (106, 106, 155, 155)
	}
	return table[pos]