<script>
	let settingsItemsTop = [
		{ name: 'Server', icon: 'heroicons:server-stack', timing: 100 },
		{ name: 'Bookmarks', icon: 'bi:bookmarks', timing: 250 }
	];
	let settingsItemsBottom = [
		{ name: 'Weather', icon: 'fluent:weather-cloudy-48-regular', timing: 350 },
		{ name: 'Services', icon: 'carbon:microservices-1', timing: 450 }
	];
	import Icon from '@iconify/svelte';
	import { fade } from 'svelte/transition';
    import { onMount } from 'svelte';
	import { quintIn } from 'svelte/easing';
    let ready = false

    onMount(() => {
        ready=true
    })


</script>

<!-- cbody -->
{#if ready}
<div class="w-full flex justify-center">
	<nav class="flex justify-center items-center h-full my-auto">
		<!-- container -->
		<div class="flex justify-center items-center flex-col flex-wrap">
			<!-- First row -->
			<div class="flex">
				<!-- Hexagon -->
				{#each settingsItemsTop as setting}
					<a href="/settings/{setting.name.toLowerCase()}"
					in:fade={{duration:300, easing: quintIn, delay:setting.timing}}>
						<button class="w-20 h-20 relative mx-2 bg-original-settings-nav-bg hexagon hover:bg-original-settings-nav-bg-hover"
						>
							<div class="text-4xl flex justify-center">
								<Icon icon={setting.icon} />
							</div>
						</button>
					</a>
				{/each}
			</div>

			<div class="flex ml-2 -my-2">
				{#each settingsItemsBottom as setting}
					<a href="/settings/{setting.name.toLowerCase()}"
					in:fade={{duration:300, easing: quintIn, delay:setting.timing}}>
						<button class="w-20 h-20 relative mx-2 bg-original-settings-nav-bg hexagon hover:bg-original-settings-nav-bg-hover">
							<div class="text-4xl flex justify-center">
								<Icon icon={setting.icon} />
							</div>
						</button>
					</a>
				{/each}
                <!-- Necessary dummy div for spacing the hexagons, remove if an odd number -->
				<div class="bg-none w-20 h-20 relative mx-3 hexagon" />
			</div>
		</div>
	</nav>
</div>
{/if}
<style>
	.hexagon {
        border: 2px;
		clip-path: polygon(0 25%, 50% 0, 100% 25%, 100% 75%, 50% 100%, 0 75%);
        box-shadow: 0 0 0 0 #ffffff, 0 2px 3px 0 rgba(0, 0, 0, 0.062);
		transition: 0.2s cubic-bezier(0, 1.2, 0.2, 1.5);
	}

    .hexagon:active {
		background-color: #2e57858a;
	}
	.hexagon:hover{
		transform: scale(1.1); 
		
	}

	.hexagon:hover:active {
		transform: scale(0.99); 

	}
</style>
