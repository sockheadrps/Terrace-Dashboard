from main import app, clients
from httpx import AsyncClient
from fastapi.testclient import TestClient
import pytest
from time import sleep


client = TestClient(app)


@pytest.mark.anyio
async def test_dashboard_endpoint():
    """
    Assertion 1: Tests the successful delivery of the /dashboard http endpoint
    """
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get("/dashboard")
        assert response.status_code == 200


def test_websocket_endpoint_dashboard():
    """
    Assertion 1: On CONNECT dashboard gets added to clients['DASHBOARD'] list
    Assertion 2: on DISCONNECT dashboard gets removed from clients['DASHBOARD'] list
    """
    with client.websocket_connect("ws://localhost/ws/stats") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": 'DASHBOARD'})
        # Sleep necessary to allow time for the server to update the client list
        sleep(.01)
        assert len(clients['DASHBOARD']) > 0
    assert len(clients['DASHBOARD']) == 0


def test_websocket_endpoint_hardware():
    """
    Assertion 1: On CONNECT hardware gets added to clients['HARDWARE'] list
    Assertion 2: on DISCONNECT hardware gets removed from clients['HARDWARE'] list
    """
    with client.websocket_connect("ws://localhost/ws/stats") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": 'HARDWARE', "client-name": "test"})
        # Sleep necessary to allow time for the server to update the client list
        sleep(.01)
        assert len(clients['HARDWARE']) > 0
    assert len(clients['HARDWARE']) == 0


def test_websocket_endpoint_services():
    """
    Assertion 1: On CONNECT service gets added to clients['SERVICE'] list
    Assertion 2: on DISCONNECT Service gets removed from clients['SERVICE'] list
    """
    with client.websocket_connect("ws://localhost/ws/stats") as websocket:
        websocket.send_json({"event": "CONNECT", "client-type": 'SERVICE', "client-name": "test"})
        # Sleep necessary to allow time for the server to update the client list
        sleep(.01)
        assert len(clients['SERVICE']) > 0
    assert len(clients['SERVICE']) == 0
