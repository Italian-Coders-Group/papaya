from typing import List


class PapUser:

	userID: int
	personalPrefix: str
	permissions: List[bool]

	def __init__( self, discordID: int, personalPrefix: str, permissions: str ):
		self.userID = discordID
		self.personalPrefix = personalPrefix
		self.permissions = PapUser.deserializePermissions(permissions)

	@staticmethod
	def serializePermissions( perms: List[bool] ) -> str:
		return ''.join( [ str( int( value ) ) for value in perms ] )

	@staticmethod
	def deserializePermissions( perms: str ) -> List[bool]:
		return [ bool( int( value ) ) for value in perms ]