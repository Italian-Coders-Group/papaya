import os

import core

core.logging.init_logging(
	filename='../logs/latest.log'
)


x = core.Bot()

import modules

x.run(
	token=os.environ.get('TOKEN')
)



