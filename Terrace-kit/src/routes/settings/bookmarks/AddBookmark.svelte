<script>
	import { createEventDispatcher, onDestroy } from 'svelte';
    import { bookmarkList, newBookmark } from "$lib/bookmarksStore"
    import { onMount } from "svelte";
    import Icon from '@iconify/svelte';
    import 'iconify-icon'
	import { fade } from 'svelte/transition';
    let bookmarks = $bookmarkList
    export let currentBookmark
    let icons = []
    const endpoint = (`https://api.iconify.design/collections?pretty=1`)
    let iconValue = ""
    export let position

    async function checkIcon(name) {
        return await fetch(`https://api.iconify.design/search?query=${name}`)
            .then(res => res.json())
            .then(json => {
                return json.icons || [];
            });
    }


    $: checkIcon(iconValue).then(res => {
        icons = res;
    })


	const dispatch = createEventDispatcher();
	const close = () => dispatch('close');

	let modal;

	const handle_keydown = e => {
		if (e.key === 'Escape') {
			close();
			return;
		}

		if (e.key === 'Tab') {
			// trap focus
			const nodes = modal.querySelectorAll('*');
			const tabbable = Array.from(nodes).filter(n => n.tabIndex >= 0);

			let index = tabbable.indexOf(document.activeElement);
			if (index === -1 && e.shiftKey) index = 0;

			index += tabbable.length + (e.shiftKey ? -1 : 1);
			index %= tabbable.length;

			tabbable[index].focus();
			e.preventDefault();
		}
	};

	const previously_focused = typeof document !== 'undefined' && document.activeElement;

	if (previously_focused) {
		onDestroy(() => {
			previously_focused.focus();
		});
	}

    $: {
        setModal(modal)
    }

    function setModal(modal) {
        if (modal !== undefined) {
            modal.style.top = `${position.y + (position.iconHeight /2)}px`
            modal.style.left= `${position.x + (position.iconWidth /2) - modal.getBoundingClientRect().width}px`
        }
    }
    



</script>

<svelte:window on:keydown={handle_keydown}/>

<div class="modal-background" on:click={close}></div>
<div class="modal" transition:fade role="dialog" aria-modal="true" bind:this={modal}>
    <div class="container">
            <div class="icon__area">
                <div class="icon__searchbar">
                    <Icon currentBookmark.icon="ic:baseline-search" />
                    <input type="text" class="icon__search" bind:value={iconValue}>
                    <button autofocus type="submit" class="submit" 
                        on:click|preventDefault={() => newBookmark(currentBookmark)}
                        on:click={close}>Save
                    </button>
                </div>
                
            </div>
            <div class="results">
                {#if currentBookmark.icon && currentBookmark.icon !== ""}
                    <button class="selected" on:click={() => currentBookmark.icon = ""}>
                        <Icon icon={currentBookmark.icon} />
                    </button>
                {/if}
                {#each icons as ic}
                    {#if ic !== currentBookmark.icon}
                        <button style="color:inherit" on:click={() => currentBookmark.icon = ic}>
                            <Icon icon={ic} />
                        </button>
                    {/if}
                {/each}
            </div>
                

    </div>
</div>

<style>
    button {
        cursor: pointer;
        background: none;
        border: none;
        outline: none;
    }

    .icon__searchbar{
        display: flex;
        flex-direction: row;
    }

    .icon__search {
        background-color: rgb(43, 43, 43);
        padding: 0 10px;

        width: 90%;
        outline: none;
        border: none;
        font-size: 25px;
        color: inherit;
        border-radius: 1rem;

    }

    .icon__search::before {
        background: url('https://api.iconify.design/ic/baseline-search.svg') no-repeat left 10px center;
    }


    .results {
        display: grid;
        grid-gap: 5px;
        grid-template-columns: repeat(10, 1fr);
        margin: 0px 5px 5px 5px;
    }

    .selected {
        outline: 2px #55D solid;
        background-color: #444;
        color: inherit;
    }

    .results button {
        font-size: 1.8rem;
        transition: 0.2s background-color ease-in-out;
        background-color: #333;
        border-radius: 4px;
    }

    .results button:hover {
        background-color: #444;
    }

	.modal-background {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0);
        border-radius: 2rem;
        z-index: 3;
	}

	.modal {
        z-index: 4;
		position: absolute;
		width: 25rem;
		max-height: 27rem;
		overflow: auto;
		border-radius: 2em;
		background: rgba(0, 0, 0, 0.877);
	}

    .container{
        display: grid;
        padding: 1rem 1rem 0rem 1rem;
        align-items: center;
        row-gap: 10px;
    }


	button.submit{
        border-radius: .5rem;
        text-align: center;
        width: 5rem;
        height: 2.5rem;
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
        box-sizing: border-box;
        border: 1px solid rgba(10, 6, 24, 0.021);
        background:rgba(125, 125, 129, 0.1);
        cursor: pointer;
        transition: all .01s ease-out;
        font-size: larger;
        color: rgb(136, 136, 136);
	}

    button.submit:hover {
        background: linear-gradient(rgb(37, 37, 37),rgb(51, 51, 51)) padding-box,
                    linear-gradient(to right, rgba(61, 61, 61, 0.11), rgba(129, 129, 129, 0)) border-box;
                    border-radius: .5rem;

        border: 1px solid transparent;
        color: #c4c3c3;
    }

</style>
