from utilities.stats import Computer
import websockets
import asyncio
import json
from asyncio.exceptions import TimeoutError

client_name = "Server-Hardware"
client_type = "HARDWARE"


async def client():
	data = None
	data_stream_requested = False
	async with websockets.connect("ws://localhost:80/ws/stats") as websocket:
		try:
			# Initial connection
			connect_event = {"event": "CONNECT", "client-type": client_type, "client-name": client_name}
			await websocket.send(json.dumps(connect_event))

			while True:
				try:
					data = json.loads(await asyncio.wait_for(websocket.recv(), timeout=1))
				except TimeoutError:
					pass

				if data:
					match data['event']:
						case "HARDWARE-REQUEST":
							data_stream_requested = True
						case "HARDWARE-TERMINATE":
							data_stream_requested = False
					data = None

				if data_stream_requested:
					data_stream = {"event": "HARDWARE-DATA",
							   "client": client_name,
							   "data": Computer.get_stats_dict()}
					await websocket.send(json.dumps(data_stream))
		finally:
			print("finally")
			disconnect_event = {"event": "DISCONNECT", "client-type": client_type, "client-name": client_name}
			await websocket.send(json.dumps(disconnect_event))

asyncio.run(client())
