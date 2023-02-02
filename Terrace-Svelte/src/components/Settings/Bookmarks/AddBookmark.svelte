<script>
	import { createEventDispatcher, onDestroy } from 'svelte';
    import { bookmarkList, newBookmark } from "../../../bookmarksStore"
    import { onMount } from "svelte";
    import "carbon-components-svelte/css/g100.css";
    import { Search, Dropdown  } from "carbon-components-svelte";
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
        let icons = [];
        return await fetch(`https://api.iconify.design/search?query=${name}`)
            .then(res => res.json())
            .then(json => {
                json.icons.forEach(element => {
                    icons.push(element)
                });
                return icons
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
        <form action="">
            <div class="input__area">
                <input type="text" class="name" placeholder="Bookmark Title..." bind:value={name}>
                <input type="text" class="url" placeholder="Bookmark URL..." bind:value={url}>
            </div>
            <div class="icon__area">
                <Search placeholder="Search catalog..." bind:value={iconValue} />
                {#each icons as ic}
                    <button on:click|preventDefault={() => icon = ic}>
                        <Icon icon={ic} />
                    </button>
                {/each}
            </div>
            <div class="save__area">
                <button autofocus type="submit" class="submit" 
                    on:click|preventDefault={() => newBookmark(name, url, icon)}
                    on:click={close}>Submit
                </button>
            </div>
            
        </form>
    </div>
</div>

<style>
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
        height: 250px;
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

    input {
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

    input:hover {
        background: linear-gradient(rgb(37, 37, 37),rgb(51, 51, 51)) padding-box,
                    linear-gradient(to right, rgba(61, 61, 61, 0.11), rgba(129, 129, 129, 0)) border-box;
                    border-radius: .5rem;

        border: 1px solid transparent;
    }
    input:focus {
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