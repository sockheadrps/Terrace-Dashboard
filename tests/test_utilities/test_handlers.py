import pytest
from utilities.handlers import new_event, ClientHandler, HardwareHandler, ServiceHandler, DashboardHandler, \
    hardware_client_set, service_client_set, broadcast
from typing import Callable
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket


app = FastAPI()


@pytest.fixture
def functions_dict():
    functions = {}
    return functions


def test_new_event(functions_dict):
    def empty_callback_function():
        pass
    # Tests that a callable is created in the functions_dict at specified key
    assert isinstance(new_event(functions_dict, "CONNECT"), Callable)
    # Tests that the correct callback function is inserted at the specified key
    new_event(functions_dict, "CONNECT")(empty_callback_function)
    assert functions_dict['CONNECT'] == empty_callback_function


#  ----- TESTS FOR BASE CLASS -----
def test_client_handler():
    # Tests the init function of the base class, since the subsequent methods will be tested in child classes
    @app.websocket_route("/test_connect")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        assert data['event'] == 'CONNECT'
        client_handler = ClientHandler(data, websocket)
        assert client_handler.client_type == data['client-type']
        assert isinstance(client_handler.ws_object, WebSocket)
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/test_connect") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "test"})


# ----- TESTS FOR DASHBOARDHANDLER SUBCLASS -----
def test_dashboard_handler_connect_dashboard():
    # Connect event returns:
    # {"event": "CONNECT", "hardware-list": [*hardware_client_set], "service-list": [*service_client_set]}
    @app.websocket_route("/test_connect_dashboard")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        assert data['event'] == 'CONNECT'
        dashboard_handler = DashboardHandler(data, websocket)
        assert dashboard_handler.client_type == data['client-type']
        assert isinstance(dashboard_handler.ws_object, WebSocket)
        await dashboard_handler(data, dashboard_handler)
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/test_connect_dashboard") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "DASHBOARD"})
        data = websocket.receive_json()
        assert data['event'] == 'CONNECT'
        assert isinstance(data['hardware-list'], list)
        assert isinstance(data['service-list'], list)


def test_dashboard_handler_connect_non_dashboard():
    # Connect event returns:
    # {"event": "CONNECT", "client-type": data['client-type'], "client-name": data["client-name"]}
    @app.websocket_route("/test_connect_non_dashboard")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        assert data['event'] == 'CONNECT'
        dashboard_handler = DashboardHandler(data, websocket)
        await dashboard_handler(data, dashboard_handler)
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/test_connect_non_dashboard") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "HARDWARE", "client-name": "hardware"})
        data = websocket.receive_json()
        assert data['event'] == 'CONNECT'
        assert data['client-type'] == 'HARDWARE'
        assert data['client-name'] == 'hardware'


def test_dashboard_handler_hardware_data_recv():
    # Tests the request for hardware stats by the dashboard
    @app.websocket_route("/test_hardware_data_recv")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        dashboard_handler = DashboardHandler(data, websocket)
        data = await websocket.receive_json()
        assert data['event'] == "HARDWARE-DATA"
        await dashboard_handler(data, dashboard_handler)
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/test_hardware_data_recv") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "DASHBOARD"})
        websocket.send_json({"event": "HARDWARE-DATA"})
        data = websocket.receive_json()
        assert isinstance(data, dict)


def test_dashboard_handler_disconnect_non_dashboard():
    # Disconnect event returns:
    # {"event": "DISCONNECT", "client-type": data['client-type'], "client-name": data["client-name"]}
    @app.websocket_route("/test_disconnect_non_dashboard")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        dashboard_handler = DashboardHandler(data, websocket)
        await dashboard_handler(data, dashboard_handler)
        data = await websocket.receive_json()
        assert data['event'] == "DISCONNECT"
        await dashboard_handler(data, dashboard_handler)
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/test_disconnect_non_dashboard") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "HARDWARE", "client-name": "hardware"})
        # Dont need data here, just need to capture the return
        data = websocket.receive_json()
        websocket.send_json({"event": "DISCONNECT", "client-type": "HARDWARE", "client-name": "hardware"})
        data = websocket.receive_json()
        assert data['event'] == "DISCONNECT"


# ----- TESTS FOR HARDWAREHANDLER SUBCLASS -----
def test_hardwarehandler_init():
    # Tests __init__ of HardwareHandler class
    @app.websocket_route("/test_hardwarehandler_init")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        hardware_handler = HardwareHandler(data, websocket)
        assert data['event'] == 'CONNECT'
        assert hardware_handler.client_name == data['client-name']
        assert hardware_handler.client_name in hardware_client_set
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/test_hardwarehandler_init") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "HARDWARE", 'client-name': 'test-hardware'})


def test_hardwarehandler_hardware_request():
    # Tests hardware_request of HardwareHandler class
    # returns {data} json
    # JS - > socket.send(JSON.stringify({event: "HARDWARE-REQUEST", "requested-client": i }));
    @app.websocket_route("/test_hardware_request")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        hardware_handler = HardwareHandler(data, websocket)
        data = await websocket.receive_json()
        assert data['event'] == "HARDWARE-REQUEST"
        assert data['requested-client'] == hardware_handler.client_name
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/test_hardware_request") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "HARDWARE", 'client-name': 'test-hardware'})
        websocket.send_json({"event": "HARDWARE-REQUEST", "requested-client": "test-hardware"})


def test_hardwarehandler_terminate_request():
    # Tests terminate_request of HardwareHandler class
    # returns {data} json
    # JS - > socket.send(JSON.stringify({event: "HARDWARE-TERMINATE", "requested-client": currentHardware }));
    @app.websocket_route("/test_terminate_request")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        hardware_handler = HardwareHandler(data, websocket)
        data = await websocket.receive_json()
        assert data['event'] == "HARDWARE-TERMINATE"
        assert data['requested-client'] == hardware_handler.client_name
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/test_terminate_request") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "HARDWARE", 'client-name': 'test-hardware'})
        websocket.send_json({"event": "HARDWARE-TERMINATE", "requested-client": "test-hardware"})


def test_hardwarehandler_connected_hardware():
    # Tests hardware_request of HardwareHandler class
    # returns {data} json
    # JS - > socket.send(JSON.stringify({event: "HARDWARE-REQUEST", "requested-client": i }));
    @app.websocket_route("/test_connected_hardware")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        hardware_handler = HardwareHandler(data, websocket)
        data = await websocket.receive_json()
        assert data['event'] == "HARDWARE-SERVICES"
        assert data['requested-client'] == hardware_handler.client_name
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/test_connected_hardware") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "HARDWARE", 'client-name': 'test-hardware'})
        websocket.send_json({"event": "HARDWARE-SERVICES", "requested-client": "test-hardware"})
        websocket.close()


# ----- TESTS FOR SERVICEHANDLER SUBCLASS -----
def test_servicehandler_init():
    # Tests init of ServiceHandler class
    # Python - > connect_event = {"event": "CONNECT", "client-type": client_type, "client-name": client_name}
    @app.websocket_route("/test_servicehandler_init")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        service_handler = ServiceHandler(data, websocket)
        assert data['event'] == "CONNECT"
        assert data['client-type'] == service_handler.client_type
        assert service_handler.client_name in service_client_set
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/test_servicehandler_init") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "SERVICE", 'client-name': 'test-service'})


# ----- TEST FOR BROADCAST -----
def test_broadcast():
    # Connect event returns:
    clients = {"DASHBOARD": [], "HARDWARE": [], "SERVICE": []}
    client_types = {"DASHBOARD": DashboardHandler, "HARDWARE": HardwareHandler, "SERVICE": ServiceHandler}

    @app.websocket_route("/test_broadcast")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        data = await websocket.receive_json()
        client = client_types[data["client-type"]](data, websocket)
        clients[data['client-type']].append(client)
        assert data['event'] == 'CONNECT'
        await broadcast(clients, data, client)
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/test_broadcast") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": "DASHBOARD"})
        data = websocket.receive_json()
        assert isinstance(data, dict)
