import asyncio

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    WebSocket,
)
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from utilities.connection_manager import Manager
from logging import basicConfig, DEBUG
from uvicorn import run
from json import loads
from utilities.clients import DashboardHandler, HardwareHandler, ServiceHandler, broadcast

connected_services = {}
hardware_clients = set()
service_clients = set()
client_set = set()
list_of_allowed_hosts = ["localhost", "127.0.0.1"]
app = FastAPI()
app.add_middleware(TrustedHostMiddleware, allowed_hosts=list_of_allowed_hosts)
connection_manager = Manager()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")
basicConfig(filename="./logs/logs.log", filemode="w", level=DEBUG)


@app.get("/favicon.ico")
async def favicon() -> None:
    # No current FavIcon - fix later
    raise HTTPException(status_code=403, detail="No favicon")


@app.get("/stats", response_class=HTMLResponse)
def stats_endpoint(request: Request) -> templates.TemplateResponse:
    """
    HTTP endpoint to serve the Server Statistics Dashboard
    :param request: HTTP Request from Client
    :return: Returns the associated HTML files to the requesting client
    """
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )


@app.websocket("/ws/stats")
async def stats_websocket(client_websocket: WebSocket) -> None:
    """
    Web Socket endpoint for communicating the "Server Statistics" in JSON to the client. Communication with the
    data visualization client is done here.
    :param client_websocket: Incoming Web Socket request.
    :return: No explicit return, just continuous requests for information from client
    """
    client = None
    await client_websocket.accept()

    # Initial connection and CONNECT event
    await client_websocket.send_json({"event": "CONNECT", "hardware-clients": [*hardware_clients],
                                      "service-clients": [*service_clients]})
    data = await client_websocket.receive()

    if "text" not in data:
        raise RuntimeError(str(data))

    text = loads(data['text'])
    if text['event'] == "CONNECT":
        match text['client-type']:
            case "DASHBOARD":
                print('dashboard connected')
                client = DashboardHandler(text, client_websocket)
            case "HARDWARE":
                client = HardwareHandler(text, client_websocket)
                hardware_clients.add(client.client_name)
            case "SERVICE":
                print('SERVICE CONNECTED')
                client = ServiceHandler(text, client_websocket)
                service_clients.add(client.client_name)

        client_set.add(client) # possible error when client type is invalid

    # Typical event communication
    while True:
        data = await client_websocket.receive()
        if "text" in data:
            print("data is", data)
            text = loads(data["text"])
            await broadcast(client_set, text, client)

        # Handling for websocket disconnect code
        if data["type"] == "websocket.disconnect":
            client_set.remove(client)
            if isinstance(client, HardwareHandler):
                hardware_clients.remove(client.client_name)
                await broadcast(client_set,
                                {"event": "HARDWARE-DISCONNECT", "client-name": client.client_name}, client)
                break
            if isinstance(client, ServiceHandler):
                service_clients.remove(client.client_name)
                await broadcast(client_set,
                                {"event": "SERVICE-DISCONNECT", "client-name": client.client_name}, client)
                break


if __name__ == "__main__":
    run(app, port=80, host="0.0.0.0")
