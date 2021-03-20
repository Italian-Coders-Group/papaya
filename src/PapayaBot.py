import os
import sys

import core

core.logging.init_logging(
	filename='./logs/latest.log'
)


core.Bot().run(
	token=os.environ.get( 'TOKEN_TEST' if '--test' in sys.argv else 'TOKEN' )
)