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

hardware_clients = set()
service_clients = set()
client_set = set()
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
    # await client_websocket.send_json({"event": "CONNECT", "hardware-clients": [*hardware_clients],
    #                                   "service-clients": [*service_clients]})
    data = await client_websocket.receive_json()
    print(data, type(data))

    if data['event'] == "CONNECT":
        match data['client-type']:
            case "DASHBOARD":
                client = DashboardHandler(data, client_websocket)
            case "HARDWARE":
                client = HardwareHandler(data, client_websocket)
                hardware_clients.add(client.client_name)
            case "SERVICE":
                client = ServiceHandler(data, client_websocket)
                service_clients.add(client.client_name)

        client_set.add(client) # possible error when client type is invalid
        await broadcast(client_set, data, client)

    # Typical event communication
    while True:
        try:
            data = await client_websocket.receive_json()
            await broadcast(client_set, data, client)

        except WebSocketDisconnect:
            client_set.remove(client)
            if isinstance(client, HardwareHandler):
                hardware_clients.remove(client.client_name)
                await broadcast(client_set,
                                {"event": "DISCONNECT",  "client-type": client.client_type,
                                 "client-name": client.client_name}, client)
                break
            if isinstance(client, ServiceHandler):
                service_clients.remove(client.client_name)
                print(f"client names {service_clients}")
                await broadcast(client_set,
                                {"event": "DISCONNECT",  "client-type": client.client_type,
                                 "client-name": client.client_name}, client)
                break


if __name__ == "__main__":
    run(app, port=80, host="0.0.0.0")
