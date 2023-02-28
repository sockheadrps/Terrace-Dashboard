import logging

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
    Response
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from logging import basicConfig
from uvicorn import run
from handlers import DashboardHandler, HardwareHandler, ServiceHandler, broadcast, \
    client_sets
from pydantic import BaseModel
import os
from data_handling import find_user, insert_user, check_pw


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


class LoginCreds(BaseModel):
    username: str
    password: str


app = FastAPI()
app.mount(
    "/_app/immutable/", StaticFiles(directory="../Terrace-kit/build/_app/immutable/"),
    name="static"
)

app.mount(
    "/assets/", StaticFiles(directory="../Terrace-kit/build/"),
    name="assets"
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.get("/", response_class=FileResponse)
def dashboard_endpoint() -> FileResponse:
    """
    HTTP endpoint to serve the Dashboard
    :param request: HTTP Request from Client
    :return: Returns the associated web files to the requesting client
    """
    return FileResponse("../Terrace-Kit/build/index.html")


@app.post("/api/register")
async def create_user_endpoint(data: LoginCreds, response: Response):
    if await find_user(data.username):
        response.status_code = status.HTTP_409_CONFLICT
    else:
        await insert_user(data.username, data.password)
        response.status_code = status.HTTP_201_CREATED


@app.post("/api/login")
async def login_endpoint(data: LoginCreds, response: Response):
    user = await find_user(data.username)
    if user is not None and await check_pw(user, data.password):
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST





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
        await client_websocket.send_json({"event": "SERVER-CONNECT"})
        client = client_types[data["client-type"]](data, client_websocket)
        clients[data["client-type"]].append(client)
        await broadcast(clients, data, client)

    while True:
        # Typical event communication
        try:
            data = await client_websocket.receive_json()
            print(f"data {data}")
            await broadcast(clients, data, client)

            # graceful disconnects
            if data["event"] == "DISCONNECT":
                clients[data["client-type"]].remove(client)
                await broadcast(
                    clients,
                    {
                        "event": "DISCONNECT",
                        "client-type": client.client_type,
                        "client-name": client.client_name,
                    },
                    client)
                break

        # non-graceful disconnects
        except WebSocketDisconnect:
            print(data)
            if data['client-type'] != "DASHBOARD":
                client_sets[data["client-type"]].remove(data['client-name'])
            if client in clients[data["client-type"]]:
                clients[data["client-type"]].remove(client)
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
            print('second')
            logging.warning(e)
            raise e


if __name__ == "__main__":
    run(app, port=8081, host="0.0.0.0", ws_ping_interval=10, ws_ping_timeout=10)
