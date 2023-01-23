<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
    export let navItems = ["Home", "Notes"];
    import {state} from '../../stores.js'
    let hardware = [];

    $: {
        state.subscribe(value => {
            if (value.hardwareList){ 
                hardware = value.hardwareList[0] 
            }
        });
    }

</script>


<nav id="navbar">
    <div class="nav__top"></div>
    <div class="routes">
        {#each navItems as nav}
            <button on:click class={nav.toLowerCase() + " nav__item" +" route"} id={nav.toLowerCase()+"__nav"} >{nav}</button>
        {/each}
    </div>
    <div class="hardware__area">
        <div class="hardwares">
            {#each hardware as hw}
            {#if hw != ""}
                <button on:click class="Hardware hw__nav nav__item">{hw}</button>
            {/if}
            {/each}
        </div>
    </div>
    <div id="settings__area">
        <button on:click class="nav__item route " id="nav__settings">Settings</button>
    </div>
</nav>


<style>

#navbar {
    display: grid;
    min-width: 100px;
    grid-template-columns: 100%;
    grid-template-rows: 1fr 3fr 8fr 1fr;
    grid-gap: 0px;
    background: linear-gradient(to right bottom, rgba(69, 71, 141, 0.212), rgba(53, 56, 128, 0.1));
    border-radius: 2rem 0rem 0rem 2rem;
}


.routes{
    grid-row: 2;
    display: block;
}

.nav__item{
    display: block;
    margin: 0px;
    width: 100%;
    height: 60px;
    background: none;
    border: none;
    color: #808080;
    font-size: 18px;
    cursor: pointer;
    background: rgba(16, 12, 49, 0.733);
    transition: all .2s ease-out;
}

.nav__item:hover { 
    background: rgba(12, 7, 31, 0.781);
}



.hardware__area{
    display: grid;
    height: 450px;
    grid-template-columns: 1fr;
    grid-row: 3;
    margin: 0;
    overflow-y: scroll;
    overflow: overlay;
}

.hardwares {
    white-space: nowrap;
    scrollbar-width: 90%;
}

.hw__nav {
    display: block;
    width: 100%;
}


.hardware__area::-webkit-scrollbar {
    display: block;
}

.hardware__area::-webkit-scrollbar-track {
    border-radius: 10px;
    background-clip: padding-box;
    margin-right: -1rem;
}

.hardware__area::-webkit-scrollbar-track-piece:end {
    background: transparent;
}

.hardware__area::-webkit-scrollbar-track-piece:start {
    background: transparent;
}

.hardware__area::-webkit-scrollbar-thumb {
    background: rgb(24, 27, 90);
    border-radius: 10px;
    border: 5px solid #0000;
    background-clip: padding-box;
  }
.hardware__area::-webkit-scrollbar-thumb:hover {
    background: #222;
    background-clip: padding-box;
}

#settings__area{
    display: flex;
    flex-direction: column-reverse;
}

#nav__settings{
    border-radius: 0rem 0rem 0rem 2rem;
}

</style>