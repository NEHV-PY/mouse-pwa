from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
import pyautogui

app = FastAPI()

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

@app.get("/")
async def get():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/manifest.json")
async def manifest():
    return FileResponse("manifest.json")

@app.get("/service-worker.js")
async def service_worker():
    return FileResponse("service-worker.js")

@app.websocket("/ws/mouse")
async def websocket_mouse_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            tipo_evento = data.get("type", "move")

            if tipo_evento == "move":
                delta_x = data.get("dx", 0)
                delta_y = data.get("dy", 0)
                pyautogui.moveRel(delta_x, delta_y)

            elif tipo_evento == "click":
                boton = data.get("button", "left")
                pyautogui.click(button=boton)

            elif tipo_evento == "scroll":
                delta_y = data.get("dy", 0)
                pyautogui.scroll(int(delta_y))

    except WebSocketDisconnect:
        print("(estado_conexion = Desconectado)")
