import os

import core

core.logging.init_logging(
	filename='../logs/latest.log'
)


x = core.Bot()
x.run(
	token=os.environ.get('TOKEN')
)



