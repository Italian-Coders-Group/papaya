import threading
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
import os
from PIL import Image


app = FastAPI()


@app.get('/tictactoe/{gameID}')
async def getGameImage(gameID: str):
	folderPath = './modules/tic_tac_toe/src/tictactoe_images'
	image = f'{folderPath}/{gameID}.png'
	return image


def run():
	uvicorn.run(app, port=6060)


def createApp():
	apiThread = threading.Thread(target=run)

	apiThread.start()
	return