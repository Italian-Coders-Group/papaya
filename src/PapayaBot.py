import os

import core

core.logging.init_logging(
	filename='../logs/latest.log'
)


core.Bot().run(
	token=os.environ.get('TOKEN')
)



