from utilities.stats import Computer
import websockets
import asyncio
import json
from asyncio.exceptions import TimeoutError

client_name = "Example-Service"


async def client():
	data = None
	async with websockets.connect("ws://localhost:8080/ws/stats") as websocket:
		try:
			# Initial connection
			connect_event = {"event": "CONNECT", "client-type": "SERVICE", "client-name": client_name}
			await websocket.send(json.dumps(connect_event))
			while True:
				try:
					data = json.loads(await websocket.recv())
				except Exception as e:
					raise e
				if data:
					print(data)
					match data['event']:
						case "CONNECT":
							print("Connected!")
							to_send = {"event": "SERVICE-CONNECT",
									   "client-name": client_name}
							await websocket.send(json.dumps(to_send))
							data = None

		finally:
			to_send = {"event": "SERVICE-DISCONNECT", "client-name": client_name}
			await websocket.send(json.dumps(to_send))

asyncio.get_event_loop().run_until_complete(client())
