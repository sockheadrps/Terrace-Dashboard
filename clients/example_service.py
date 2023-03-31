import websockets
from websockets.exceptions import ConnectionClosedError
import asyncio
import json
import argparse
import random

"""
This is a basic example client. Handle for server events in the match data['event'] event logic loop.
client_name currently may not contain spaces, use "-" in place of spaces. (This is due to current javascript logic
and will be refactored later to fix this requirement.) There is further work to be done for exception handling
when this client closes, but it functions fully at the moment.
"""

client_type = "SERVICE"


async def client(host, name):
    stream_task = None
    try:
        async with websockets.connect(f"ws://{host}:8081/ws/stats") as websocket:
            # Initial connection
            connect_event = {
                "event": "CONNECT",
                "client-type": client_type,
                "client-name": name,
            }
            await websocket.send(json.dumps(connect_event))
            while True:
                try:
                    data = json.loads(await websocket.recv())
                    if data:
                        print(data)
                        # SERVER EVENTS
                        if stream_task is None:
                            stream_task = asyncio.create_task(client_stream(websocket))
                        match data["event"]:
                            case "TEST-EVENT":
                                connect_response = {
                                    "event": "TEST-EVENT",
                                    "client-name": name,
                                    "event-response": "OK",
                                }
                                await websocket.send(json.dumps(connect_response))
                        data = None

                except ConnectionClosedError:
                    print("The server has shut down!")
                    break

    except ConnectionRefusedError:
        print("Server is either offline, or connection point is wrong!")

async def client_stream(websocket, interval=1):
    while True:
        test_event = {
            "event": "SERVICE-DATA",
            "client-type": client_type,
            "client-name": name,
            "data": {"random number":random.randint(1, 100)}
        }
        print(test_event)
        await websocket.send(json.dumps(test_event))
        await asyncio.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hardware client for Terrace")
    parser.add_argument("host", metavar="host", type=str, help="Enter the host URL")
    parser.add_argument(
        "name", metavar="name", type=str, help="Enter the name of this hardware client"
    )
    args = parser.parse_args()

    host = args.host
    name = args.name
    print(host, name)
    asyncio.run(client(host, name))
