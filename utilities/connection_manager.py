from fastapi import WebSocket
from typing import List, Dict


class Manager:
	def __init__(self):
		self.connections: List[Dict[str, WebSocket | id: str]] = []
		self.websocket_type_list = []

	async def connect(self, web_socket: WebSocket) -> None:
		await web_socket.accept()
		self.connections.append({"ws_object": web_socket, "id": web_socket.headers['sec-websocket-key']})

	async def disconnect_websocket(self, web_socket: WebSocket) -> str:
		for item in self.connections:
			if item['ws_object'] == web_socket:
				self.connections.remove(item)
				return item['id']
