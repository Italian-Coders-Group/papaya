from datetime import datetime
from typing import List


def getRandomGameID(players: List[int]) -> str:
	n = players[0]
	# if is against the same player use that player as salt
	if ( len(players) == 2 ) and ( players[0] == players[1] ):
		return f'{str( datetime.now() ).replace( " ", "," )}-{n}'
	# if aganist other players use all players as salt (XOR them together)
	for index, identifier in enumerate( players ):
		if index != 0:
			n = n ^ identifier
	return f'{str( datetime.now() ).replace(" ", ",")}-{n}'
