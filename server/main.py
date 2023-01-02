from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    WebSocket,
    WebSocketDisconnect
)
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from logging import basicConfig, DEBUG
from uvicorn import run
from handlers import DashboardHandler, HardwareHandler, ServiceHandler, broadcast
import argparse

clients = {"DASHBOARD": [], "HARDWARE": [], "SERVICE": []}
client_types = {"DASHBOARD": DashboardHandler, "HARDWARE": HardwareHandler, "SERVICE": ServiceHandler}


list_of_allowed_hosts = ["localhost", "127.0.0.1"]
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")
basicConfig(filename="../logs/logs.log", filemode="w", level=DEBUG)


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


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_endpoint(request: Request) -> templates.TemplateResponse:
    """
    HTTP endpoint to serve the Dashboard
    :param request: HTTP Request from Client
    :return: Returns the associated web files to the requesting client
    """
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )


@app.websocket("/ws/stats")
async def websocket_endpoint(client_websocket: WebSocket) -> None:
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
    parser = argparse.ArgumentParser(description="Terrace Dashboard Server")
    parser.add_argument('host', metavar="host", type=str, help="Enter the host URL")
    args = parser.parse_args()
    host = args.host
    run(app, port=8080, host=host)
