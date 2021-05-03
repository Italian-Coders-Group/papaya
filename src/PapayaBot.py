import os
import sys

import core
# from src.api import createApp


# createApp() REMOVING API, NO NEED FOR IT NOW
core.Bot().initLoggingAndRun(
	filename='../logs/latest.log',
	token=os.environ.get( 'TOKEN_TEST' if '--test' in sys.argv else 'TOKEN' )
)
