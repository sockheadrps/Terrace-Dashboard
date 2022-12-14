import json

hardware_client_set = set()


def new_event(funcs, ev):
	def func(cb):
		funcs[ev] = cb
		return cb

	return func


class ClientHandler(object):
	funcs = {}
	hw_client_set = []

	def __init__(self, data, ws_object):
		self.client_type = data['client-type']
		self.ws_object = ws_object
		print("init ", data)

	async def __call__(self, data, sender):
		await self.funcs[data["event"]](self, data, sender)

	@new_event(funcs, "CONNECT")
	async def connect(self, sender):
		print('aa')
		await self.ws_object.send({"event": "CONNECTED"})

	@new_event(funcs, "DISCONNECT")
	async def disconnect(self, sender):
		await self.ws_object.send({"event": "DISCONNECT"})

	@new_event(funcs, "HARDWARE-REQUEST")
	async def hardware_request(self, data, sender):
		pass

	@new_event(funcs, "HARDWARE-TERMINATE")
	async def terminate_request(self, data, sender):
		pass

	@new_event(funcs, "HARDWARE-DATA")
	async def hardware_data_recv(self, data, sender):
		pass

	@new_event(funcs, 'HARDWARE-SERVICES')
	async def connected_hardware(self, data, sender):
		pass

	@new_event(funcs, 'HARDWARE-CONNECT')
	async def hardware_connect(self, data, sender):
		pass

	@new_event(funcs, 'HARDWARE-DISCONNECT')
	async def hardware_disconnect(self, data, sender):
		pass

	@new_event(funcs, 'SERVICE-CONNECT')
	async def hardware_connect(self, data, sender):
		pass

	@new_event(funcs, 'SERVICE-DISCONNECT')
	async def hardware_disconnect(self, data, sender):
		pass

class DashboardHandler(ClientHandler):
	funcs = ClientHandler.funcs.copy()

	def __init__(self, data, ws_object, current_hw=None):
		super().__init__(data, ws_object)
		self.current_hw = current_hw

	@new_event(funcs, "CONNECT")
	async def connect(self, sender):
		await self.ws_object.send_json({"event": "CONNECTED", "hardware-list": [*hardware_client_set]})

	@new_event(funcs, "HARDWARE-DATA")
	async def hardware_data_recv(self, data, sender):
		await self.ws_object.send_json(data)

	@new_event(funcs, "HARDWARE-CONNECT")
	async def hardware_connect(self, data, sender):
		print('hw connect in db')
		await self.ws_object.send_json(data)

	@new_event(funcs, "HARDWARE-DISCONNECT")
	async def hardware_disconnect(self, data, sender):
		print('hw disconnect')
		await self.ws_object.send_json(data)


class HardwareHandler(ClientHandler):
	funcs = ClientHandler.funcs.copy()

	def __init__(self, data, ws_object):
		super().__init__(data, ws_object)
		self.client_name = data['client-name']
		hardware_client_set.add(self.client_name)

	@new_event(funcs, "HARDWARE-REQUEST")
	async def hardware_request(self, data, sender):
		print('hardware requedst')
		await self.ws_object.send_json(data)

	@new_event(funcs, "HARDWARE-TERMINATE")
	async def terminate_request(self, data, sender):
		await self.ws_object.send_json(data)

	@new_event(funcs, 'HARDWARE-SERVICES')
	async def connected_hardware(self, data, sender):
		await self.ws_object.send_json(data)


class ServiceHandler(ClientHandler):
	funcs = ClientHandler.funcs.copy()

	def __init__(self, data, ws_object):
		super().__init__(data, ws_object)
		self.client_name = data['client-name']

	@new_event(funcs, "SERVICE-CONNECT")
	async def hardware_request(self, data, sender):
		print('SERVICE connect')
		await self.ws_object.send_json(data)

	@new_event(funcs, "SERVICE-DISCONNECT")
	async def terminate_request(self, data, sender):
		await self.ws_object.send_json(data)


async def broadcast(clients, data, sender):
	for client in clients:
		await client(data, sender)
