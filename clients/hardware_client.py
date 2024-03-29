from stats import Computer
import websockets
from websockets.exceptions import ConnectionClosed
import asyncio
import json
import argparse


async def client(name, websocket):
    client_type = "HARDWARE"
    stream_task = None
    clients = 0

    # Initial connection
    connect_event = {
        "event": "CONNECT",
        "client-type": client_type,
        "client-name": name,
    }
    await websocket.send(json.dumps(connect_event))

    while True:
        data = json.loads(await websocket.recv())
        match data["event"]:
            case "HARDWARE-REQUEST":
                clients += 1
                if stream_task is None:
                    stream_task = asyncio.create_task(client_stream(websocket))
            case "HARDWARE-TERMINATE":
                if 0 < clients:
                    clients -= 1
                    if clients == 0:
                        stream_task.cancel()
                        stream_task = None


async def client_stream(websocket, interval=1):
    while True:
        data_stream = {
            "event": "HARDWARE-DATA",
            "client": name,
            "data": Computer.get_stats_dict(),
        }
        await websocket.send(json.dumps(data_stream))
        await asyncio.sleep(interval)


async def main(host, name):
    async with websockets.connect(f"ws://{host}:8081/ws/stats") as websocket:
        await client(name, websocket)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hardware client for Terrace")
    parser.add_argument(
        "host",
        nargs="?",
        metavar="host",
        const="127.0.0.1",
        type=str,
        help="Enter the host URL",
        default="127.0.0.1",
    )
    parser.add_argument(
        "name", metavar="name", type=str, help="Enter the name of this hardware client"
    )
    args = parser.parse_args()

    host = args.host
    name = args.name

    asyncio.run(main(host, name))
