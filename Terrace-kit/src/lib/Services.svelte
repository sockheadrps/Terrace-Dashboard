<script lang="ts">
	import { state, serviceStore, websocketSend } from '$lib/stores';
	import { onMount } from 'svelte';
	import Icon from '@iconify/svelte';
	import { serviceList, newService, loadServices, saveServices } from './stores/serviceStore';
	import { fade } from 'svelte/transition';
	import { flip } from 'svelte/animate';

	let services = [];
	let serviceElms = {};
	let name: string;
	let serviceDiv: HTMLElement;
	let initialConnect = true;
	let serviceIcons = {};
	let ready = false;
    let orderChange = false

	onMount(() => {
		websocketSend('CONNECTIONS-REQUEST', {});
		$serviceList = loadServices();
		ready = true;
	});



    function orderServices(services){
        let orderedServices: Array<string> = []
        let serviceNames: Array<string> = $serviceList.map((e) => e.name);
            services.forEach(element => {
                let idx = serviceNames.indexOf(element)                
                orderedServices.splice(idx, 0, element)
            });
            services = []
            return orderedServices
    }

	function animateElement(elm) {
		elm.style.transition = 'none';
		elm.style.border = '3px solid rgba(24, 24, 24, 0.95)';
		elm.style.color = 'rgba(90, 90, 90, 0.95)';
		const value = '1px';
		const transitionDuration = '250ms';
		const timing = 'linear';
		const delay = '0s';
		requestAnimationFrame(() => {
			requestAnimationFrame(() => {
				elm.style.transition = `color ${transitionDuration} ${timing} ${delay}`;
				elm.style.color = 'rgba(160, 160, 160, 0.95)';
			});
		});
	}

	// Handle WS connection and messages.
	$: if ($state.wsMessage !== undefined) {
		switch ($state.wsMessage.event) {
			case 'CONNECT':
				websocketSend('CONNECTIONS-REQUEST', {});
				break;
			case 'DISCONNECT':
				websocketSend('CONNECTIONS-REQUEST', {});
				break;
			case 'SERVICE-DATA':
				if ($state.wsMessage['client-name'] === 'Controller') {
					name = $state.wsMessage['client-name'];
					if (services !== undefined && serviceElms !== undefined) {
						serviceDiv = serviceElms[name];
						if (!services.includes($state.wsMessage['client-name'])) {
							services.push($state.wsMessage['client-name']);
						}
						if (serviceDiv !== undefined && serviceDiv !== null) {
							// animateElement(serviceDiv)
						}
					}
				}
				break;
			case 'CONNECTIONS-REQUEST':
				services = $state.wsMessage['service-list'];
		}
	}

    $: {
        $serviceList = $serviceList
        services = orderServices(services)
    }

	$: {
		if (ready) {
			let serviceNames: Array<string> = $serviceList.map((e) => e.name);
			let unsavedServices: Array<string> = services.filter((e) => !serviceNames.includes(e));

			$serviceList = [
				...$serviceList,
				...unsavedServices.map((e) => ({ name: e, icon: 'material-symbols:electrical-services' }))
			];
			services.forEach((element) => {
				serviceIcons[element] = $serviceList.find((e) => e.name === element)?.icon;
			});
		}
	}

</script>

{#if services !== undefined && services.length > 0 && serviceElms !== undefined}
	{#each services as service (service)}
		<a href="/services/{service}"
		>
			<button
				class="bg-original-card-bg-dark rounded-md text-original-muted mb-4 mx-2 flex-1 md:w-32 w-20 md:h-[136px] h-24 transition-colors hover:text-original-muted-hover hover:bg-original-service-dark"
				transition:fade
				bind:this={serviceElms[service]}
			>
				<div class="md:text-8xl text-4xl flex flex-col text-center justify-center">
					<div class="mx-auto">
						<Icon icon={serviceIcons[service]} />
					</div>
				</div>
			</button>
		</a>
	{/each}
{/if}
