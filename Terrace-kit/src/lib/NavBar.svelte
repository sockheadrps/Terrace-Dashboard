<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
    let navItems = [{name: "Home", link: ""}, {name: "Notes", link: "notes"}];
    //import {state} from '../../stores.js'
    let hardware = [];

    /*state.subscribe(value => {
        if (value.hardwareList){
            hardware = value.hardwareList[0]
        }
    });*/
</script>


<nav id="navbar">
    <div class="nav__top"></div>
    <div class="routes">
        {#each navItems as nav}
            <a href="/{nav.link}"><button class="nav__item route">{nav.name}</button></a>
        {/each}
    </div>

    <!--    
    <div class="hardware__area">
        <div class="hardwares">
            {#each hardware as hw}
            {#if hw != ""}
                <button on:click class="Hardware hw__nav nav__item">{hw}</button>
            {/if}
            {/each}
        </div>
    </div>
    -->    


    <div id="settings__area">
        <a href="/settings/weather"><button class="nav__item route">Settings</button></a>
    </div>
</nav>


<style>

#navbar {
    display: grid;
    min-width: 100px;
    grid-template-columns: 100%;
    grid-template-rows: 1fr 3fr 8fr 1fr;
    grid-gap: 0px;
    background: linear-gradient(
        to left top,
         rgba(27, 27, 27, 0.911),
         rgba(20, 20, 20, 0.904)
         );
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
    background: rgba(12, 12, 12, 0.918);
}

.nav__item:hover {
    background: linear-gradient(rgb(0, 0, 0),rgb(15, 15, 15)) padding-box,
                linear-gradient(to right, rgba(84, 69, 99, 0.034), rgba(101, 101, 143, 0)) border-box;
    border: 1px solid transparent;
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
    background: rgba(0, 0, 0, 0);

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
    background: rgb(44, 44, 44);
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
