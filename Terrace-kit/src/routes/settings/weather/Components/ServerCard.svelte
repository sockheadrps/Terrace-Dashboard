<script lang="ts">
	import Icon from '@iconify/svelte';
	export let data: string;
	export let long: string;
	export let lat: string;
	let timerID = 0;
	let respCode = 0;

	function checkAPI(key: string, long: string, lat: string) {
		let url = `https://api.openweathermap.org/data/2.5/weather?lat=${long}&lon=${lat}&appid=${key}`;
        console.log(data)

		clearTimeout(timerID);
		if (url !== undefined && data.length === 32) {
			timerID = window.setTimeout(() => {
				console.log(url, 'url');
				fetch(url)
					.then((response) => response)
					.then((response) => {
                        console.log(response)    
						respCode = response.status
					})
					.catch((e) => {
						respCode = 404;
					});
			}, 1500);
		}
	}

	$: if (data.length === 32) {
        console.log('checking apoi ', respCode)
		checkAPI(data, long, lat);
	}

    $: console.log(respCode)
</script>

<div class="h-full grid grid-rows-3">
	<div class="flex justify-center items-center text-6xl">
		{#if respCode === 200}
			<div>
				<Icon icon="emojione:white-heavy-check-mark" />
			</div>
		{/if}
		{#if respCode !== 200 && data.length !== 32 && data.length !== 0}
			<div>
				<Icon icon="emojione:cross-mark-button" />
			</div>
		{/if}
		{#if respCode === 401}
			<div>
				<Icon icon="emojione:slightly-frowning-face" />
			</div>
		{/if}
	</div>
	<h1 class="md:text-4xl text-2xl">Server</h1>
	<div>
		<input
			type="text"
			class="w-full h-10 text-original-base bg-original-fill outline-none border-b-2 border-original-muted hover:bg-original-input-hover text-center"
			placeholder="Server IP..."
			bind:value={data}
		/>
	</div>
</div>
