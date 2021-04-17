from dataclasses import dataclass

from typing import List


@dataclass
class PapUser:

	discordID: int
	personalPrefix: str
	permissions: List[bool]

	@staticmethod
	def serializePermissions( perms: List[bool] ) -> str:
		return ''.join( str( int( value ) ) for value in perms )

	@staticmethod
	def deserializePermissions( perms: str ) -> List[bool]:
		return [ bool( int( value ) ) for value in perms ]