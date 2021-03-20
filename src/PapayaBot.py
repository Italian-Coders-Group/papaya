import os
import sys

import botframework


botframework.Bot().initLoggingAndRun(
	filename='../logs/latest.log',
	token=os.environ.get( 'TOKEN_TEST' if '--test' in sys.argv else 'TOKEN' )
)
