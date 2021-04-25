import os
import sys

import core
from src.api import createApp


createApp()
core.Bot().initLoggingAndRun(
	filename='../logs/latest.log',
	token=os.environ.get( 'TOKEN_TEST' if '--test' in sys.argv else 'TOKEN' )
)
