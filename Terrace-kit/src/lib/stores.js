import { writable } from 'svelte/store';
let wsMessage
let websocket

export const state = writable({
    websocket: websocket,
    wsMessage: wsMessage
});

export const websocketConnect = (url) => {
    let ws = new WebSocket(`${url}/ws/stats`);
    ws.addEventListener('open', () => {
        ws.send(JSON.stringify({ event: 'CONNECT', 'client-type': 'DASHBOARD' }));
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
        websocket.send(JSON.stringify({ event: 'DISCONNECT', 'client-type': 'DASHBOARD' }));   
        state.update((state) => ({
            ...state,
            websocket: undefined,
        }));
    }
};

export const websocketSend = (dataType, data) => {
    if (websocket !== undefined) {
        websocket.send(JSON.stringify({ event: dataType, 'client-type': 'DASHBOARD', 'data': data }));   
    }
};


// export const state = writable({
//     websocket: ws,
//     wsMessage: "",
//     data: [],
//     hardwareList: [],
//     hardwareData: [],
//     serviceList: [],
//     services: []
// });

// export const websocketConnect = (url) => {
//     ws = new WebSocket(`${url}/ws/stats`);
//     ws.addEventListener('open', () => {
//         ws.send(JSON.stringify({ event: 'CONNECT', 'client-type': 'DASHBOARD' }));
//     });

//     ws.addEventListener('message', (message) => {
//         const data = JSON.parse(message.data);
//         console.log(data)
//         wsMessage = data
//         if (data.event === 'CONNECT') {
//             if (data['hardware-list']) {
//                 hardwareList = data['hardware-list'];
//             }
//             if (data['service-list']) {
//                 serviceList = data['service-list'];
//             }
//             if (data['client-type'] === 'HARDWARE') {
//                 hardwareList.push(data['client-name']);
//             }
//             if (data['client-type'] === 'SERVICE') {
//                 serviceList.push(data['client-name']);
//             }
//         }
//         if (data.event === 'DISCONNECT') {
//             if (data['client-type'] === 'HARDWARE') {
//                 hardwareList = hardwareList.filter(
//                     function (e) { return e !== data['client-name']; }
//                 );
//             } else if (data['client-type'] === 'SERVICE') {
//                 serviceList = serviceList.filter(
//                     function (e) { return e !== data['client-name']; }
//                 );
//                 services = services.filter(
//                     function (e) { return e !== data['client-name']; }
//                 );
//             }
//         }

//         if (data.event === 'HARDWARE-DATA') {
//             hardwareData = data.data;
//         }
//         if (data.event === 'SERVICE-DATA') {
//             services[data['client-name']] = data.data
//         }
            
//         state.update((state) => ({
//             ...state,
//             websocket:
//             message: wsMessage,
//             data: [data],
//             hardwareList: [hardwareList],
//             hardwareData: [hardwareData],
//             serviceList: [serviceList][0],
//             services:{services}
//         }));
        
//     });
// };

export const currentNavStore = writable('Settings');
export const activeHardwareClient = writable('');
export const serviceStore = writable({});

