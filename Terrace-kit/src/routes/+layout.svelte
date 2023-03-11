<script lang="ts">
	import NavBar from '$lib/NavBar.svelte';
	import { onDestroy, onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import '../app.css';
	export const trailingSlash = 'ignore';
	import { websocketConnect } from '../lib/stores';
	let ready = false;
	import { quintIn } from 'svelte/easing';
	
	

	onMount(() => {
		let localStorage: { url: string } | null;
		localStorage = JSON.parse(window.localStorage.getItem('server'));
		console.log({ localStorage });
		if (localStorage !== null) {
			websocketConnect(localStorage.url.replace(/(http)s?:\/\//, 'ws://'));
		}
		ready = true;
	});


	// If window closes while communicating with a hw client, let it know to stop communicating with server
	function beforeunload() {
		// if (activeHardwareClient) {
		//     terminateHwCommunication(activeHardwareClient)
		// }
		// // Let the server know the dashboard has disconnected
		// wsDisconnect()
	}

	// Function for window on load
	function onConnect() {
		// make initial WS connection
		// websocketConnect()
	}
</script>

{#if ready}
<div class="main">
	<div id="board" class="grid grid-cols-12 justify-center original-theme -z-10 backdrop-blur-sm h-screen bg-clip-content"
	>	
		<div class="col-span-2">
			<NavBar />

		</div>
		<div class="col-span-10 ">
			<!-- <div class="text-original-base flex flex-row justify-end">
				<button class="w-24 rounded-md bg-slate-800 mx-2">
					Sign up
				</button>
				<button class="w-24 rounded-md bg-slate-800 mx-2">
					Login
				</button>
			</div> -->
				<slot />
		</div>
	</div>
</div>

{/if}

<style>
	@import url('https://fonts.googleapis.com/css2?family=Asap&family=Spline+Sans:wght@500&display=swap');
	.main {
		background: url('/assets/backgrnd.jpeg');
		background-size: cover;
		background-repeat: no-repeat;
		overflow: hidden;
	}
	#board {
		/* grid-template-columns: 15% 85%; */
		background: linear-gradient(to left top, rgba(36, 36, 36, 0.719), rgba(20, 20, 20, 0.671));
	}
	*{
		font-family: 'Asap', sans-serif;
		font-family: 'Spline Sans', sans-serif;
		
    }
</style>


