from core import moduleUtils
from core.eventSystem import Listener


@Listener
async def onReload():
	from . import acceptSystem
	moduleUtils.reload(acceptSystem)
	acceptSystem.AcceptSystem()
