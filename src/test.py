from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import registry

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True, future=True)


mapper_registry = registry()
Base = mapper_registry.generate_base()


class Guild(Base):
	__tablename__ = 'guilds'

	identifier = Column( Integer )


class User(Base):
	__tablename__ = 'users'

	discordID = Column( Integer, primary_key=True )
	guildID = Column( ForeignKey('guilds.identifier'), primary_key=True )
	personalPrefix = Column( String(4) )
	permissions = Column( Text )


mapper_registry.metadata.create_all(engine)