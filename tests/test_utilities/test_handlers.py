import pytest
from utilities.handlers import new_event, ClientHandler, HardwareHandler, ServiceHandler, DashboardHandler, \
    hardware_client_set, service_client_set, broadcast
from typing import Callable
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket


app = FastAPI()
client = TestClient(app)


@pytest.fixture
def functions_dict():
    functions = {}
    return functions


def test_new_event(functions_dict):
    """
    Assertion 1: Tests that a callable is created in the functions_dict at specified key
    Assertion 2: Tests that the correct callback function is inserted at the specified key
    :param functions_dict: Pytest fixture
    :empty_callback_function() simulates a callback function
    """
    def empty_callback_function():
        pass
    assert isinstance(new_event(functions_dict, "CONNECT"), Callable)
    new_event(functions_dict, "CONNECT")(empty_callback_function)
    assert functions_dict['CONNECT'] == empty_callback_function


#  ----- TESTS FOR BASE CLASS -----
def test_client_handler():
    """
    Tests the init function of the base class
    Assertion 1: Verifies the initial event is CONNECT
    Assertion 2: Verifies server response for "client-type" is the correct class client type
    Assertion 3: Verifies the class ws_object is of type WebSocket
    """
    @app.websocket_route("/test_connect")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        assert data['event'] == 'CONNECT'
        client_handler = ClientHandler(data, websocket)
        assert client_handler.client_type == data['client-type']
        assert isinstance(client_handler.ws_object, WebSocket)
        await websocket.close()

    with client.websocket_connect("/test_connect") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "test"})


# ----- TESTS FOR DASHBOARDHANDLER SUBCLASS -----
def test_dashboard_handler_connect_dashboard():
    """
    Assertion 1: Simulates a DashboardHandler serverside CONNECT event for clients that are Dashboards
    Assertion 2: Simulates a dashboard client and verifies a CONNECT event
    Assertion 3: Simulates a dashboard client and verifies the CONNECT event returns a 'hardware-list'
    Assertion 4: Simulates a dashboard client and verifies the CONNECT event returns a 'service-list'

    Server connect event for dashboard handlers will respond with:
    {"event": "CONNECT", "hardware-list": [*hardware_client_set], "service-list": [*service_client_set]}
    """
    @app.websocket_route("/test_connect_dashboard")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        assert data['event'] == 'CONNECT'
        dashboard_handler = DashboardHandler(data, websocket)
        await dashboard_handler(data, dashboard_handler)
        await websocket.close()

    with client.websocket_connect("/test_connect_dashboard") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "DASHBOARD"})
        data = websocket.receive_json()
        assert data['event'] == 'CONNECT'
        assert isinstance(data['hardware-list'], list)
        assert isinstance(data['service-list'], list)


def test_dashboard_handler_connect_hardware():
    """
    Assertion 1: Simulates a DashboardHandler serverside CONNECT event for clients that are Hardware
    Assertion 2: Simulates a hardware client and verifies a CONNECT event
    Assertion 3: Simulates a hardware client and verifies the CONNECT event returns the correct client-type
    Assertion 4: Simulates a hardware client and verifies the CONNECT event returns the correct client-name

    Server connect event for non dashboard clients will respond with:
    {"event": "CONNECT", "client-type": data['client-type'], "client-name": data["client-name"]}
    """
    @app.websocket_route("/test_connect_hardware")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        assert data['event'] == 'CONNECT'
        dashboard_handler = DashboardHandler(data, websocket)
        await dashboard_handler(data, dashboard_handler)
        await websocket.close()

    with client.websocket_connect("/test_connect_hardware") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "HARDWARE", "client-name": "test"})
        data = websocket.receive_json()
        assert data['event'] == 'CONNECT'
        assert data['client-type'] == 'HARDWARE'
        assert data['client-name'] == 'test'


def test_dashboard_handler_disconnect_hardware():
    """
    Assertion 1: Simulates and verifies the serverside DISCONNECT event for hardware
    Assertion 2: Simulates and verifies the hardware client DISCONNECT event

    Disconnect event returns:
    {"event": "DISCONNECT", "client-type": data['client-type'], "client-name": data["client-name"]}
    """

    @app.websocket_route("/test_disconnect_hardware")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        dashboard_handler = DashboardHandler(data, websocket)
        await dashboard_handler(data, dashboard_handler)
        data = await websocket.receive_json()
        assert data['event'] == "DISCONNECT"
        await dashboard_handler(data, dashboard_handler)
        await websocket.close()

    with client.websocket_connect("/test_disconnect_hardware") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "HARDWARE", "client-name": "test"})
        # Data is not necessary here, just need to capture the connect event before asserting the disconnect
        data = websocket.receive_json()
        websocket.send_json({"event": "DISCONNECT", "client-type": "HARDWARE", "client-name": "test"})
        data = websocket.receive_json()
        assert data['event'] == "DISCONNECT"


def test_dashboard_handler_connect_service():
    """
    Assertion 1: Simulates a DashboardHandler serverside CONNECT event for clients that are Services
    Assertion 2: Simulates a service client and verifies a CONNECT event
    Assertion 3: Simulates a service client and verifies the CONNECT event returns the correct client-type
    Assertion 4: Simulates a service client and verifies the CONNECT event returns the correct client-name

    Server connect event for non dashboard clients will respond with:
    {"event": "CONNECT", "client-type": data['client-type'], "client-name": data["client-name"]}
    """
    @app.websocket_route("/test_connect_hardware")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        assert data['event'] == 'CONNECT'
        dashboard_handler = DashboardHandler(data, websocket)
        await dashboard_handler(data, dashboard_handler)
        await websocket.close()

    with client.websocket_connect("/test_connect_hardware") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "SERVICE", "client-name": "test"})
        data = websocket.receive_json()
        assert data['event'] == 'CONNECT'
        assert data['client-type'] == 'SERVICE'
        assert data['client-name'] == 'test'


def test_dashboard_handler_disconnect_service():
    """
    Assertion 1: Simulates and verifies the serverside DISCONNECT event for services
    Assertion 2: Simulates and verifies the service client DISCONNECT event

    Disconnect event returns:
    {"event": "DISCONNECT", "client-type": data['client-type'], "client-name": data["client-name"]}
    """
    @app.websocket_route("/test_disconnect_service")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        dashboard_handler = DashboardHandler(data, websocket)
        await dashboard_handler(data, dashboard_handler)
        data = await websocket.receive_json()
        assert data['event'] == "DISCONNECT"
        await dashboard_handler(data, dashboard_handler)
        await websocket.close()

    with client.websocket_connect("/test_disconnect_hardware") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "SERVICE", "client-name": "test"})
        # Data is not necessary here, just need to capture the connect event before asserting the disconnect
        data = websocket.receive_json()
        websocket.send_json({"event": "DISCONNECT", "client-type": "SERVICE", "client-name": "test"})
        data = websocket.receive_json()
        assert data['event'] == "DISCONNECT"


def test_dashboard_handler_hardware_data_recv():
    """
    Tests data "stream" from a hardware client
    Assertion 1: Simulates and verifies the serverside "HARDWARE-DATA" event
    Assertion 2: Verifies the data is the correct format (dict)

    The hardware client 'HARDWARE-DATA' event will respond at 1 second intervals with:
    {"event": "HARDWARE-DATA", "client": client_name, "data": Computer.get_stats_dict()}
    """
    @app.websocket_route("/test_hardware_data_recv")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        dashboard_handler = DashboardHandler(data, websocket)
        data = await websocket.receive_json()
        assert data['event'] == "HARDWARE-DATA"
        await dashboard_handler(data, dashboard_handler)
        await websocket.close()

    with client.websocket_connect("/test_hardware_data_recv") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "DASHBOARD"})
        websocket.send_json({"event": "HARDWARE-DATA"})
        data = websocket.receive_json()
        assert isinstance(data, dict)


# ----- TESTS FOR HARDWAREHANDLER SUBCLASS -----
def test_hardwarehandler_init():
    """
    Tests __init__ of HardwareHandler subclass
    Assertion 1: Simulates and verifies that client_name instance property is properly set
    Assertion 2: Simulates and verifies the client_name is added to the hardware_client_set
    """
    @app.websocket_route("/test_hardwarehandler_init")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        hardware_handler = HardwareHandler(data, websocket)
        assert hardware_handler.client_name == data['client-name']
        assert hardware_handler.client_name in hardware_client_set
        await websocket.close()

    with client.websocket_connect("/test_hardwarehandler_init") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "HARDWARE", 'client-name': 'test-hardware'})


def test_hardwarehandler_hardware_request():
    """
    Tests the HARDWARE-REQUEST event sent by a dashboard client
    Assertion 1: Simulates and verifies the serverside HARDWARE-REQUEST event
    Assertion 2: Verifies the 'requested-client' is the client name of the hardware handler

    The event from JS:
    socket.send(JSON.stringify({event: "HARDWARE-REQUEST", "requested-client": i }));
    """
    @app.websocket_route("/test_hardware_request")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        hardware_handler = HardwareHandler(data, websocket)
        data = await websocket.receive_json()
        assert data['event'] == "HARDWARE-REQUEST"
        assert data['requested-client'] == hardware_handler.client_name
        await websocket.close()

    with client.websocket_connect("/test_hardware_request") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "HARDWARE", 'client-name': 'test-hardware'})
        websocket.send_json({"event": "HARDWARE-REQUEST", "requested-client": "test-hardware"})


def test_hardwarehandler_terminate_request():
    """
    Tests the HARDWARE-TERMINATE event sent by a dashboard client
    Assertion 1: Simulates and verifies the serverside HARDWARE-TERMINATE event
    Assertion 2: Verifies the 'requested-client' is the client name of the hardware handler

    The event from JS:
    JS - > socket.send(JSON.stringify({event: "HARDWARE-TERMINATE", "requested-client": currentHardware }));
    """
    @app.websocket_route("/test_terminate_request")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        hardware_handler = HardwareHandler(data, websocket)
        data = await websocket.receive_json()
        assert data['event'] == "HARDWARE-TERMINATE"
        assert data['requested-client'] == hardware_handler.client_name
        await websocket.close()

    with client.websocket_connect("/test_terminate_request") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "HARDWARE", 'client-name': 'test-hardware'})
        websocket.send_json({"event": "HARDWARE-TERMINATE", "requested-client": "test-hardware"})


def test_hardwarehandler_connected_hardware():
    """
    Tests hardware_request of HardwareHandler class
    Assertion 1: Simulates and verifies the HARDWARE-SERVICES event
    Assertion 2: Verifies 'requested-client' is the hardwarehandler class name

    The event from js:
    socket.send(JSON.stringify({event: "HARDWARE-REQUEST", "requested-client": i }));
    """
    @app.websocket_route("/test_connected_hardware")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        hardware_handler = HardwareHandler(data, websocket)
        data = await websocket.receive_json()
        assert data['event'] == "HARDWARE-SERVICES"
        assert data['requested-client'] == hardware_handler.client_name
        await websocket.close()

    with client.websocket_connect("/test_connected_hardware") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "HARDWARE", 'client-name': 'test-hardware'})
        websocket.send_json({"event": "HARDWARE-SERVICES", "requested-client": "test-hardware"})
        websocket.close()


# ----- TESTS FOR SERVICEHANDLER SUBCLASS -----
def test_servicehandler_init():
    """
    Tests the ServiceHandler __init__
    Assertion 1: Simulates and verifies the service handler gets created with the correct client type
    Assertion 2: Verifies the service name gets added to the service_client_set

    The service client connect event:
    {"event": "CONNECT", "client-type": client_type, "client-name": client_name}
    """
    @app.websocket_route("/test_servicehandler_init")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        service_handler = ServiceHandler(data, websocket)
        assert data['client-type'] == service_handler.client_type
        assert service_handler.client_name in service_client_set
        await websocket.close()

    with client.websocket_connect("/test_servicehandler_init") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "SERVICE", 'client-name': 'test-service'})


# ----- TEST FOR BROADCAST -----
def test_broadcast():
    """
    Assertion 1: Verifies broadcast communicates the correct data type (dict
    :return:
    """
    clients = {"DASHBOARD": [], "HARDWARE": [], "SERVICE": []}
    client_types = {"DASHBOARD": DashboardHandler, "HARDWARE": HardwareHandler, "SERVICE": ServiceHandler}

    @app.websocket_route("/test_broadcast")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        client = client_types[data["client-type"]](data, websocket)
        clients[data['client-type']].append(client)
        await broadcast(clients, data, client)
        await websocket.close()

    with client.websocket_connect("/test_broadcast") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "DASHBOARD"})
        data = websocket.receive_json()
        assert isinstance(data, dict)
