import asyncio
from itertools import chain


hardware_client_set = set()
service_client_set = set()
client_sets = {"HARDWARE": hardware_client_set, "SERVICE": service_client_set}


def new_event(functions: dict, event: str):
    """
    :param functions: A dictionary instantiated by the ClientHandler class that maps the event to a callback function
    :param event: A string used as a key in the functions dictionary
    :return: A function that returns the callback function
    """
    def func(callback):
        functions[event] = callback
        return callback

    return func


class ClientHandler(object):
    funcs = {}

    def __init__(self, data, ws_object):
        self.client_type = data['client-type']
        self.client_name = data.get('client-name')
        self.ws_object = ws_object

    async def __call__(self, data, sender):
        await self.funcs[data["event"]](self, data, sender)

    @new_event(funcs, "CONNECT")
    async def connect(self, data, sender):
        pass

    @new_event(funcs, "DISCONNECT")
    async def disconnect(self, data, sender):
        if sender is self and self.client_type in client_sets:
            client_sets[self.client_type].remove(self.client_name)

    @new_event(funcs, "HARDWARE-REQUEST")
    async def hardware_request(self, data, sender):
        pass

    @new_event(funcs, "HARDWARE-TERMINATE")
    async def terminate_request(self, data, sender):
        pass

    @new_event(funcs, "HARDWARE-DATA")
    async def hardware_data_recv(self, data, sender):
        pass


class DashboardHandler(ClientHandler):
    funcs = ClientHandler.funcs.copy()

    def __init__(self, data, ws_object):
        super().__init__(data, ws_object)
        self.client_name = "_"
        self.hardware = None

    @new_event(funcs, "CONNECT")
    async def connect(self, data, sender):
        if data.get("client-type") != "DASHBOARD":
            await self.ws_object.send_json({"event": "CONNECT", "client-type": data['client-type'],
                                            "client-name": data["client-name"]})
        elif sender is self:
            await self.ws_object.send_json({"event": "CONNECT", "hardware-list": [*hardware_client_set],
                                            "service-list": [*service_client_set]})

    @new_event(funcs, "HARDWARE-DATA")
    async def hardware_data_recv(self, data, sender):
        print(f"hdr {data['client']}")
        if self.hardware is sender:
            await self.ws_object.send_json(data)

    @new_event(funcs, "DISCONNECT")
    async def disconnect(self, data, sender):
        if data.get("client-type") != "DASHBOARD":
            await self.ws_object.send_json({"event": "DISCONNECT", "client-type": data['client-type'],
                                            "client-name": data["client-name"]})
        elif sender is self:
            print("dashboard disconnected")


class HardwareHandler(ClientHandler):
    funcs = ClientHandler.funcs.copy()

    def __init__(self, data, ws_object):
        super().__init__(data, ws_object)
        hardware_client_set.add(self.client_name)

    @new_event(funcs, "HARDWARE-REQUEST")
    async def hardware_request(self, data, sender):
        if sender.hardware is None and data["requested-client"] == self.client_name:
            sender.hardware = self
            await self.ws_object.send_json(data)

    @new_event(funcs, "HARDWARE-TERMINATE")
    async def terminate_request(self, data, sender):
        print('HARDWARE-TERMINATE', data, sender)
        if sender.hardware is self:
            sender.hardware = None
            await self.ws_object.send_json(data)

    @new_event(funcs, 'HARDWARE-SERVICES')
    async def connected_hardware(self, data, sender):
        await self.ws_object.send_json(data)


class ServiceHandler(ClientHandler):
    funcs = ClientHandler.funcs.copy()

    def __init__(self, data, ws_object):
        super().__init__(data, ws_object)
        service_client_set.add(self.client_name)


async def broadcast(clients, data, sender):
    coros = (client(data, sender) for client in clients.values())
    await asyncio.gather(*coros)

