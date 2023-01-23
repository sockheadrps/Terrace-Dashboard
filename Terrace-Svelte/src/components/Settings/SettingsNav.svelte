<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
    export let settingsItems = ["Weather"];

</script>

<nav id="navbar">
    <div class="nav__top"></div>
    <div id="nav__items">
        {#each settingsItems as setting}
            <div class="nav__lay"></div>
            <button on:click class={setting.toLowerCase() + " nav__item" +" route"} id={setting.toLowerCase()+"__nav"}>{setting}
            </button>
        {/each}
    </div>
</nav>

<style>

#navbar {
    display: grid;
    min-width: 100px;
    grid-template-columns: 100%;
    grid-gap: 0px;
    background: linear-gradient(to right bottom, rgba(69, 71, 141, 0.212), rgba(53, 56, 128, 0.1));
    border-radius: 2rem 2rem 0rem 0rem;
}


#nav__items{
    display: flex;
    flex-direction: column;
    padding-left: 2rem;
    padding-right: 2rem;
    height: 0;    
}


.nav__item{
    width: 20%;
    margin: 0px;
    background: none;
    border: none;
    color: #808080;
    font-size: 18px;
    cursor: pointer;
    background: rgba(24, 13, 70, 0.719);
    transition: all .2s ease-out;
    padding: 1rem;
    border-radius: 0rem 0rem 1rem 1rem;
}


.nav__item:hover { 
    background: rgba(41, 49, 158, 0.308);
  }

</style>