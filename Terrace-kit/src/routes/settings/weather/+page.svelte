<script lang="ts">
	import { fade } from 'svelte/transition';
	import { quintIn, quintOut } from 'svelte/easing';
	import { onMount } from 'svelte';
	import Card from './Components/Card.svelte';
	import ServerCard from './Components/ServerCard.svelte';
	let longitude = ""
	let latitude = ""
	let apiKey = '';
	let response = 0;
	let ready = false;
	let success = false
	let url: string
	let respCode = 0

	onMount(() => {
		ready = true;
	});

</script>

{#if ready}
	<div
		class="flex flex-col text-center"
		in:fade={{ duration: 250, easing: quintIn, delay:200 }}
		out:fade={{ duration: 250, easing: quintOut }}
	>
		<label class="text-6xl tablet:text-2xl pt-10" for="Weather API">Weather API</label>
		<div class="mx-6">
			<div class="mt-20 flex flex-row gap-x-20 mx-10 justify-center">
				<div class="tablet:h-28">
					<Card
						bind:data={latitude}
						dataName={'Latitude'}
						checkInput={async (value) =>
							isNaN(value) || parseFloat(value) > 90 || parseFloat(value) < -90}
					/>
				</div>

				<div class="tablet:h-28">
					<Card
						bind:data={longitude}
						dataName={'Longitude'}
						checkInput={async (value) =>
							isNaN(value) || parseFloat(value) > 180 || parseFloat(value) < -180}
					/>
				</div>

				<div class="tablet:h-28">
					<ServerCard
						bind:data={apiKey}
						bind:long={longitude}
						bind:lat={latitude}
					/>
				</div>
			</div>
			<div class="row-span-2 w-1/2">
				{#if response === 200}
					<div class="bg-green-500 h-10 mx-20" />
				{:else if response === 401 || response === 400}
					<div class="bg-yellow-500 h-10 mx-20" />
				{:else}
					<div class="opacity-0 h-10 mx-20" />
				{/if}
			</div>
		</div>
	</div>
{/if}
