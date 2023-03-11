<script lang="ts">
	import Icon from '@iconify/svelte';
	import { fade } from 'svelte/transition';
	import { onDestroy, onMount } from 'svelte';
	import { state, websocketSend } from '../../../lib/stores';
	import Button from '../Button/Button.svelte';
	import { flip } from 'svelte/animate';
	let playing = false;
	let sliderValue: number;
	let sliderElm: undefined | HTMLElement;
	let mediaChoices = [];
	let selected = '';
	let ready = false;

	function setSlider() {
		websocketSend('DATA-REQUEST', {
			'TARGET-CLIENT': 'Controller',
			QUERY: 'level',
			TARGET: selected
		});
	}

	$: {
		// Get Media
		if ($state.wsMessage !== undefined && Object.keys($state.wsMessage).length > 0) {
			if ('media' in $state.wsMessage) {
				mediaChoices = Object.keys($state.wsMessage.media);
			} else if ('data' in $state.wsMessage) {
				if (Object.hasOwn($state.wsMessage.data, 'QUERY-RESPONSE')) {
					if ($state.wsMessage.data['QUERY-RESPONSE'] === 'level') {
						sliderValue = $state.wsMessage.data['VALUE'] * 100;
					}
				}
			}
		}
	}

	$: if (sliderValue !== undefined) {
		websocketSend('SERVICE-DATA', {
			'TARGET-CLIENT': 'Controller',
			LEVEL: sliderValue,
			MEDIA: selected
		});
	}

	$: {
		if (sliderElm !== undefined) {
			sliderElm.style.background = `linear-gradient(90deg,rgb(15, 15, 15) ${sliderValue}%, rgb(35, 35, 35) ${sliderValue}%)`;
		}
	}
	onMount(() => {
		ready = true;
		websocketSend('DATA-REQUEST', { 'TARGET-CLIENT': 'Controller', QUERY: 'all' });
	});
	onDestroy(() => (ready = false));
</script>

{#if ready == true}
	<div class="flex flex-col justify-center pt-10 tablet:pt-5" in:fade>
		<div class="flex flex-row justify-center opacity-60 hover:opacity-95">
			<select
				class="w-1/3 h-12 outline-none rounded-2xl border-2 bg-original-table-header border-original-dark text-original-muted text-2xl text-center cursor-pointer"
				bind:value={selected}
				on:change={() => setSlider()}
			>
				{#each mediaChoices as choice}
					<option value={choice}>
						{choice}
					</option>
				{/each}
			</select>
		</div>

		<div class="flex flex-row justify-center mt-10 tablet:mt-5 items-center">
			<!-- Previous button -->
			<button
				class="flex items-center justify-center p-3 h-24 w-24 border-4 m-2 text-5xl rounded-full border-original-dark text-original-muted gradient backdrop:blur-sm focus:outline-none"
				on:click|preventDefault={() =>
					websocketSend('SERVICE-DATA', { 'TARGET-CLIENT': 'Controller', COMMAND: 'previous' })}
			>
				<Icon icon="fluent:previous-16-regular" />
			</button>

			<!-- Play/Pause -->
			<button
				class="flex items-center justify-center p-3 h-28 w-28 border-4 m-2 text-6xl
                    rounded-full border-original-dark text-original-muted gradient backdrop:blur-sm
                    focus:outline-none"
				on:click|preventDefault={() => {
					websocketSend('SERVICE-DATA', { 'TARGET-CLIENT': 'Controller', COMMAND: 'play-pause' });
					playing = !playing;
				}}
			>
				{#if playing}
					<div
						class="absolute"
						in:fade={{ delay: 250, duration: 250 }}
						out:fade={{ duration: 250 }}
					>
						<Icon icon="fluent:play-16-regular" />
					</div>
				{:else}
					<div
						class="absolute"
						in:fade={{ delay: 250, duration: 250 }}
						out:fade={{ duration: 250 }}
					>
						<Icon icon="fluent:pause-16-regular" />
					</div>
				{/if}
			</button>
			<!-- Next button -->
			<button
				class="flex items-center justify-center h-24 w-24 p-3 border-4 m-2 text-5xl rounded-full border-original-dark text-original-muted gradient     backdrop:blur-sm focus:outline-none"
				on:click|preventDefault={() =>
					websocketSend('SERVICE-DATA', { 'TARGET-CLIENT': 'Controller', COMMAND: 'next' })}
			>
				<Icon icon="fluent:next-16-regular" />
			</button>
		</div>
		<div class=" flex flex-row w-2/3 align-middle mx-auto mt-10 " id="volume-area">
			<input
				class="appearance-none w-full h-6 outline-none opacity-70 rounded-md shadow-lg transition-opacity slider hover:opacity-100"
				bind:value={sliderValue}
				bind:this={sliderElm}
				type="range"
				id="volume"
				min="0"
				max="100"
			/>
		</div>
		<div class="h-1/3 mt-5 flex justify-center align-top">
			<Button
				iconName="fluent:live-20-filled"
                onHoverIcon="fluent:live-20-filled"
				buttonCommand="live"
				name="Live"
				targetClient="Controller"
			/>
			<Button
				iconName="material-symbols:back-hand-outline"
                onHoverIcon="material-symbols:back-hand-outline"
				buttonCommand="brb"
				name="BRB"
				targetClient="Controller"
			/>
		</div>
	</div>
{/if}

<style>
	.gradient {
		background: linear-gradient(rgb(22, 22, 22), rgb(51, 51, 51)) padding-box,
			linear-gradient(to right, rgba(0, 0, 0, 0.678), rgba(0, 0, 0, 0.548)) border-box;
	}
	.gradient:hover {
		background: linear-gradient(rgb(15, 15, 15), rgb(48, 48, 48)) padding-box,
			linear-gradient(to right, rgba(0, 0, 0, 0.397), rgba(0, 0, 0, 0.281)) border-box;
		color: #525151;
	}

	.slider {
		background: linear-gradient(90deg, rgb(15, 15, 15) 50%, rgb(35, 35, 35) 50%);
		cursor: pointer;
	}

	.slider::-webkit-slider-thumb {
		appearance: none;
		width: 40px;
		height: 40px;
		background: rgb(63, 63, 63);
		border-radius: 50%;
		opacity: 0.95;
	}
</style>
