import websockets
from websockets.exceptions import ConnectionClosedError
import asyncio
import json
import argparse
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
import pydirectinput

def liveScreen():
    pydirectinput.keyDown('ctrl')
    pydirectinput.keyDown('alt')
    pydirectinput.keyDown('1')
    pydirectinput.keyUp('ctrl')
    pydirectinput.keyUp('alt')
    pydirectinput.keyUp('1')


def brbScreen():
    pydirectinput.keyDown('ctrl')
    pydirectinput.keyDown('alt')
    pydirectinput.keyDown('2')
    pydirectinput.keyUp('ctrl')
    pydirectinput.keyUp('alt')
    pydirectinput.keyUp('2')


client_type = "SERVICE"



def detect_media():
    media = {}
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name():
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            # Get names of programs we can access volume to, store volume value
            media[session.Process.name()[:-4]] = volume.GetMasterVolume()

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface,
                  POINTER(IAudioEndpointVolume))
    # Access and store master volume level
    try:
        media['master'] = volume.GetMasterVolumeLevelScalar()
    except Exception as e:
        print(e, "Error accessing master")
    return media


def set_volume(media, target, new_volume):
    if target in media.keys():
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(
                ISimpleAudioVolume)
            if session.Process and session.Process.name() == target + ".exe":
                volume.SetMasterVolume(new_volume, None)
        if target == "master":
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface,
                          POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(new_volume, None)



async def client(host):
    stream_task = None
    try:
        async with websockets.connect(f"ws://{host}:8081/ws/stats") as websocket:
            # Initial connection
            connect_event = {
                "event": "CONNECT",
                "client-type": client_type,
                "client-name": "Controller",
            }
            # Sending initial data
            await websocket.send(json.dumps(connect_event))
            connect_event = {
                "event": "SERVICE-DATA",
                "client-type": client_type,
                "client-name": "Controller",
                "data": {},
                "media": detect_media()
            }
            await websocket.send(json.dumps(connect_event))
            while True:
                try:
                    data = json.loads(await websocket.recv())
                    if data:
                        # SERVER CONTROL EVENTS
                        if data["event"] == "SERVICE-DATA":
                            if data['data']:
                                if data['data'].get('TARGET-CLIENT') == 'Controller':
                                    match data["data"].get("COMMAND"):
                                        case "play-pause":
                                            pyautogui.keyDown('playpause')
                                        case "next":
                                            pyautogui.keyDown('nexttrack')
                                        case "previous":
                                            pyautogui.keyDown('prevtrack')
                                        case "live":
                                            liveScreen()
                                        case "brb":
                                            brbScreen()

                        if data.get("data"):
                            if isinstance(data['data'], dict):
                                if data['data'].get('TARGET-CLIENT') == 'Controller':
                                    print('1')
                                    if data["data"].get('LEVEL'):
                                        print('level')
                                        media = data['data']['MEDIA']
                                        level = int(data["data"]["LEVEL"]) / 100
                                        detected_media = detect_media()
                                        set_volume(detected_media, media, level)
                        # SERVER DATA REQUESTS
                        if data["event"] == "DATA-REQUEST":
                            print('req', data)
                            if data['data'].get('TARGET-CLIENT') == 'Controller':
                                match data['data']['QUERY']:
                                    case "level":
                                        target = data['data']['TARGET']
                                        if target in detect_media():
                                            response = {
                                                "event": "SERVICE-DATA",
                                                "client-type": client_type,
                                                "client-name": "Controller",
                                                "data": {
                                                    'QUERY-RESPONSE': 'level',
                                                    'TARGET': target,
                                                    'VALUE': detect_media()[target]
                                                         }
                                                }
                                            await websocket.send(json.dumps(response))
                                    case "all":
                                        print('responding...')
                                        response = {
                                            "event": "SERVICE-DATA",
                                            "client-type": client_type,
                                            "client-name": "Controller",
                                            "data": {},
                                            "media": detect_media()
                                        }
                                        await websocket.send(json.dumps(response))

                        data = None

                except ConnectionClosedError:
                    print("The server has shut down!")
                    break

    except ConnectionRefusedError:
        print("Server is either offline, or connection point is wrong!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hardware client for Terrace")
    parser.add_argument("host", metavar="host", type=str, help="Enter the host URL")
    args = parser.parse_args()

    host = args.host
    asyncio.run(client(host))


