from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    WebSocket,
    WebSocketDisconnect
)
from uvicorn import run

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from logging import basicConfig, DEBUG
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from utilities.handlers import DashboardHandler, HardwareHandler, ServiceHandler, broadcast
clients = {"DASHBOARD": [], "HARDWARE": [], "SERVICE": []}
client_types = {"DASHBOARD": DashboardHandler, "HARDWARE": HardwareHandler, "SERVICE": ServiceHandler}
list_of_allowed_hosts = ["localhost", "127.0.0.1"]
app = FastAPI()
app.add_middleware(TrustedHostMiddleware, allowed_hosts=list_of_allowed_hosts)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
basicConfig(filename="./logs/logs.log", filemode="w", level=DEBUG)

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/favicon.ico")
async def favicon() -> None:
    # No current FavIcon - fix later
    raise HTTPException(status_code=403, detail="No favicon")

@app.websocket("/ws/stats")
async def stats_websocket(client_websocket: WebSocket):
    client = None    
    await client_websocket.accept()
    try:
        data = await client_websocket.receive_json()
    except Exception as e:
        raise 
    if data['event'] == "CONNECT":
        client = client_types[data["client-type"]](data, client_websocket)
        clients[data['client-type']].append(client)
        await broadcast(clients, data, client)
    while True:
    # Typical event communication
        try:
            data = await client_websocket.receive_json()
            await broadcast(clients, data, client)

        except WebSocketDisconnect:
            clients[data['client-type']].remove(client)
            await broadcast(clients, {"event": "DISCONNECT",  "client-type": client.client_type,
                                        "client-name": client.client_name}, client)
            break
if __name__ == "__main__":
    run(app, port=8000, host="0.0.0.0")
