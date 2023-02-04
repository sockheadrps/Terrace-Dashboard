import logging

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from logging import basicConfig
from uvicorn import run
from handlers import DashboardHandler, HardwareHandler, ServiceHandler, broadcast
import os


path = "logs"
# Check whether the specified path exists or not
isExist = os.path.exists(path)
if not isExist:
    # Create a new directory because it does not exist
    os.makedirs(path)
    print("Created logs dir")

clients = {"DASHBOARD": [], "HARDWARE": [], "SERVICE": []}
client_types = {
    "DASHBOARD": DashboardHandler,
    "HARDWARE": HardwareHandler,
    "SERVICE": ServiceHandler,
}


app = FastAPI()
app.mount(
    "/assets", StaticFiles(directory="../Terrace-Svelte/dist/assets"), name="static"
)
basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    filename="logs/server.log",
    encoding="utf-8",
    level=logging.DEBUG,
)


@app.get("/favicon.ico")
async def favicon() -> None:
    # No current FavIcon - fix later
    raise HTTPException(status_code=403, detail="No favicon")


@app.get("/", status_code=200)
def home_endpoint(request: Request):
    """
    HTTP home endpoint
    :param request: HTTP Request from Client
    :return: Returns 200 status code
    """
    return {"status_code": "200"}


@app.get("/dashboard", response_class=FileResponse)
def dashboard_endpoint() -> FileResponse:
    """
    HTTP endpoint to serve the Dashboard
    :param request: HTTP Request from Client
    :return: Returns the associated web files to the requesting client
    """
    return FileResponse("../Terrace-Svelte/dist/index.html")


@app.websocket("/ws/stats")
async def websocket_endpoint(client_websocket: WebSocket) -> None:
    """
    Web Socket endpoint for client communication
    :param client_websocket: Incoming Web Socket request
    :return: No explicit return
    """
    client = None
    await client_websocket.accept()
    try:
        data = await client_websocket.receive_json()
    except Exception as e:
        logging.warning(e)
        raise e

    # Initial connection and CONNECT event
    if data["event"] == "CONNECT":
        await client_websocket.send_json({"event": "CONNECT"})
        client = client_types[data["client-type"]](data, client_websocket)
        clients[data["client-type"]].append(client)
        await broadcast(clients, data, client)

    while True:
        # Typical event communication
        try:
            data = await client_websocket.receive_json()
            await broadcast(clients, data, client)

        except WebSocketDisconnect:
            await broadcast(
                clients,
                {
                    "event": "DISCONNECT",
                    "client-type": client.client_type,
                    "client-name": client.client_name,
                },
                client,
            )
            break
        except Exception as e:
            logging.warning(e)
            raise e


if __name__ == "__main__":
    run(app, port=8081, host="0.0.0.0", ws_ping_interval=10, ws_ping_timeout=10)
