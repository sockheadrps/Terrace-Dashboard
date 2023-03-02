<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';
	import Icon from '@iconify/svelte';
	const dispatch = createEventDispatcher();
	const home = { link: '', icon: 'ic:outline-space-dashboard', endPoint: '/' };
	const settings = {
		link: 'settings/weather',
		icon: 'ion:settings-outline',
		endPoint: '/settings/weather'
	};
	import { state, websocketConnect } from './stores';
	import { page } from '$app/stores';
	import Services from '$lib/Services.svelte';
	import { serviceList, loadServices } from './stores/serviceStore';
	import { fly, fade } from 'svelte/transition';

	onMount(() => {
		$serviceList = loadServices();
	});

	//import {state} from '../../stores.js'
	let hardware = [];

	/*state.subscribe(value => {
        if (value.hardwareList){
            hardware = value.hardwareList[0]
        }
    });*/
	function handleClick() {
		if ($state.websocket === undefined) {
			let localStorage: { url: string } | null;
			localStorage = JSON.parse(window.localStorage.getItem('server'));
			console.log({ localStorage });
			if (localStorage !== null) {
				websocketConnect(localStorage.url.replace(/(http)s?:\/\//, 'ws://'));
			}
		}
	}
</script>

<div class="flex flex-col h-screen w-full pt-5">
	<nav class="h-full relative flex flex-col bg-original-nav-background px-1">
		<div class="grid grid-rows-6 h-full">
			<div class="overflow-y-auto flex-row row-span-5">
				<div class="text-center">
					<Services />
				</div>
			</div>

			<div class="text-center flex h-full">
				<div class="m-auto">
					{#if $page.url.pathname === '/'}
						<a href="/{settings.link}">
							<button class="" on:click={() => handleClick()}>
								<div
									class="text-5xl bg-original-card-bg-dark text-original-muted p-2
                                    rounded-md transition-colors hover:text-original-muted-hover 
                                    hover:bg-original-service-dark"
									in:fly={{ x: 100, delay: 250, duration: 250 }}
									out:fly={{ x: -100, duration: 250 }}
								>
									<Icon icon={settings.icon} />
								</div>
							</button>
						</a>
					{:else}
						<a href="/{home.link}">
							<button class="" on:click={() => handleClick()}>
								<div
									class="text-5xl bg-original-card-bg-dark text-original-muted p-2
                                rounded-md transition-colors hover:text-original-muted-hover 
                                hover:bg-original-service-dark"
									in:fly={{ x: 100, delay: 250, duration: 250 }}
									out:fly={{ x: -100, duration: 250 }}
								>
									<Icon icon={home.icon} />
								</div>
							</button>
						</a>
					{/if}
				</div>
			</div>
		</div>
	</nav>
</div>
