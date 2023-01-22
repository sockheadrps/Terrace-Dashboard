import { writable } from 'svelte/store';
let hardwareList = [];
let serviceList = [];
let hardwareData = '';
let ws = '';

/**
 * Function for websocket communication
 * @param {jsonObject} event
 */
export function wsSend (event) {
  ws.send(JSON.stringify(event));
}

/**
 * Function for disconnecting websockets
 * @param {client-name} hardwareClient
 */
export function wsDisconnect (hardwareClient) {
  ws.send(JSON.stringify(
    { event: 'HARDWARE-TERMINATE', 'requested-client': hardwareClient }));
}

export const state = writable({
  data: []
});

export const connect = () => {
  ws = new WebSocket('ws://192.168.1.117:8081/ws/stats');
  ws.addEventListener('open', () => {
    ws.send(JSON.stringify({ event: 'CONNECT', 'client-type': 'DASHBOARD' }));
  });

  ws.addEventListener('message', (message) => {
    const data = JSON.parse(message.data);
    console.log(JSON.stringify(data));

    if (data.event === 'CONNECT') {
      if (data['hardware-list']) {
        hardwareList = data['hardware-list'];
      } else if (data['serive-list']) {
        serviceList = data['service-list'];
      }
      if (data['client-type'] === 'HARDWARE') {
        hardwareList.push(data['client-name']);
      } else if (data['client-type'] === 'SERVICE') {
        serviceList.push(data['client-name']);
      }
    }
    if (data.event === 'DISCONNECT') {
      if (data['client-type'] === 'HARDWARE') {
        hardwareList = hardwareList.filter(
          function (e) { return e !== data['client-name']; }
        );
      } else if (data['client-type'] === 'SERVICE') {
        serviceList = serviceList.filter(
          function (e) { return e !== data['client-name']; }
        );
      }
    }

    if (data.event === 'HARDWARE-DATA') {
      hardwareData = data.data;
    }
    state.update((state) => ({
      ...state,
      data: [data],
      hardwareList: ['hardwareList'],
      hardwareData: [hardwareData],
      serviceList: [serviceList]
    }));
  });
};

export const currentNav = writable('Home');
export const activeHardwareClient = writable('');
