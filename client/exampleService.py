import websockets
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
import asyncio
import json

client_name = "Example-Service"


async def client():
	data = None
	try:
		async with websockets.connect("ws://localhost:80/ws/stats") as websocket:
			# Initial connection
			connect_event = {"event": "CONNECT", "client-type": "SERVICE", "client-name": client_name}
			await websocket.send(json.dumps(connect_event))
			while True:
				try:
					data = json.loads(await websocket.recv())
					if data:
						print(data)
						match data['event']:
							case "CONNECT":
								print("Connected!")
								to_send = {"event": "SERVICE-CONNECT",
										   "client-name": client_name}
								await websocket.send(json.dumps(to_send))
						data = None

				except ConnectionClosedError:
					print("The server has refused connection. Is the server running?")

	except ConnectionRefusedError:
		print("Server is either offline, or connection point is wrong!")
	finally:
		# Send disconnect message if service closes and there is a websocket connection
		try:
			to_send = {"event": "SERVICE-DISCONNECT", "client-name": client_name}
			await websocket.send(json.dumps(to_send))
		except ConnectionClosedOK:
			print("Client successfully closed")


asyncio.run(client())
