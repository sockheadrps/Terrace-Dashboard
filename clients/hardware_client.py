from stats import Computer
import websockets
import asyncio
import json
import argparse


async def client(host, name):
    client_type = "HARDWARE"
    stream_task = None
    clients = 0
    async with websockets.connect(f"ws://{host}:8080/ws/stats") as websocket:
        try:
            # Initial connection
            connect_event = {"event": "CONNECT", "client-type": client_type, "client-name": name}
            await websocket.send(json.dumps(connect_event))

            while True:
                data = json.loads(await websocket.recv())
                if data['requested-client'] == name:
                    match data['event']:
                        case "HARDWARE-REQUEST":
                            print('Start stream....')
                            clients += 1
                            if stream_task is None:
                                stream_task = asyncio.create_task(client_stream(websocket))
                        case "HARDWARE-TERMINATE":
                            print('End Stream...')
                            if 0 < clients:
                                clients -= 1
                                if clients == 0:
                                    stream_task.cancel()
                                    stream_task = None

        finally:
            disconnect_event = {"event": "DISCONNECT", "client-type": client_type, "client-name": name}
            await websocket.send(json.dumps(disconnect_event))


async def client_stream(websocket, interval=1):
    while True:
        print('data stream')
        data_stream = {"event": "HARDWARE-DATA", "client": name, "data": Computer.get_stats_dict()}
        await websocket.send(json.dumps(data_stream))
        await asyncio.sleep(interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Hardware client for Terrace")
    parser.add_argument('host', metavar="host", type=str, help="Enter the host URL")
    parser.add_argument('name', metavar="name", type=str, help="Enter the name of this hardware client")
    args = parser.parse_args()

    host = args.host
    name = args.name

    asyncio.run(client(host, name))
