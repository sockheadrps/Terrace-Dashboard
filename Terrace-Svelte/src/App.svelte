<script>
    import Board from "./components/Board/Board.svelte";
	import { activeHardwareClient, wsDisconnect, terminateHwCommunication, websocketConnect } from "../src/stores.js";

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

<svelte:window on:beforeunload={beforeunload} on:load={onConnect}/>
<main>
	<Board />
</main>

<style>
:global(:root) {
    overflow: hidden ;
    display: flex;
    flex-direction: column;
    height: 100vh;
    justify-content: center;
    background: Radial-gradient(rgba(255, 255, 255, 0.35), rgb(43, 43, 43)), Radial-gradient(at 0 0, #181818, #1f1f1f);
}

:global(body) {
    margin: 0;
}

:global(.scroll::-webkit-scrollbar) {
    display: block;
    background: rgba(0, 0, 0, 0);
}

:global(.scroll::-webkit-scrollbar-track) {
    border-radius: 10px;
    background-clip: padding-box;
    margin-right: -1rem;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

:global(.scroll::-webkit-scrollbar-track-piece:end) {
    background: transparent;
}

:global(.scroll::-webkit-scrollbar-track-piece:start) {
    background: transparent;
}

:global(.scroll::-webkit-scrollbar-thumb) {
    background: rgb(44, 44, 44);
    border-radius: 10px;
    border: 5px solid #0000;
    background-clip: padding-box;
}

:global(.scroll::-webkit-scrollbar-thumb:hover) {
    background: #222;
    background-clip: padding-box;
}

main {
    text-align: center;
    /* padding: 1em; */
    /* margin: 0 auto; */
}

@media (min-width: 640px) {
    main {
        max-width: 700;
    }
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Asap', sans-serif;
    font-family: 'Spline Sans', sans-serif;
}

main{
    height: 100%;
}
</style>
