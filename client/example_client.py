import websockets
import asyncio



async def client():
	async with websockets.connect("ws://localhost:8080/ws/stats") as websocket:
		try:
			await websocket.send('{"event": "CONNECT", "client": "Twitch Bot"}')
			while True:
				data = await websocket.recv()
				print(data)

		except Exception as e:
			print("Host unavailable!")
		finally:
			await websocket.send('{"event":  "TWITCH_CLOSE"}')

asyncio.get_event_loop().run_until_complete(client())