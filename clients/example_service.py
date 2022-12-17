import websockets
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
import asyncio
import json

"""
This is a basic example client. Handle for server events in the match data['event'] event logic loop.
client_name currently may not contain spaces, use "-" in place of spaces. (This is due to current javascript logic
and will be refactored later to fix this requirement.) There is further work to be done for exception handling
when this client closes, but it functions fully at the moment.
"""

client_name = "Example-Service"
client_type = "SERVICE"


async def client():
    data = None
    try:
        async with websockets.connect("ws://localhost:80/ws/stats") as websocket:
            # Initial connection
            connect_event = {"event": "CONNECT", "client-type": client_type, "client-name": client_name}
            await websocket.send(json.dumps(connect_event))
            while True:
                try:
                    data = json.loads(await websocket.recv())
                    if data:
                        print(data)
                        # SERVER EVENTS
                        match data['event']:
                            case "TEST-EVENT":
                                connect_response = {"event": "TEST-EVENT", "client-name": client_name,
                                                    "event-response": "OK"}
                                await websocket.send(json.dumps(connect_response))
                        data = None

                except ConnectionClosedError:
                    print("The server has refused connection. Is the server running?")

    except ConnectionRefusedError:
        print("Server is either offline, or connection point is wrong!")
    finally:
        # Send disconnect message if service closes and there is a websocket connection
        try:
            disconnect_event = {"event": "DISCONNECT", "client-type": client_type, "client-name": client_name}
            await websocket.send(json.dumps(disconnect_event))
        except ConnectionClosedOK:
            print("Client successfully closed")


asyncio.run(client())
