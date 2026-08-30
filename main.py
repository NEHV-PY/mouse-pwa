import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

app = FastAPI()

app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def get_index():
    return FileResponse("index.html")

@app.get("/manifest.json")
async def get_manifest():
    return FileResponse("manifest.json")

@app.get("/sw.js")
async def get_sw():
    return FileResponse("sw.js")

@app.websocket("/ws/mouse")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            tipo = data.get("type")

            if tipo == "move":
                pyautogui.moveRel(data["dx"], data["dy"])
            elif tipo == "click":
                pyautogui.click(button=data["button"])
            elif tipo == "down":
                pyautogui.mouseDown(button="left")
            elif tipo == "up":
                pyautogui.mouseUp(button="left")
            elif tipo == "scroll":
                pyautogui.scroll(int(data["dy"]))
            elif tipo == "text":
                pyautogui.write(data["text"])
            elif tipo == "key":
                pyautogui.press(data["key"])
            elif tipo == "media":
                pyautogui.press(data["action"])

    except WebSocketDisconnect:
        pass
