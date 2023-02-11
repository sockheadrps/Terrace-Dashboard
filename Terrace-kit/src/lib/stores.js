import { writable } from 'svelte/store';
let hardwareList = [];
let serviceList = [];
let services = {}
let hardwareData;
let wsMessage
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
export function wsDisconnect () {
    ws.send(JSON.stringify(
        { event: 'DISCONNECT', 'client-type': 'DASHBOARD' }));
}

/**
 * Function for disconnecting active hardware clients
 * @param {client-name} hardwareClient
 */
export function terminateHwCommunication (hardwareClient) {
    ws.send(JSON.stringify(
        { event: 'HARDWARE-TERMINATE', 'requested-client': hardwareClient }));
}

export const state = writable({
    wsMessage: "",
    data: [],
    hardwareList: [],
    hardwareData: [],
    serviceList: [],
    services: []
});

export const websocketConnect = (url) => {
    ws = new WebSocket(`${url}/ws/stats`);
    ws.addEventListener('open', () => {
        ws.send(JSON.stringify({ event: 'CONNECT', 'client-type': 'DASHBOARD' }));
    });

    ws.addEventListener('message', (message) => {
        const data = JSON.parse(message.data);
        console.log(data)
        wsMessage = data
        if (data.event === 'CONNECT') {
            if (data['hardware-list']) {
                hardwareList = data['hardware-list'];
            }
            if (data['service-list']) {
                serviceList = data['service-list'];
            }
            if (data['client-type'] === 'HARDWARE') {
                hardwareList.push(data['client-name']);
            }
            if (data['client-type'] === 'SERVICE') {
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
                services = services.filter(
                    function (e) { return e !== data['client-name']; }
                );
            }
        }

        if (data.event === 'HARDWARE-DATA') {
            hardwareData = data.data;
        }
        if (data.event === 'SERVICE-DATA') {
            services[data['client-name']] = data.data
        }
            
        state.update((state) => ({
            ...state,
            message: wsMessage,
            data: [data],
            hardwareList: [hardwareList],
            hardwareData: [hardwareData],
            serviceList: [serviceList][0],
            services:{services}
        }));
        
    });
};

export const currentNavStore = writable('Settings');
export const activeHardwareClient = writable('');
