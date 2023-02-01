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
	}
	main {
		text-align: center;
		padding: 1em;
		margin: 0 auto;
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
