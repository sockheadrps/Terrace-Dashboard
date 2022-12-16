from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    WebSocket,
    WebSocketDisconnect
)
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from logging import basicConfig, DEBUG
from uvicorn import run
from utilities.handlers import DashboardHandler, HardwareHandler, ServiceHandler, broadcast

clients = {"DASHBOARD": [], "HARDWARE": [], "SERVICE": []}
client_types = {"DASHBOARD": DashboardHandler, "HARDWARE": HardwareHandler, "SERVICE": ServiceHandler}


list_of_allowed_hosts = ["localhost", "127.0.0.1"]
app = FastAPI()
app.add_middleware(TrustedHostMiddleware, allowed_hosts=list_of_allowed_hosts)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")
basicConfig(filename="./logs/logs.log", filemode="w", level=DEBUG)


@app.get("/favicon.ico")
async def favicon() -> None:
    # No current FavIcon - fix later
    raise HTTPException(status_code=403, detail="No favicon")


@app.get("/dashboard", response_class=HTMLResponse)
def stats_endpoint(request: Request) -> templates.TemplateResponse:
    """
    HTTP endpoint to serve the Dashboard
    :param request: HTTP Request from Client
    :return: Returns the associated web files to the requesting client
    """
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )


@app.websocket("/ws/stats")
async def stats_websocket(client_websocket: WebSocket) -> None:
    """
    Web Socket endpoint for client communication
    :param client_websocket: Incoming Web Socket request
    :return: No explicit return
    """
    client = None
    await client_websocket.accept()

    # Initial connection and CONNECT event
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
    run(app, port=80, host="0.0.0.0")
