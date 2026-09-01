import pyautogui
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import json
import os

# Configuración de seguridad de PyAutoGUI
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

app = FastAPI()

# Servir archivos estáticos (para manifest.json, iconos, etc.)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get_index():
    return FileResponse("index.html")

@app.get("/manifest.json")
async def get_manifest():
    return FileResponse("manifest.json")

@app.websocket("/ws/mouse")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data_text = await websocket.receive_text()
            data = json.loads(data_text)
            event_type = data.get("type")

            # Mover cursor
            if event_type == "move":
                dx = data.get("dx", 0)
                dy = data.get("dy", 0)
                pyautogui.moveRel(dx, dy)

            # Clics de ratón
            elif event_type == "click":
                btn = data.get("button", "left")
                clicks = data.get("clicks", 1)
                pyautogui.click(button=btn, clicks=clicks)

            # Scroll
            elif event_type == "scroll":
                clicks = data.get("clicks", 0)
                pyautogui.scroll(clicks)

            # Drag and Drop
            elif event_type == "drag_start":
                pyautogui.mouseDown(button="left")
            elif event_type == "drag_end":
                pyautogui.mouseUp(button="left")

            # GESTO MULTITÁCTIL: ZOOM (Pinch-to-zoom)
            elif event_type == "zoom":
                direction = data.get("direction")
                if direction == "in":
                    pyautogui.hotkey('ctrl', '+')
                elif direction == "out":
                    pyautogui.hotkey('ctrl', '-')

            # Entrada de texto y teclas
            elif event_type == "text":
                pyautogui.write(data.get("text", ""))
            elif event_type == "key":
                pyautogui.press(data.get("key"))
            elif event_type == "hotkey":
                pyautogui.hotkey(*data.get("keys", []))

            # Comandos del sistema
            elif event_type == "system":
                cmd = data.get("cmd")
                if cmd == "sleep":
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    except WebSocketDisconnect:
        pass
