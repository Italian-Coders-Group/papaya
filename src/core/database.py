import sqlalchemy
from sqlalchemy import text, Column, UniqueConstraint, Integer


class Database:

	engine: sqlalchemy.engine.Engine
	guilds: sqlalchemy.Table

	def __init__(self):
		self.engine = sqlalchemy.create_engine("sqlite:///./db", echo=True, future=True)
		if not self.engine.has_table('guilds'):
			self.guilds = sqlalchemy.Table(
				'some_table', None,
				Column( 'id', Integer, primary_key=True ),
				Column( 'data', Integer ),
				UniqueConstraint( 'id', 'data', sqlite_on_conflict='IGNORE' )
			)

	def loadGuild( self, identifier: int ) -> dict:
		with self.engine.connect() as conn:
			result = conn.execute( text( "select 'hello world'" ) )
		res = result.all()
		return {}


def loadGuild(identifier: int) -> dict:
	return __instance.loadGuild()


__instance: Database = Database()