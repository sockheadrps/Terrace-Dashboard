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
    Depends,
    Cookie
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from logging import basicConfig
from uvicorn import run
from handlers import DashboardHandler, ServiceHandler, broadcast, \
    client_sets, DebuggerHandler
from pydantic import BaseModel
import os
from data_handling import find_user, insert_user, check_pw
from datetime import time, timedelta
from jose import jwt
from jose.jwt import JWTError, ExpiredSignatureError
from typing import Optional

path = "logs"
# Check whether the specified path exists or not
isExist = os.path.exists(path)
if not isExist:
    # Create a new directory because it does not exist
    os.makedirs(path)
    print("Created logs dir")

clients = {"DASHBOARD": [], "SERVICE": [], "DEBUGGER": []}
client_types = {
    "DASHBOARD": DashboardHandler,
    "SERVICE": ServiceHandler,
    "DEBUGGER": DebuggerHandler,
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
    if data.get('type') == "websocket.disconnect":
        return data

    else:
        if data.get('text'):
            data = data['text']
        elif data.get('bytes'):
            data = data['bytes'].decode("utf-8")
        return json.loads(data)

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


# @app.get("/", response_class=FileResponse)
@app.get("/")
def dashboard_endpoint(request: Request) -> FileResponse:
    """
    HTTP endpoint to serve the Dashboard
    :param request: HTTP Request from Client
    :param jwt: client json web token
    :return: Returns the associated web files to the requesting client
    """
    try:
        if request.cookies.get("jwt") is not None:
            claims = jwt.decode(jwt, SECRET_KEY)
            print(claims)
            print('token verification succeeded')
            return FileResponse("../Terrace-kit/build/index.html")
        raise JWTError
    except JWTError:
        print('send to login')
        return  {"sendto": "login"}
        # return FileResponse("../Terrace-kit/build/login.html")
    except ExpiredSignatureError:
        print('REFRESH')
        # validate refresh token
        # generate new jwt and new refresh


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
async def login_for_access_token(response: Response,
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    user = await find_user(form_data.username)
    if user is not None and await check_pw(user, form_data.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
        acess_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires)
        response.set_cookie(key="fakesession", value="fake-cookie-session-value")

        return {"access_token": acess_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

@app.post("/api/token-refresh", response_model=Token)
async def access_token_refresh(response: Response,
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    user = await find_user(form_data.username)
    if user is not None and await check_pw(user, form_data.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
        acess_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires)
        response.set_cookie(key="fakesession", value="fake-cookie-session-value")
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


    data = handle_ws_commtype(await client_websocket.receive())


    # Initial connection 
    if data.get("event") == "CONNECT":
        await client_websocket.send_json({"event": "SERVER-CONNECT"})
        client = client_types[data["client-type"]](data, client_websocket, data["client-name"])
        clients[data["client-type"]].append(client)
        await broadcast(clients, data, client)

    while True:
        try:
            data = handle_ws_commtype(await client_websocket.receive())
            if data.get("type") == "websocket.disconnect" or data.get("event") == "DISCONNECT":
                data = {
                            "event": "DISCONNECT",
                            'client-type': client.client_type, 
                            'client-name': client.client_name
                        }
                raise WebSocketDisconnect()

            
            # Typical communication
            await broadcast(clients, data, client)

    
        except WebSocketDisconnect:
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


if __name__ == "__main__":
    run(app, port=8081, host="192.168.1.136", ws_ping_interval=10, ws_ping_timeout=10)
