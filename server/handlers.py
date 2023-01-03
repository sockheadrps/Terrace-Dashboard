hardware_client_set = set()
service_client_set = set()

hw_clients = {}

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
        self.ws_object = ws_object

    async def __call__(self, data, sender):
        await self.funcs[data["event"]](self, data, sender)

    @new_event(funcs, "CONNECT")
    async def connect(self, data, sender):
        pass

    @new_event(funcs, "DISCONNECT")
    async def disconnect(self, data, sender):
        pass

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
        await self.ws_object.send_json(data)
        # if self.hardware is sender:
        #     await self.ws_object.send_json(data)

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
        self.client_name = data['client-name']
        hardware_client_set.add(self.client_name)
        hw_clients[self.client_name] = ws_object

    @new_event(funcs, "HARDWARE-REQUEST")
    async def hardware_request(self, data, sender):
        sender.hardware = self
        await self.ws_object.send_json(data)

    @new_event(funcs, "HARDWARE-TERMINATE")
    async def terminate_request(self, data, sender):
        print('HARDWARE-TERMINATE', data, sender)
        # print(hw_clients[data['requested-client']])
        # await hw_clients[data['requested-client']].send_json({'event': 'HARDWARE-TERMINATE'})
        sender.hardware = None
        await self.ws_object.send_json(data)

    @new_event(funcs, 'HARDWARE-SERVICES')
    async def connected_hardware(self, data, sender):
        await self.ws_object.send_json(data)


class ServiceHandler(ClientHandler):
    funcs = ClientHandler.funcs.copy()

    def __init__(self, data, ws_object):
        super().__init__(data, ws_object)
        self.client_name = data['client-name']
        service_client_set.add(self.client_name)


async def broadcast(clients, data, sender):
    for client_list in clients.values():
        for client in client_list:
            await client(data, sender)
