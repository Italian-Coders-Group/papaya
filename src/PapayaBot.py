import os
import sys

import core


core.Bot().initLoggingAndRun(
	filename='../logs/latest.log',
	token=os.environ.get( 'TOKEN_TEST' if '--test' in sys.argv else 'TOKEN' )
)
