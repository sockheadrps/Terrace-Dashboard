<script>
	import ToggleButton from '../Button/ToggleButton.svelte';
	import Button from '../Button/Button.svelte';
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';
	let ready = false;
	onMount(() => {
		ready = true;
	});
</script>

{#if ready}
	<div class="flex flex-row justify-center mt-10 items-center"
    in:fade={{ delay: 250, duration: 250 }} out:fade={{ duration: 250 }}>
		<div class="h-1/3 mt-5 flex justify-center align-top">
			<ToggleButton
				OniconName="mdi:microphone-plus"
				commandType="TTS"
				buttonOnCommand={true}
				OfficonName="mdi:microphone-minus"
				buttonOffCommand={false}
				name="TTS"
			/>
		</div>
		<div class="h-1/3 mt-5 flex justify-center align-top">
			<Button
				buttonCommand="STOP-TTS"
				name="STFU TTS"
				iconName="mdi:face"
				onHoverIcon="mdi:emoticon-dead"
				targetClient="Twitch"
			/>
		</div>
	</div>
{/if}
