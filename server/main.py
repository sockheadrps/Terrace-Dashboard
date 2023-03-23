import datetime
import logging
import json

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
    Response,
    Depends
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from logging import basicConfig
from uvicorn import run
from handlers import DashboardHandler, HardwareHandler, ServiceHandler, broadcast, \
    client_sets
from pydantic import BaseModel
import os
from data_handling import find_user, insert_user, check_pw
from datetime import time, timedelta
from jose import jwt

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

ACCESS_TOKEN_EXPIRES_MINUTES = 30
SECRET_KEY = "ABCDEFG"
ALGORITHM ="HS256"


class LoginCreds(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def handle_ws_commtype(data) -> dict:
    if data.get('text'):
        data = data['text']
    elif data.get('bytes'):
        data = data['bytes'].decode("utf-8")
    return json.loads(data)
    # return json.loads(data)

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


@app.post("/api/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await find_user(form_data.username)
    if user is not None and await check_pw(user, form_data.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
        acess_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires)
        return {"access_token": acess_token, "token_type": "bearer"}
    else:
        print('raised')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
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
    try:
        data = handle_ws_commtype(await client_websocket.receive())
        print(data)
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
            data = handle_ws_commtype(await client_websocket.receive())
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
