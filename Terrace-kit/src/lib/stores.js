import { writable } from 'svelte/store';
let wsMessage
let websocket

export const state = writable({
    websocket: websocket,
    wsMessage: wsMessage
});

export const websocketConnect = (url) => {
    console.log('webscoket connect')
    let ws = new WebSocket(`${url}/ws/stats`);
    ws.addEventListener('open', () => {
        ws.send(JSON.stringify({ event: 'CONNECT', 'client-type': 'DASHBOARD', 'client-name': "" }));
    });

    ws.addEventListener('message', (message) => {
        const data = JSON.parse(message.data);
        if (data.event === 'CONNECT') {
            websocket = ws
        }
        state.update((state) => ({
            ...state,
            websocket: ws,
            wsMessage: data,
        }));
        
    });
};

export const websocketDisconnect = () => {
    if (websocket !== undefined) {
        websocket.send(JSON.stringify({ event: 'DISCONNECT', 'client-type': 'DASHBOARD',
        'client-name': "" }));   
        state.update((state) => ({
            ...state,
            websocket: undefined,
        }));
    }
};

export const websocketSend = (dataType, data) => {
    if (websocket !== undefined) {
        websocket.send(JSON.stringify({ event: dataType, 'client-type': 'DASHBOARD', 
        'name': 'name', ...data }));  
    }
};

export const currentNavStore = writable('Settings');
export const activeHardwareClient = writable('');
export const serviceStore = writable({});

