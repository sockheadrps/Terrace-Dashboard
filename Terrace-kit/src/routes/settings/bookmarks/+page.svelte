<script lang="ts">
	import { bookmarkList, deleteBookmark, loadBookmarks, saveBookmarks } from '$lib/bookmarksStore';
	import AddBookmark from './AddBookmark.svelte';
	import Icon from '@iconify/svelte';
	import 'iconify-icon';
	import type { BookMark, KeyFrame } from '$lib/bookmarkTypes';
	import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';
    import { quintIn, quintOut } from 'svelte/easing';

	let currentBookmark: BookMark | undefined;
	let name = '';
	let url = '';
	let body: Element;
	let index: number;
	let afterIndex: number;
	let position: object;
	let ready = false;

	onMount(() => {
		$bookmarkList = loadBookmarks();
		ready = true;
	});

	function editBookmark(event: MouseEvent, bookmark: BookMark) {
		position = {
			x: event.srcElement.getBoundingClientRect().x,
			y: event.srcElement.getBoundingClientRect().y,
			iconWidth: event.srcElement.getBoundingClientRect().width,
			iconHeight: event.srcElement.getBoundingClientRect().height
		};
		currentBookmark = bookmark;
	}

	function handleDragEnd() {
		let startKeys = transitionKeys();
		let endKeys = move([...startKeys], index, afterIndex);

		animateShift(startKeys, endKeys);
		move($bookmarkList, index, afterIndex);

		$bookmarkList = $bookmarkList;
		saveBookmarks($bookmarkList);
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
</script>

{#if ready}
	<div in:fade={{ duration: 250, easing: quintIn, delay:250 }}
	out:fade={{duration: 100, easing: quintOut}}>
		{#if currentBookmark !== undefined}
			<AddBookmark
				{position}
				bind:currentBookmark
				on:close={() => {
					currentBookmark = undefined;
					name = '';
					url = '';
				}}
			/>
		{/if}

		<div class="mt-20 tablet:mt-5 overflow-y-auto tablet:h-72 scroll">
			<table class="w-11/12 mx-auto select-none">
				<thead class="bg-original-table-header text-left">
					<tr>
						<th class="p-2">
							<span
								class="inline-block cursor-text min-w-[12rem] max-w-[30rem] w-auto bg-inherit outline-none border-none text-original-base transition-colors duration-200 ease-in-out bg px-1.5 py-0.5 rounded-md focus:bg-original-table-header-focus"
								contenteditable="true"
								spellcheck="false"
								placeholder="Title"
								bind:textContent={name}
							/>
						</th>
						<th>
							<span
								class="inline-block cursor-text min-w-[12rem] max-w-[30rem] w-auto bg-inherit outline-none border-none text-original-base transition-colors duration-200 ease-in-out bg px-1.5 py-0.5 rounded-md focus:bg-original-table-header-focus"
								contenteditable="true"
								spellcheck="false"
								placeholder="URL"
								bind:textContent={url}
							/>
						</th>
						<th class="text-center">
							<button
								class="align-middle text-3xl"
								on:click={(event) => editBookmark(event, { name, url, icon: null })}
							>
								<Icon icon="material-symbols:bookmark-add-outline" />
							</button>
						</th>
					</tr>
				</thead>
				<tbody bind:this={body} class="overflow-auto w-full">
					{#each $bookmarkList as bookmark, idx (idx)}
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
									contenteditable="true"
									spellcheck="false"
									bind:textContent={bookmark.name}
									on:input={saveBookmarks}
								/>
							</td>
							<td>
								<span
									class="inline-block cursor-text min-w-[12rem] max-w-[30rem] w-auto bg-inherit outline-none border-none text-original-base transition-colors duration-200 ease-in-out bg px-1.5 rounded-md focus:bg-original-table-header-focus"
									contenteditable="true"
									spellcheck="false"
									bind:textContent={bookmark.url}
									on:input={saveBookmarks}
								/>
							</td>
							<td class="text-center">
								<button
									class="text-center align-middle cursor-pointer bg-none border-none outline-none text-inherit transition-colors duration-200 ease-in-out hover:text-original-iconhover text-3xl"
									on:click={() => editBookmark(event, bookmark)}
								>
									<Icon icon={bookmark.icon} />
								</button>
								<button
									class="text-center text-red-400 align-middle cursor-pointer bg-none border-none outline-none text-inherit transition-colors duration-200 ease-in-out hover:text-original-iconhover text-3xl"
									on:click={() => deleteBookmark(bookmark)}
								>
									<Icon icon="carbon:trash-can" />
								</button>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
{/if}

<style>
	:global(span[contentEditable='true']:empty:before) {
		content: attr(placeholder);
		color: #636363;
	}

	.scroll::-webkit-scrollbar {
    background: rgba(0, 0, 0, 0);
    display: block;
}
	.scroll::-webkit-scrollbar-track {
		border-radius: 10px;
		background-clip: padding-box;
	}
	.scroll::-webkit-scrollbar-track-piece:end {
		background: transparent;
	}
	.scroll::-webkit-scrollbar-track-piece:start {
		background: transparent;
  		}
	.scroll::-webkit-scrollbar-thumb {
		background: rgb(44, 44, 44);
		border-radius: 10px;
		border: 5px solid #0000;
		background-clip: padding-box;
	}
	.scroll::-webkit-scrollbar-thumb:hover {
		background: #222;
		background-clip: padding-box;
	}
</style>
