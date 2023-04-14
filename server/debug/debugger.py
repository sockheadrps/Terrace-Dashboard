import websockets
from websockets.exceptions import ConnectionClosedError
import asyncio
import json
import argparse
from rich import print_json, print
from datetime import datetime


"""

"""

client_type = "DEBUGGER"


async def client(host):
    try:
        async with websockets.connect(f"ws://{host}:8081/ws/stats") as websocket:
            # Initial connection
            connect_event = {
                "event": "CONNECT",
                "client-type": client_type,
                "client-name": "Debugger",
            }
            await websocket.send(json.dumps(connect_event))
            while True:
                try:
                    data = json.loads(await websocket.recv())
                    if data:
                        # SERVER EVENTS
                        match data["event"]:
                            case "DEBUG":
                                print(f'[italic red]{datetime.now().strftime("%H:%M:%S.%f")}[/italic red]')
                                if data.get('clients'):
                                    for c_type in json.loads(data.get('clients')):
                                        if data.get('data'):
                                            print(f"[bold yellow]{c_type}: {json.loads(data['clients'])[c_type]}[/bold yellow]")
                                print_json(json.dumps(data['data']))
                                print(f"{'-'*40}")
                        data = None

                except ConnectionClosedError:
                    print("The server has shut down!")
                    break

    except ConnectionRefusedError:
        print("Server is either offline, or connection point is wrong!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hardware client for Terrace")
    parser.add_argument("host", metavar="host", type=str, help="Enter the host URL")
    args = parser.parse_args()
    host = args.host
    asyncio.run(client(host))
