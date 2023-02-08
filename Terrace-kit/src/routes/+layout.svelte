<script>
import NavBar from "$lib/NavBar.svelte";
import "../app.css";
import { activeHardwareClient, wsDisconnect, terminateHwCommunication, websocketConnect } from "$lib/stores.js";

// If window closes while communicating with a hw client, let it know to stop communicating with server
function beforeunload() {
    if (activeHardwareClient) {
        terminateHwCommunication(activeHardwareClient)
    }
    // Let the server know the dashboard has disconnected
    wsDisconnect()
}

// Function for window on load
function onConnect() {
    // make initial WS connection
    websocketConnect()
}
</script>

<div id="board">
    <NavBar />
    <slot />
</div>

<style>
#board {
    display: grid;
    height: 90vh;
    grid-template-columns: 15% 85%;
    background: linear-gradient(
        to left top,
        rgba(36, 36, 36, 0.822),
        rgba(20, 20, 20, 0.863)
    );

    z-index: -1;
    backdrop-filter: blur(.23rem);
    border-radius: 2rem;
}
</style>