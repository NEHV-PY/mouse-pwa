import pyautogui
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.0

app = FastAPI()
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def get():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws/mouse")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            event = json.loads(data)
            event_type = event.get("type")

            if event_type == "move":
                pyautogui.moveRel(event.get("dx", 0), event.get("dy", 0))
            elif event_type == "scroll":
                pyautogui.scroll(event.get("clicks", 0))
            elif event_type == "click":
                pyautogui.click(button=event.get("button", "left"), clicks=event.get("clicks", 1))
            elif event_type == "drag_start":
                pyautogui.mouseDown(button="left")
            elif event_type == "drag_end":
                pyautogui.mouseUp(button="left")
            elif event_type == "key":
                key = event.get("key")
                if key:
                    pyautogui.press(key)
            elif event_type == "text":
                text = event.get("text")
                if text:
                    pyautogui.typewrite(text)
    except WebSocketDisconnect:
        pass

