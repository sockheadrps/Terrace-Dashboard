<script lang="ts">
	import { serviceList, saveServices, loadServices, deleteService } from '$lib/stores/serviceStore';
	import AddService from './AddService.svelte';
	import Icon from '@iconify/svelte';
	import 'iconify-icon';
	import type { Service, KeyFrame } from '$lib/stores/serviceTypes';
	import { fade } from 'svelte/transition';
	import { quintIn, quintOut } from 'svelte/easing';
	let currentService: Service | undefined;
	let name = '';
	let url = '';
	let body: Element;
	let index: number;
	let afterIndex: number;
	let position: object;

	function editService(event: MouseEvent, service: Service) {
		position = {
			x: event.srcElement.getBoundingClientRect().x,
			y: event.srcElement.getBoundingClientRect().y,
			iconWidth: event.srcElement.getBoundingClientRect().width,
			iconHeight: event.srcElement.getBoundingClientRect().height
		};
		currentService = service;
	}

	function handleDragEnd() {
		let startKeys = transitionKeys();
		let endKeys = move([...startKeys], index, afterIndex);

		animateShift(startKeys, endKeys);
		move($serviceList, index, afterIndex);

		$serviceList = $serviceList;
		saveServices($serviceList);
	}

	function transitionKeys() {
		return Array.from(body.children).map((e) => e.getBoundingClientRect());
	}

	function animateShift(startKeys: KeyFrame[], endKeys: KeyFrame[]) {
		requestAnimationFrame(() => {
			let children = Array.from(body.children) as HTMLElement[];
			children.forEach((e, idx) => {
				e.style.transition = 'transform 0s';
				e.style.transform = `translate(${endKeys[idx].x - startKeys[idx].x}px, ${
					endKeys[idx].y - startKeys[idx].y
				}px)`;
			});

			requestAnimationFrame(() => {
				let cnt = index < afterIndex ? 0 : index - afterIndex - 1;
				children.forEach((e, idx) => {
					if (idx !== afterIndex) {
						e.style.transition = `transform 500ms ${cnt * 50}ms ease-in-out`;
						if (index < afterIndex) cnt += index <= idx ? 1 : 0;
						else cnt -= idx < index ? 1 : 0;
					} else {
						e.style.transition = `transform ${
							450 + Math.abs(afterIndex - index) * 50
						}ms ease-in-out`;
					}
					e.style.transform = '';
				});
			});
		});
	}

	function move(arr: any[], origIdx: number, newIdx: number) {
		let val = arr[origIdx];
		arr.splice(origIdx, 1);
		arr.splice(newIdx, 0, val);
		return arr;
	}

	$: console.log($serviceList);
</script>

<div in:fade={{ duration: 250, easing: quintIn, delay: 100 }}
	out:fade={{duration: 100, easing: quintOut}}
>
	<div>
		{#if currentService !== undefined}
			<AddService
				{position}
				bind:currentService
				on:close={() => {
					currentService = undefined;
					name = '';
					url = '';
				}}
			/>
		{/if}

		<div class="md:mt-20 mt-2">
			<table class="w-11/12 mx-auto select-none">
				<thead class="bg-original-table-header text-left">
					<tr>
						<th class="p-2 w-11/12">
							<span
								class="inline-block cursor-text min-w-[12rem] max-w-[30rem] w-auto bg-inherit outline-none border-none text-original-base transition-colors duration-200 ease-in-out bg px-1.5 py-0.5 rounded-md focus:bg-original-table-header-focus"
							>
								Services
							</span>
						</th>

						<th class="text-center" />
					</tr>
				</thead>
				<tbody bind:this={body}>
					{#each $serviceList as service, idx (idx)}
						<tr
							class="even:bg-original-table-row-even cursor-move h-10"
							draggable="true"
							on:dragstart={() => (index = idx)}
							on:dragover={() => (afterIndex = idx)}
							on:dragend={handleDragEnd}
						>
							<td>
								<span
									class="inline-block cursor-text min-w-[12rem] max-w-[30rem] w-auto bg-inherit outline-none border-none text-original-base transition-colors duration-200 ease-in-out bg px-1.5 rounded-md focus:bg-original-table-header-focus"
									contenteditable="false"
									bind:textContent={service.name}
									on:input={saveServices}
								/>
							</td>
							<td class="text-center">
								<button
									class="text-center align-middle cursor-pointer bg-none border-none outline-none text-inherit transition-colors duration-200 ease-in-out hover:text-original-iconhover text-3xl"
									on:click={() => editService(event, service)}
								>
									<Icon icon={service.icon} />
								</button>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</div>

<style>
	:global(span[contentEditable='true']:empty:before) {
		content: attr(placeholder);
		color: #636363;
	}
</style>
