<script lang="ts">
	import { websocketSend } from '$lib/stores';
	export let iconName: undefined | string;
	import Icon from '@iconify/svelte';
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';
	export let buttonCommand: undefined | string;
	export let name: undefined | string;
	export let targetClient: undefined | string;
	export let onHoverIcon = '';
	let hovering = false;
	let displayedIcon = iconName;
	let ready = false;

	onMount(() => {
		ready = true;
	});

	$: {
		console.log(buttonCommand, iconName);
	}

	function handleClick() {
		console.log('click');
		websocketSend('SERVICE-DATA', { 'TARGET-CLIENT': targetClient, COMMAND: buttonCommand });
	}
</script>

{#if ready}
	<button
		class="h-32 m-2 bg-original-card-bg-dark text-original-muted px-6
        rounded-md transition-colors hover:text-original-muted-hover 
        hover:bg-original-service-dark text-center hover:text-red-500"
		on:mouseover={() => {
			displayedIcon = onHoverIcon;
		}}
		on:mouseleave={() => {
			displayedIcon = iconName;
		}}
		on:focus={() => {
			displayedIcon = iconName;
		}}
		on:click|preventDefault={() => handleClick()}
        in:fade={{ duration: 250, delay: 250 }}
	>
		<div class="text-7xl text-center m-1 relative" transition:fade|local>
			<Icon icon={displayedIcon} />
		</div>

		<div class="text-center">
			{name}
		</div>
	</button>
{/if}
