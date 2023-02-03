<script>
	import { createEventDispatcher, onDestroy } from 'svelte';
    import { bookmarkList, newBookmark } from "../../../bookmarksStore"
    import { onMount } from "svelte";
    import Icon from '@iconify/svelte';
    import 'iconify-icon'
    let bookmarks = $bookmarkList
    let name =""
    let url = ""
    let icon = ""
    let icons = []
    const endpoint = (`https://api.iconify.design/collections?pretty=1`)
    let iconValue = ""


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
</script>

<svelte:window on:keydown={handle_keydown}/>

<div class="modal-background" on:click={close}></div>

<div class="modal" role="dialog" aria-modal="true" bind:this={modal}>
    <div class="container">
            <div class="input__area">
                <input type="text" class="bk__data" placeholder="Bookmark Title..." bind:value={name}>
                <input type="text" class="bk__data" placeholder="Bookmark URL..." bind:value={url}>
            </div>
            <div class="icon__area">
                <div class="icon__searchbar">
                    <input type="text" class="icon__search" bind:value={iconValue}>
                </div>
                <div class="results">
                    {#if icon !== ""}
                        <button class="selected" on:click={() => icon = ""}>
                            <Icon {icon} />
                        </button>
                    {/if}
                    {#each icons as ic}
                        {#if ic !== icon}
                            <button on:click={() => icon = ic}>
                                <Icon icon={ic} />
                            </button>
                        {/if}
                    {/each}
                </div>
            </div>
            <div class="save__area">
                <button autofocus type="submit" class="submit" 
                    on:click|preventDefault={() => newBookmark(name, url, icon)}
                    on:click={close}>Submit
                </button>
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
        vertical-align: middle;
        position: relative;

    }

    .icon__search {
        display: inline-block;
        top: 50%;
        transform: translateY(-50%);
        margin-top: 50px;
        height: 50px;
        font-size: 35px;
        width: 100%;
        padding: 0px 50px;
        background-color: rgb(43, 43, 43);
        outline: none;
        border-bottom: 1px solid rgb(82, 82, 82);
        border-right: 0px;
        background-image:url('https://api.iconify.design/ic/baseline-search.svg');
        background-repeat:no-repeat;
        background-position:left center;outline:0;
        background-size: 30px;
        background-position: 10px 10px;
        color: #a0a0a0;
    }


    .add_bookmark button {
        cursor: pointer;
    }

    .results {
        display: grid;
        grid-gap: 5px;
        grid-template-columns: repeat(15, 1fr);
        margin-top: 10px;
    }

    .selected {
        outline: 2px #55D solid;
        background-color: #444;
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
		background: rgba(0, 0, 0, 0.74);
        border-radius: 2rem;
	}

	.modal {
		position: absolute;
		left: 50%;
		top: 50%;
		width: calc(100vw - 4em);
		max-width: 70em;
		max-height: calc(100vh - 4em);
        height: 35em;
		overflow: auto;
		transform: translate(-50%,-50%);
		padding: 1em;
		border-radius: 2em;
		background: rgb(27, 27, 27);
	}

    .container{
        display: grid;
        align-items: center;
    }

    .input__area{
        margin-top: 1rem;
        grid-row: 1;
        display: grid;
        grid-template-columns: 1fr 1fr;
    }

    .icon__area{
        grid-template-columns: 1;
        grid-row: 2;
        height: 100%;
        font-size: 45px;
    }

    .save__area{
        grid-row: 3;
        display: block;
        flex-direction: column-reverse;
        align-items: center;

    }

	button.submit{
        margin-top: 1rem;
        border-radius: .5rem;
        text-align: center;
        width: 16rem;
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

    .bk__data  {
        background-color: rgb(26, 27, 31);
        border-radius: .5rem;
        text-align: center;
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
        box-sizing: border-box;
        border: 1px solid rgba(10, 6, 24, 0.021);
        background:rgba(64, 64, 73, 0.1);
        color: #808080;
        height: 2rem;
        margin: 0 1rem 1rem 0;
    }

    .bk__data :hover {
        background: linear-gradient(rgb(37, 37, 37),rgb(51, 51, 51)) padding-box,
                    linear-gradient(to right, rgba(61, 61, 61, 0.11), rgba(129, 129, 129, 0)) border-box;
                    border-radius: .5rem;

        border: 1px solid transparent;
    }
    .bk__data :focus {
        background: linear-gradient(rgb(43, 43, 43),rgb(66, 66, 66)) padding-box,
                    linear-gradient(to right, rgba(61, 61, 61, 0.11), rgba(129, 129, 129, 0)) border-box;
                    border-radius: .5rem;

        border-radius: 2rem;
        border: 1px solid rgba(10, 6, 24, 0.021);
        opacity: .7;
        color: #bebebe;
        outline: none;
    }
</style>
