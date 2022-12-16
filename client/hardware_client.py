from utilities.stats import Computer
import websockets
import asyncio
import json
from asyncio.exceptions import TimeoutError

client_name = "Server-Hardware"


async def client():
	data = None
	data_stream_requested = False
	async with websockets.connect("ws://localhost:80/ws/stats") as websocket:
		try:
			# Initial connection
			connect_event = {"event": "CONNECT", "client-type": "HARDWARE", "client-name": client_name}
			await websocket.send(json.dumps(connect_event))
			while True:
				try:
					data = json.loads(await asyncio.wait_for(websocket.recv(), timeout=1))
				except TimeoutError:
					pass

				if data:
					match data['event']:
						case "CONNECT":
							print("Connected!")
							to_send = {"event": "HARDWARE-CONNECT",
									   "client-name": client_name}
							await websocket.send(json.dumps(to_send))
							data = None
						case "HARDWARE-REQUEST":
							data_stream_requested = True
						case "HARDWARE-TERMINATE":
							data_stream_requested = False

				if data_stream_requested:
					to_send = {"event": "HARDWARE-DATA",
							   "client": client_name,
							   "data": Computer.get_stats_dict()}
					await websocket.send(json.dumps(to_send))
		finally:
			print("finally")
			to_send = {"event": "HARDWARE-DISCONNECT", "client-name": client_name}
			await websocket.send(json.dumps(to_send))

asyncio.run(client())
